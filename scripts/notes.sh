# 用 source 加载此文件，支持 zsh 和 bash。根据文件位置定位仓库。
if [ -n "${ZSH_VERSION:-}" ]; then
  _cheatsheet_source="${(%):-%x}"
elif [ -n "${BASH_VERSION:-}" ]; then
  _cheatsheet_source="${BASH_SOURCE[0]}"
else
  printf '%s\n' '请在 zsh 或 bash 中加载 notes.sh。' >&2
  return 1
fi
CHEATSHEET_DIR="$(cd -- "$(dirname -- "$_cheatsheet_source")/.." && pwd)"
unset _cheatsheet_source

note() {
  if [ "$#" -eq 0 ] || [ -z "$*" ]; then
    printf '%s\n' "用法：note '命令；作用；场景；来源'" >&2
    return 1
  fi
  if [ ! -f "$CHEATSHEET_DIR/docs/inbox.md" ]; then
    printf '%s\n' '找不到收集箱，请重新加载 notes.sh。' >&2
    return 1
  fi
  printf '\n- %s %s\n' "$(date +%F)" "$*" >> "$CHEATSHEET_DIR/docs/inbox.md" || return
  printf '%s\n' '已记录到 inbox。'
}

# 子 shell 保证执行成功或失败都不改变调用者的工作目录。
notepush() (
  cd -- "$CHEATSHEET_DIR" || exit
  if [ "$(git branch --show-current)" != main ]; then
    printf '%s\n' '请先切换到 main 分支再发布笔记。' >&2
    exit 1
  fi
  git remote get-url origin >/dev/null || exit
  if [ -n "$(git diff --cached --name-only -- . ':!docs')" ]; then
    printf '%s\n' '暂存区里有站点配置等非笔记文件，请先单独处理这些改动。' >&2
    exit 1
  fi
  .venv/bin/python -m mkdocs build --strict || exit
  git add -A -- docs || exit
  if ! git diff --cached --quiet; then
    git commit -m "notes: $(date +%F)" || exit
  fi
  # 没有新改动也继续推送，以便重试上次网络失败的提交。
  git push -u origin main || exit
  printf '%s\n' '已推送，等待 GitHub Actions 更新网站。'
)
