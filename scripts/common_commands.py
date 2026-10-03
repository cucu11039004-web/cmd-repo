"""按 docs/pins.yml 生成首页命令；本地预览时提供点选和收集箱归档接口。

构建时只改生成的网页，不写回 Markdown；只有 mkdocs serve 下的本地接口会改写 docs/ 里的文件。
"""

import html
import json
import os
import re
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional
from urllib.parse import urlsplit

import yaml
from mkdocs.exceptions import PluginError
from mkdocs.utils import get_relative_url


PLACEHOLDER = "<!-- common-commands -->"
LEGACY_MARKER = "<!-- common -->"
PINS_FILE = "pins.yml"
INBOX_FILE = "inbox.md"
PINS_HEADER = (
    "# 首页命令：本地预览时点 ☆ 自动写入，也可以手动编辑。\n"
    "# id 是条目锚点，added 是加入首页的时间；首页每列按时间倒序显示。\n"
)
TONES = 4
LANGUAGES = ("bash", "text", "python")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
ANCHOR = re.compile(r"^(.*?)\s+\{\s*#([^\s}]+)\s*\}\s*$")
ENGLISH_ID = re.compile(r"[a-z][a-z0-9-]*\Z")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
ENTRY_HEADING = re.compile(r'<h3 id="([^"]+)"')
RECORD = re.compile(r"^- (?:(\d{4}-\d{2}-\d{2}) )?(.+)$")
NOTE_PREFIXES = {"作用": "effect", "场景": "scene", "遇到场景": "scene", "来源": "source"}
UNSORTED = "未分小节"
UNSORTED_NOTE = "归档时没有选小节的条目，有空再挪到合适的小节。"


@dataclass
class Command:
    title: str
    anchor: Optional[str]
    source: str
    line: int
    section: str = ""
    category: str = ""
    code: Optional[str] = None
    effect: Optional[str] = None


# ---------- 读取 Markdown ----------

def closes_fence(fence: str, line: str) -> bool:
    return re.fullmatch(r" {0,3}" + re.escape(fence[0]) + r"{" + str(len(fence)) + r",}\s*", line) is not None


def scan_headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """给出代码块之外的标题：（行下标、级别、去掉固定锚点后的标题）。"""
    headings = []
    fence = None
    for index, line in enumerate(lines):
        if fence is not None:
            if closes_fence(fence, line):
                fence = None
            continue
        opening = FENCE.match(line)
        if opening:
            fence = opening[1]
            continue
        heading = HEADING.match(line)
        if heading:
            explicit = ANCHOR.match(heading[2])
            headings.append((index, len(heading[1]), explicit[1] if explicit else heading[2]))
    return headings


def collect_commands(markdown: str, source: str) -> list[Command]:
    """按文件顺序读取三级标题条目，忽略代码块内的标题和说明。"""
    commands = []
    anchors = set()
    current = None
    fence = None
    code_lines = []

    def finish():
        if current is None:
            return
        prefix = f"{source}:{current.line}「{current.title}」"
        if current.anchor is None or not ENGLISH_ID.fullmatch(current.anchor):
            raise PluginError(f"{prefix}：条目缺少固定英文锚点（例如 {{ #tmux-detach }}）。")
        if current.code is None or not current.code.strip():
            raise PluginError(f"{prefix}：条目缺少完整且非空的命令代码块。")
        commands.append(current)

    for number, line in enumerate(markdown.splitlines(), start=1):
        # 围栏内部内容原样保留，不能被当作 Markdown 元数据解析。
        if fence is not None:
            if closes_fence(fence, line):
                if current is not None and current.code is None:
                    current.code = "\n".join(code_lines)
                fence = None
            else:
                code_lines.append(line)
            continue
        opening = FENCE.match(line)
        if opening:
            fence = opening[1]
            code_lines = []
            continue

        heading = HEADING.match(line)
        if heading:
            level = len(heading[1])
            title = heading[2]
            explicit = ANCHOR.match(title)
            anchor = explicit[2] if explicit else None
            if anchor is not None:
                if anchor in anchors:
                    raise PluginError(f"{source}:{number}「{title}」：固定锚点 #{anchor} 重复。")
                anchors.add(anchor)
                title = explicit[1]
            if level <= 3:
                finish()
                current = Command(title, anchor, source, number) if level == 3 else None
            continue

        if line.strip() == LEGACY_MARKER:
            raise PluginError(
                f"{source}:{number}：首页改由 docs/{PINS_FILE} 决定，请删除 {LEGACY_MARKER} 标记。"
            )
        if current is not None and line.startswith("- 作用："):
            current.effect = line.removeprefix("- 作用：").strip()

    finish()
    return commands


