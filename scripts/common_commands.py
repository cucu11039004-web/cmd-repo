"""从分类 Markdown 汇总常用命令；只改构建中的首页，不写回源文件。"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

from mkdocs.exceptions import PluginError


PLACEHOLDER = "<!-- common-commands -->"
COMMON_MARKER = "<!-- common -->"
LIMIT = 4
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
ANCHOR = re.compile(r"^(.*?)\s+\{\s*#([^\s}]+)\s*\}\s*$")
ENGLISH_ID = re.compile(r"[a-z][a-z0-9-]*\Z")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
CODE_DETAIL = re.compile(
    r'(<pre\b[^>]*>(?:<span[^>]*></span>)?<code\b[^>]*>)(.*?)'
    r'(</code></pre></div>)\s*<p><a href="([^"]+)">查看详情</a></p>',
    re.DOTALL,
)


@dataclass
class Command:
    title: str
    anchor: Optional[str]
    line: int
    common: bool = False
    code: Optional[str] = None
    effect: Optional[str] = None


def collect_commands(markdown: str, source: str) -> list[Command]:
    """按文件顺序读取三级标题条目，忽略代码块内的标题、标记和说明。"""
    commands = []
    anchors = set()
    current = None
    fence = None
    code_lines = []

    def finish():
        if current is None or not current.common:
            return
        prefix = f"{source}:{current.line}「{current.title}」"
        if current.anchor is None or not ENGLISH_ID.fullmatch(current.anchor):
            raise PluginError(f"{prefix}：常用条目缺少固定英文锚点（例如 {{ #git-status }}）。")
        if current.code is None or not any(
            line.strip() for line in current.code.splitlines()[1:-1]
        ):
            raise PluginError(f"{prefix}：常用条目缺少完整且非空的命令代码块。")
        if not current.effect:
            raise PluginError(f"{prefix}：常用条目缺少非空的「- 作用：」说明。")
        commands.append(current)

    for number, line in enumerate(markdown.splitlines(), start=1):
        # 围栏内部内容原样保留，不能被当作 Markdown 元数据解析。
        if fence is not None:
            code_lines.append(line)
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + r"{" + str(len(fence)) + r",}\s*", line):
                if current is not None and current.code is None:
                    current.code = "\n".join(code_lines)
                fence = None
            continue
        opening = FENCE.match(line)
        if opening:
            fence = opening[1]
            code_lines = [line]
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
                current = Command(title, anchor, number) if level == 3 else None
            continue

        if line.strip() == COMMON_MARKER:
            if current is None:
                raise PluginError(f"{source}:{number}：常用标记必须放在命令的三级标题下。")
            current.common = True
        elif current is not None and line.startswith("- 作用："):
            current.effect = line.removeprefix("- 作用：").strip()

    finish()
    return commands


def category_pages(nav: list) -> Iterator[tuple[str, str]]:
    """按导航顺序读取分类页，也支持将来出现的嵌套导航。"""
    for item in nav:
        if not isinstance(item, dict):
            continue
        for title, target in item.items():
            if isinstance(target, list):
                yield from category_pages(target)
            elif isinstance(target, str) and target.endswith(".md"):
                if target not in {"index.md", "inbox.md"}:
                    yield title, target


def on_page_markdown(markdown, *, page, config, **kwargs):
    if page.file.src_uri != "index.md":
        return markdown
    if markdown.count(PLACEHOLDER) != 1:
        raise PluginError(f"index.md：必须包含且只包含一个 {PLACEHOLDER} 汇总占位符。")

    sections = []
    for title, source in category_pages(config["nav"]):
        # 每次构建都重新读取，mkdocs serve 修改分类页时也会同步刷新首页。
        path = Path(config["docs_dir"]) / source
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as error:
            raise PluginError(f"无法读取分类页 {source}：{error}") from error
        commands = collect_commands(content, source)
        if not commands:
            continue
        sections.append(f"## [{title}]({source})")
        for command in commands[:LIMIT]:
            sections.append(
                f"{command.code}\n\n[查看详情]({source}#{command.anchor})"
            )
    return markdown.replace(PLACEHOLDER, "\n\n".join(sections))


def on_page_content(html, *, page, **kwargs):
    """将详情链接移到命令文本上；保留主题的代码块和原生复制按钮。"""
    if page.file.src_uri != "index.md":
        return html

    def link_command(match):
        opening, code, closing, href = match.groups()
        return (
            f'{opening}<a href="{href}" title="查看命令详情">'
            f"{code}</a>{closing}"
        )

    linked = CODE_DETAIL.sub(link_command, html)
    # 分类块在桌面并排、手机纵向排列；标题仍由 Markdown 生成并保留锚点。
    sections = re.split(r"(?=<h2\b)", linked)
    if len(sections) == 1:
        return linked
    groups = "\n".join(
        f'<section class="common-command-group">{section}</section>'
        for section in sections[1:]
    )
    return f'{sections[0]}<div class="common-commands-grid">{groups}</div>'
