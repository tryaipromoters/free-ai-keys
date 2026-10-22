#!/usr/bin/env python3
"""从 config.json / sites.json 渲染 README.md。仅标准库，无第三方依赖。

用法:
    python3 scripts/sync.py          # 渲染 README.md
    python3 scripts/sync.py --check  # 只检查配置是否合法，不写文件
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "config.json"
SITES_FILE = ROOT / "sites.json"
TEMPLATE_FILE = ROOT / "templates" / "README.tmpl.md"
README_FILE = ROOT / "README.md"


def load_json(path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate(cfg, sites):
    errors = []
    entries = (cfg.get("premium") or {}).get("entries") or []
    if (cfg.get("premium") or {}).get("enabled") and not entries:
        errors.append("config.json: premium.enabled 为 true 但 entries 为空")
    for i, e in enumerate(entries):
        if not e.get("url"):
            errors.append(f"config.json: premium.entries[{i}] 缺少 url")
    for i, s in enumerate(sites):
        if not s.get("url"):
            errors.append(f"sites.json: 第 {i + 1} 条缺少 url")
        if not s.get("name"):
            errors.append(f"sites.json: 第 {i + 1} 条缺少 name")
    return errors


def premium_block(cfg):
    p = cfg.get("premium") or {}
    if not p.get("enabled"):
        return ""
    entries = [e for e in (p.get("entries") or []) if e.get("url")]
    if not entries:
        return ""
    lines = []
    if p.get("highlight"):
        lines += [f"**{p['highlight']}**", ""]
    for e in entries:
        icon = "🌐" if e.get("needs_proxy") else "🌏"
        lines += [f"- {icon} **[{e.get('label') or '注册'} →]({e['url']})**"]
    lines.append("")
    if any(e.get("needs_proxy") for e in entries):
        lines += ["> 🌐 需**科学上网**才能打开｜🌏 全球 CDN 直连，无需代理", ""]
    return "\n".join(lines)


def deals_table(cfg, sites):
    """羊毛总表：本站 + 官方免费渠道，统一成一张表。"""
    rows = []
    p = cfg.get("premium") or {}
    if p.get("enabled") and p.get("entries"):
        proxy = any(e.get("needs_proxy") for e in p["entries"])
        urls = " ｜ ".join(
            f"[{'需魔法' if e.get('needs_proxy') else '直连'}]({e['url']})" for e in p["entries"]
        )
        rows.append(
            f"| **{p.get('name', '—')}** | {p.get('bonus', '—')} | {p.get('models', '—')} | "
            f"{'🌐 注册需代理' if proxy else '🌏 全球直连'} | {p.get('note', '—')} | {urls} |"
        )
    for s in sites:
        proxy = s.get("needs_proxy")
        access = "🌐 需代理" if proxy else ("🌏 全球直连" if proxy is False else "—")
        rows.append(
            f"| {s.get('name', '—')} | {s.get('free', '—')} | {s.get('models', '—')} | "
            f"{access} | {s.get('note', '—')} | [注册 →]({s.get('url', '#')}) |"
        )
    if not rows:
        return "> 暂无收录。\n"
    head = "| 名称 | 免费额度 | 支持模型 | 网络 | 备注 | 入口 |\n| :-- | :-- | :-- | :--: | :-- | :--: |\n"
    return head + "\n".join(rows) + "\n"


def ads_block(cfg):
    ads = cfg.get("ads") or []
    if not ads:
        return ""
    lines = ["## 赞助", ""]
    for ad in ads:
        title = ad.get("title", "")
        desc = ad.get("desc", "")
        url = ad.get("url", "#")
        lines.append(f"- **[{title}]({url})** — {desc}" if desc else f"- **[{title}]({url})**")
    lines.append("")
    return "\n".join(lines) + "\n"


def render(cfg, sites, now=None):
    if now is None:
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    values = {
        "title": cfg.get("title", "Free AI Token"),
        "tagline": cfg.get("tagline", ""),
        "repo_name": cfg.get("repo_name", "free-ai-keys"),
        "updated": now,
        "updated_short": now.split(" ")[0],
        "site_count": len(sites),
        "premium_block": premium_block(cfg),
        "deals_table": deals_table(cfg, sites),
        "ads_block": ads_block(cfg),
        "disclaimer_extra": cfg.get("disclaimer_extra", ""),
    }

    out = template
    for name, value in values.items():
        out = out.replace("{{" + name + "}}", str(value))
    out = re.sub(r"\{\{[a-z_]+\}\}", "", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="只校验配置，不写文件")
    args = parser.parse_args()

    cfg = load_json(CONFIG_FILE, {})
    sites = load_json(SITES_FILE, [])

    errors = validate(cfg, sites)
    for err in errors:
        print(f"[error] {err}", file=sys.stderr)
    if errors and args.check:
        return 1

    readme = render(cfg, sites)
    if args.check:
        print(f"[check] 配置合法：{len(sites)} 个官方渠道，"
              f"{len((cfg.get('premium') or {}).get('entries') or [])} 个领取入口")
        return 0

    README_FILE.write_text(readme, encoding="utf-8")
    print(f"[done] 已渲染 README.md：{len(sites)} 个官方渠道")
    return 0


if __name__ == "__main__":
    sys.exit(main())