def category_pages(nav: list, section: Optional[str] = None) -> Iterator[tuple[str, str, str]]:
    """按导航顺序给出（大类、页面标题、文件），首页和收集箱除外。"""
    for item in nav:
        if not isinstance(item, dict):
            continue
        for title, target in item.items():
            if isinstance(target, list):
                yield from category_pages(target, section or title)
            elif isinstance(target, str) and target.endswith(".md"):
                if target not in {"index.md", INBOX_FILE}:
                    yield section or title, title, target


def section_tones(nav: list) -> dict[str, int]:
    """大类按导航顺序循环使用四种颜色。"""
    tones = {}
    for section, _, _ in category_pages(nav):
        tones.setdefault(section, len(tones) % TONES + 1)
    return tones


def read_page(docs_dir: Path, source: str) -> str:
    try:
        return (docs_dir / source).read_text(encoding="utf-8")
    except OSError as error:
        raise PluginError(f"无法读取 {source}：{error}") from error


def collect_entries(nav: list, docs_dir: Path) -> dict[str, Command]:
    """读取全部分类页；锚点同时是首页选择的 ID，必须全站唯一。"""
    entries = {}
    for section, title, source in category_pages(nav):
        for command in collect_commands(read_page(docs_dir, source), source):
            previous = entries.get(command.anchor)
            if previous is not None:
                raise PluginError(
                    f"{source}:{command.line}「{command.title}」：锚点 #{command.anchor} "
                    f"与 {previous.source}:{previous.line} 重复，锚点需要全站唯一。"
                )
            command.section = section
            command.category = title
            entries[command.anchor] = command
    return entries


def read_pins(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise PluginError(f"{PINS_FILE} 无法读取：{error}") from error
    if data is None:
        return []
    if not isinstance(data, list):
        raise PluginError(f"{PINS_FILE} 应该是列表，每项包含 id 和 added。")
    pins = []
    seen = set()
    for number, item in enumerate(data, start=1):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or item.get("added") is None:
            raise PluginError(f"{PINS_FILE} 第 {number} 项需要 id 和 added 两个字段。")
        if item["id"] in seen:
            raise PluginError(f"{PINS_FILE} 第 {number} 项：#{item['id']} 重复。")
        seen.add(item["id"])
        pins.append({"id": item["id"], "added": str(item["added"])})
    return pins


def load_site(config) -> tuple[dict[str, Command], list[dict]]:
    docs_dir = Path(config["docs_dir"])
    entries = collect_entries(config["nav"], docs_dir)
    pins = read_pins(docs_dir / PINS_FILE)
    for pin in pins:
        if pin["id"] not in entries:
            raise PluginError(
                f"{PINS_FILE} 里的 #{pin['id']} 找不到对应条目：删掉这一项，或恢复该条目的锚点。"
            )
    return entries, pins


# ---------- 构建：首页与分类页 ----------

_site: dict = {}


def on_pre_build(config, **kwargs):
    entries, pins = load_site(config)
    _site.update(
        entries=entries,
        pins=pins,
        pinned={pin["id"] for pin in pins},
        tones=section_tones(config["nav"]),
    )


def render_pin(command: Command, page, files) -> str:
    target = files.get_file_from_path(command.source)
    href = f"{get_relative_url(target.url, page.url)}#{command.anchor}"
    return (
        f'<li class="pin-item" data-pin-id="{command.anchor}">'
        f'<span class="pin-tag">{html.escape(command.category)}</span>'
        f'<a class="pin-code" href="{html.escape(href)}" title="查看详情"><code>{html.escape(command.code)}</code></a>'
        '<button class="pin-copy" type="button" title="复制命令" aria-label="复制命令"></button>'
        '<button class="pin-remove" type="button" title="移出首页" aria-label="移出首页" hidden>✕</button>'
        "</li>"
    )


def render_home(page, files) -> str:
    """每个大类一列，列内最新加入的在前；只显示小类和命令，忘了再点进详情。"""
    pins = sorted(_site["pins"], key=lambda pin: pin["added"], reverse=True)
    columns = {section: [] for section in _site["tones"]}
    for pin in pins:
        command = _site["entries"][pin["id"]]
        columns[command.section].append(render_pin(command, page, files))
    board = []
    for section, tone in _site["tones"].items():
        items = "".join(columns[section]) or '<li class="pin-empty">暂无</li>'
        board.append(
            f'<section class="pin-column" data-tone="{tone}">'
            f'<h2 class="pin-column-title">{html.escape(section)}'
            f'<span class="pin-column-count">{len(columns[section])}</span></h2>'
            f'<ul class="pin-list">{items}</ul></section>'
        )
    if pins:
        intro = f'<p class="pin-count">共 <span class="pin-number">{len(pins)}</span> 条。点命令查看详情，点右侧图标复制。</p>'
    else:
        intro = '<p class="pin-count">还没有加入首页的命令。在本地预览（<code>cmdserve</code>）里，到分类页点条目标题旁的 ☆。</p>'
    # 每段放在一行，Markdown 会把它当作原样输出的 HTML 块。
    return f'{intro}\n\n<div class="pin-board">{"".join(board)}</div>'


def on_page_markdown(markdown, *, page, files, **kwargs):
    if page.file.src_uri != "index.md":
        return markdown
    if markdown.count(PLACEHOLDER) != 1:
        raise PluginError(f"index.md：必须包含且只包含一个 {PLACEHOLDER} 汇总占位符。")
    return markdown.replace(PLACEHOLDER, render_home(page, files))


def on_page_content(html_content, *, page, **kwargs):
    """分类页条目标题加上 ID 和已选状态；收集箱末尾留出本地归档界面的位置。"""
    if page.file.src_uri == INBOX_FILE:
        return html_content + '<div class="inbox-filing" data-inbox-filing hidden></div>'
    entries = _site["entries"]

    def mark(match):
        anchor = match[1]
        command = entries.get(anchor)
        if command is None or command.source != page.file.src_uri:
            return match[0]
        pinned = " data-pinned" if anchor in _site["pinned"] else ""
        return f'{match[0]} data-pin-id="{anchor}"{pinned}'

    return ENTRY_HEADING.sub(mark, html_content)


# ---------- 本地接口用到的读写 ----------

class RequestError(Exception):
    def __init__(self, status: str, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def write_text_atomic(path: Path, text: str) -> None:
    # 先写临时文件再替换，避免预览重建时读到写了一半的文件。
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def write_pins(path: Path, pins: list[dict]) -> None:
    body = yaml.safe_dump(pins, allow_unicode=True, sort_keys=False) if pins else "[]\n"
    write_text_atomic(path, PINS_HEADER + body)


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def parse_note(text: str) -> dict[str, str]:
    """按「命令；作用；来源」拆分一条记录；带「作用：」等前缀的段落按前缀归位。

    优先按中文分号拆分；整条都没有中文分号时，才按英文分号拆分。
    """
    fields = {"code": "", "effect": "", "scene": "", "source": ""}
    loose = []
    separator = "；" if "；" in text else ";"
    for part in (part.strip() for part in text.split(separator)):
        if not part:
            continue
        prefix, separator, rest = part.partition("：")
        key = NOTE_PREFIXES.get(prefix) if separator else None
        if key and not fields[key]:
            fields[key] = rest.strip()
        else:
            loose.append(part)
    empty = [key for key in ("code", "effect", "source") if not fields[key]]
    for key, part in zip(empty, loose):
        fields[key] = part
    return fields


def read_records(markdown: str) -> list[dict]:
    """收集箱里每个 “- 日期 内容” 列表项是一条记录。"""
    records = []
    fence = None
    for line in markdown.splitlines():
        if fence is not None:
            if closes_fence(fence, line):
                fence = None
            continue
        opening = FENCE.match(line)
        if opening:
            fence = opening[1]
            continue
        match = RECORD.match(line)
        if match:
            records.append({"raw": line, "date": match[1] or "", "text": match[2], "fields": parse_note(match[2])})
    return records


def remove_record(markdown: str, raw: str) -> str:
    lines = markdown.split("\n")
    if raw not in lines:
        raise RequestError("409 Conflict", "收集箱里找不到这条记录，可能已经处理过，请刷新页面。")
    index = lines.index(raw)
    del lines[index]
    # note 写入时每条前面带一个空行，一起删掉，避免空行越积越多。
    if index > 0 and not lines[index - 1].strip() and (index >= len(lines) or not lines[index].strip()):
        del lines[index - 1]
    return "\n".join(lines)


def default_language(source: str) -> str:
    if source.startswith("editing/"):
        return "text"
    if source.startswith("python/") and source != "python/env.md":
        return "python"
    return "bash"


def page_outline(nav: list, docs_dir: Path) -> list[dict]:
    pages = []
    for section, title, source in category_pages(nav):
        lines = read_page(docs_dir, source).split("\n")
        pages.append({
            "section": section,
            "title": title,
            "source": source,
            "language": default_language(source),
            "subsections": [name for _, level, name in scan_headings(lines) if level == 2],
        })
    return pages


def make_anchor(code: str, source: str, taken: set) -> str:
    """用命令里的英文单词生成锚点，如 ls -la → ls-la；键位类页面加页面名前缀，如 emacs-c-n。"""
    slug = Path(source).stem
    words = re.findall(r"[a-z0-9]+", code.split("\n")[0].lower())[:4]
    if source.startswith("editing/") or not words or not words[0][0].isalpha():
        words = [slug] + words
    base = "-".join(words)[:40].rstrip("-")
    anchor, number = base, 2
    while anchor in taken:
        anchor, number = f"{base}-{number}", number + 1
    return anchor


def render_entry(fields: dict[str, str]) -> list[str]:
    """标题就是作用；来源、场景只在填写时出现。"""
    code = fields["code"]
    # 命令里含有反引号时，围栏要比其中最长的一串更长。
    longest = max((len(run) for run in re.findall(r"`+", code)), default=0)
    fence = "`" * max(3, longest + 1)
    lines = [
        f"### {fields['effect']} {{ #{fields['anchor']} }}",
        "",
        f"{fence}{fields['language']}",
        *code.split("\n"),
        fence,
    ]
    details = [f"- {label}：{fields[key]}" for key, label in (("scene", "遇到场景"), ("source", "来源")) if fields[key]]
    return lines + ([""] + details if details else [])


def insert_entry(markdown: str, subsection: int, entry: list[str]) -> str:
    """把条目追加到第 subsection 个二级小节的末尾，文件顺序即添加顺序。"""
    lines = markdown.split("\n")
    headings = scan_headings(lines)
    starts = [index for index, level, _ in headings if level == 2]
    start = starts[subsection]
    end = next((index for index, level, _ in headings if index > start and level <= 2), len(lines))
    at = end
    while at > start + 1 and not lines[at - 1].strip():
        at -= 1
    block = [""] + entry
    if at == end and end < len(lines):
        block.append("")
    lines[at:at] = block
    result = "\n".join(lines)
    return result if result.endswith("\n") else result + "\n"


def append_unsorted(markdown: str, entry: list[str]) -> str:
    """没选小节时放进页面末尾的「未分小节」，没有就先建一个。"""
    names = [name for _, level, name in scan_headings(markdown.split("\n")) if level == 2]
    if UNSORTED not in names:
        markdown = markdown.rstrip("\n") + f"\n\n## {UNSORTED}\n\n{UNSORTED_NOTE}\n"
        names.append(UNSORTED)
    return insert_entry(markdown, names.index(UNSORTED), entry)


def single_line(request: dict, key: str, label: str, required: bool = True) -> str:
    value = request.get(key, "")
    if not isinstance(value, str):
        raise RequestError("400 Bad Request", f"{label}应为文本。")
    value = " ".join(value.replace("\r", "").split("\n")).strip()
    if required and not value:
        raise RequestError("400 Bad Request", f"请填写{label}。")
    return value


# ---------- 本地接口（只在 mkdocs serve 时存在） ----------

def on_serve(server, *, config, **kwargs):
    """包装预览服务器：路径以 /__pins__、/__inbox__ 结尾的请求由这里处理，其余交给 MkDocs。"""
    app = server.get_app()
    lock = threading.Lock()
    nav = config["nav"]
    docs_dir = Path(config["docs_dir"])
    pins_path = docs_dir / PINS_FILE
    inbox_path = docs_dir / INBOX_FILE

    def set_pin(pins: list[dict], anchor: str, pinned: bool, known: set) -> list[dict]:
        # 顺便清理已经不存在的条目，新加入的放在最前面。
        pins = [pin for pin in pins if pin["id"] != anchor and pin["id"] in known]
        if pinned:
            pins.insert(0, {"id": anchor, "added": now()})
        return pins

    def pins_api(request: Optional[dict]) -> dict:
        if request is None:
            return {"ok": True}
        anchor, pinned = request.get("id"), request.get("pinned")
        if not isinstance(anchor, str) or not isinstance(pinned, bool):
            raise RequestError("400 Bad Request", "请求格式应为 {\"id\": 锚点, \"pinned\": true/false}。")
        entries = collect_entries(nav, docs_dir)
        if pinned and anchor not in entries:
            raise RequestError("404 Not Found", f"找不到条目 #{anchor}。")
        write_pins(pins_path, set_pin(read_pins(pins_path), anchor, pinned, set(entries)))
        return {"ok": True, "id": anchor, "pinned": pinned}

    def inbox_api(request: Optional[dict]) -> dict:
        if request is None:
            entries = collect_entries(nav, docs_dir)
            return {
                "ok": True,
                "records": read_records(read_page(docs_dir, INBOX_FILE)),
                "pages": page_outline(nav, docs_dir),
                "anchors": sorted(entries),
                # 用来提醒收集箱里的命令是否已经有条目。
                "existing": {command.code.strip(): f"{command.category} › {command.title}" for command in entries.values()},
            }
        if request.get("action") == "delete":
            raw = request.get("raw")
            if not isinstance(raw, str):
                raise RequestError("400 Bad Request", "缺少要删除的记录。")
            write_text_atomic(inbox_path, remove_record(read_page(docs_dir, INBOX_FILE), raw))
            return {"ok": True}
        items = request.get("items")
        if request.get("action") != "file" or not isinstance(items, list) or not items:
            raise RequestError("400 Bad Request", "请求格式应为 {\"action\": \"file\", \"items\": [...]} 或删除。")
        return file_records(items)

    def file_records(items: list) -> dict:
        """一次归档多条：全部检查通过才写入，任何一条有问题都不改文件。"""
        pages = {page["source"]: page for page in page_outline(nav, docs_dir)}
        taken = set(collect_entries(nav, docs_dir))
        inbox = read_page(docs_dir, INBOX_FILE)
        pins = read_pins(pins_path)
        texts = {}
        filed = []
        for number, item in enumerate(items, start=1):
            try:
                if not isinstance(item, dict) or not isinstance(item.get("raw"), str):
                    raise RequestError("400 Bad Request", "缺少要归档的记录。")
                inbox = remove_record(inbox, item["raw"])
                page = pages.get(item.get("page"))
                if page is None:
                    raise RequestError("400 Bad Request", "请选择分类。")
                subsection = item.get("subsection")
                if subsection is not None and (
                    not isinstance(subsection, int) or not 0 <= subsection < len(page["subsections"])
                ):
                    raise RequestError("400 Bad Request", "小节不存在，请刷新页面。")
                code = item.get("code")
                if not isinstance(code, str) or not code.strip():
                    raise RequestError("400 Bad Request", "请填写命令。")
                fields = {
                    "code": code.replace("\r", "").strip("\n"),
                    "effect": single_line(item, "effect", "作用"),
                    "scene": single_line(item, "scene", "遇到场景", required=False),
                    "source": single_line(item, "source", "来源", required=False),
                    "language": item.get("language") or page["language"],
                    "anchor": single_line(item, "anchor", "锚点", required=False),
                }
                if ANCHOR.match(fields["effect"]) or fields["effect"].startswith("#"):
                    raise RequestError("400 Bad Request", "作用会成为标题，里面不要写锚点或以 # 开头。")
                if fields["language"] not in LANGUAGES:
                    raise RequestError("400 Bad Request", f"代码语言只能是 {'、'.join(LANGUAGES)}。")
                if fields["anchor"]:
                    if not ENGLISH_ID.fullmatch(fields["anchor"]):
                        raise RequestError("400 Bad Request", "锚点以小写字母开头，只能含小写字母、数字和连字符。")
                    if fields["anchor"] in taken:
                        raise RequestError("409 Conflict", f"锚点 #{fields['anchor']} 已被使用。")
                else:
                    fields["anchor"] = make_anchor(fields["code"], page["source"], taken)
            except RequestError as error:
                label = item.get("code") if isinstance(item, dict) else None
                raise RequestError(error.status, f"第 {number} 条（{label or '无命令'}）：{error.message}") from None
            taken.add(fields["anchor"])
            source = page["source"]
            text = texts.get(source) or read_page(docs_dir, source)
            entry = render_entry(fields)
            texts[source] = insert_entry(text, subsection, entry) if subsection is not None else append_unsorted(text, entry)
            if item.get("pin", True):
                pins = set_pin(pins, fields["anchor"], True, taken)
            where = page["subsections"][subsection] if subsection is not None else UNSORTED
            filed.append({"anchor": fields["anchor"], "page": source, "where": f"{page['title']} › {where}"})

        for source, text in texts.items():
            collect_commands(text, source)  # 写入前再按构建规则检查一遍
        # 依次写分类页、首页清单、收集箱，任何一步之后的中间状态都能正常构建。
        for source, text in texts.items():
            write_text_atomic(docs_dir / source, text)
        write_pins(pins_path, pins)
        write_text_atomic(inbox_path, inbox)
        return {"ok": True, "filed": filed}

    routes = {"/__pins__": pins_api, "/__inbox__": inbox_api}

    def respond(start_response, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        start_response(status, [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
        ])
        return [body]

    def read_request(environ) -> dict:
        # 要求 JSON 且来源与本站一致，其他网页无法借浏览器改写文件。
        origin = environ.get("HTTP_ORIGIN") or ""
        if (
            not environ.get("CONTENT_TYPE", "").startswith("application/json")
            or urlsplit(origin).netloc != environ.get("HTTP_HOST")
        ):
            raise RequestError("403 Forbidden", "只接受本站页面发出的 JSON 请求。")
        length = int(environ.get("CONTENT_LENGTH") or 0)
        if length > 65536:
            raise RequestError("413 Payload Too Large", "请求内容太长。")
        try:
            request = json.loads(environ["wsgi.input"].read(length))
        except ValueError:
            raise RequestError("400 Bad Request", "请求不是合法的 JSON。") from None
        if not isinstance(request, dict):
            raise RequestError("400 Bad Request", "请求应为 JSON 对象。")
        return request

    def app_with_api(environ, start_response):
        path = environ.get("PATH_INFO", "")
        handler = next((api for suffix, api in routes.items() if path.endswith(suffix)), None)
        if handler is None:
            return app(environ, start_response)
        try:
            method = environ["REQUEST_METHOD"]
            if method == "GET":
                with lock:
                    payload = handler(None)
            elif method == "POST":
                request = read_request(environ)
                with lock:
                    payload = handler(request)
            else:
                raise RequestError("405 Method Not Allowed", "只支持 GET 和 POST。")
        except RequestError as error:
            return respond(start_response, error.status, {"error": error.message})
        except PluginError as error:
            return respond(start_response, "409 Conflict", {"error": str(error)})
        return respond(start_response, "200 OK", payload)

    server.set_app(app_with_api)
    return server
