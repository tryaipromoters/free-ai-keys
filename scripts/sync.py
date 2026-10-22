#!/usr/bin/env python3
"""探活 keys/keys.txt 并重新渲染 README。仅标准库，无第三方依赖。

用法:
    python3 scripts/sync.py            # 探活 + 写 README / data/status.json
    python3 scripts/sync.py --offline  # 不联网，只用上次结果重新渲染
    python3 scripts/sync.py --prune    # 探活后把失效的移到 keys/archive/
"""

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYS_FILE = ROOT / "keys" / "keys.txt"
ARCHIVE_DIR = ROOT / "keys" / "archive"
STATUS_FILE = ROOT / "data" / "status.json"
CONFIG_FILE = ROOT / "config.json"
TEMPLATE_FILE = ROOT / "templates" / "README.tmpl.md"
SITES_FILE = ROOT / "sites.json"
README_FILE = ROOT / "README.md"

FIELDS = ("name", "base_url", "model", "key", "note", "probe")

MASK_HINT = "（Key 见 keys/keys.txt）"


def load_config():
    if not CONFIG_FILE.exists():
        return {}
    with CONFIG_FILE.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_sites():
    if not SITES_FILE.exists():
        return []
    with SITES_FILE.open(encoding="utf-8") as fh:
        return json.load(fh)


def parse_keys(path):
    """解析 keys.txt，返回 (entries, errors)。空行和注释行跳过。"""
    entries, errors = [], []
    if not path.exists():
        return entries, errors
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            errors.append(f"keys.txt:{lineno} 字段不足 4 个，已跳过")
            continue
        item = dict(zip(FIELDS, parts + [""] * (len(FIELDS) - len(parts))))
        if not item["key"]:
            errors.append(f"keys.txt:{lineno} Key 为空，已跳过")
            continue
        if item["probe"] not in ("", "auto", "models", "chat", "none"):
            item["probe"] = "auto"
        entries.append(item)
    return entries, errors


def http_json(url, key, timeout):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {key}",
            "User-Agent": "free-ai-keys-probe/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8", "replace"))


def http_chat(base_url, model, key, timeout, max_tokens):
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model or "gpt-4o-mini",
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": max_tokens,
            "stream": False,
        }
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "free-ai-keys-probe/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        resp.read()
        return resp.status


def classify(exc):
    """把异常归类成 (status, reason)，便于 README 里统计。"""
    if isinstance(exc, urllib.error.HTTPError):
        code = exc.code
        if code in (401, 403):
            return "dead", f"HTTP {code} 鉴权失败"
        if code == 429:
            return "limited", "HTTP 429 限流"
        if code == 404:
            return "dead", "HTTP 404 接口不存在"
        if code >= 500:
            return "error", f"HTTP {code} 上游错误"
        return "error", f"HTTP {code}"
    if isinstance(exc, urllib.error.URLError):
        return "error", f"连接失败：{exc.reason}"
    if isinstance(exc, TimeoutError):
        return "error", "超时"
    return "error", type(exc).__name__


def probe_one(entry, cfg):
    """返回 {status, reason, latency_ms}。status: ok / limited / dead / error / skipped"""
    probe_cfg = cfg.get("probe", {})
    timeout = probe_cfg.get("timeout", 12)
    max_tokens = probe_cfg.get("chat_max_tokens", 1)
    mode = entry.get("probe") or probe_cfg.get("mode", "auto")
    base = entry["base_url"].rstrip("/")

    if mode == "none":
        return {"status": "skipped", "reason": "未检测", "latency_ms": None}

    started = dt.datetime.now(dt.timezone.utc)
    order = ["models", "chat"] if mode == "auto" else [mode]
    last = {"status": "error", "reason": "未检测", "latency_ms": None}

    for step in order:
        try:
            if step == "models":
                http_json(base + "/models", entry["key"], timeout)
            else:
                http_chat(base, entry["model"], entry["key"], timeout, max_tokens)
            elapsed = int((dt.datetime.now(dt.timezone.utc) - started).total_seconds() * 1000)
            return {"status": "ok", "reason": "正常", "latency_ms": elapsed}
        except Exception as exc:  # noqa: BLE001 - 探活需要吞掉所有异常
            status, reason = classify(exc)
            elapsed = int((dt.datetime.now(dt.timezone.utc) - started).total_seconds() * 1000)
            last = {"status": status, "reason": reason, "latency_ms": elapsed}
            if status == "dead" and isinstance(exc, urllib.error.HTTPError) and exc.code in (401, 403):
                return last
            if status == "dead":
                continue
    return last


def probe_all(entries, cfg):
    workers = max(1, int(cfg.get("probe", {}).get("workers", 8)))
    results = {}
    if not entries:
        return results
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(probe_one, e, cfg): e["key"] for e in entries}
        for fut in concurrent.futures.as_completed(futures):
            key = futures[fut]
            try:
                results[key] = fut.result()
            except Exception as exc:  # noqa: BLE001
                results[key] = {"status": "error", "reason": type(exc).__name__, "latency_ms": None}
    return results


def mask(key):
    if len(key) <= 10:
        return key[:3] + "***"
    return f"{key[:6]}…{key[-4:]}"


def load_previous():
    if not STATUS_FILE.exists():
        return {}
    try:
        with STATUS_FILE.open(encoding="utf-8") as fh:
            data = json.load(fh)
        return {row["masked"]: row for row in data.get("results", [])}
    except (json.JSONDecodeError, KeyError):
        return {}


def build_rows(entries, results):
    rows = []
    for entry in entries:
        res = results.get(entry["key"]) or {
            "status": "error",
            "reason": "未检测",
            "latency_ms": None,
        }
        rows.append(
            {
                "name": entry["name"],
                "base_url": entry["base_url"],
                "model": entry["model"],
                "note": entry["note"],
                "masked": mask(entry["key"]),
                "status": res["status"],
                "reason": res["reason"],
                "latency_ms": res["latency_ms"],
            }
        )
    return rows


def archive_dead(entries, rows):
    """把 dead 的 key 从 keys.txt 移到 keys/archive/YYYY-MM.txt。返回移动数量。"""
    dead_masked = {r["masked"] for r in rows if r["status"] == "dead"}
    if not dead_masked:
        return 0
    dead = {e["key"] for e in entries if mask(e["key"]) in dead_masked}
    if not dead:
        return 0
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m")
    archive_path = ARCHIVE_DIR / f"{stamp}.txt"
    moved_lines = []
    kept = []
    for line in KEYS_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            kept.append(line)
            continue
        parts = [p.strip() for p in stripped.split("|")]
        if len(parts) >= 4 and parts[3] in dead:
            moved_lines.append(f"# {dt.datetime.now(dt.timezone.utc).date()} 失效：{parts[4] if len(parts) > 4 else ''}")
            moved_lines.append(stripped)
        else:
            kept.append(line)
    if not moved_lines:
        return 0
    with archive_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(moved_lines) + "\n")
    KEYS_FILE.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8")
    return len(moved_lines) // 2


def render(sites, cfg, rows, offline):
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    alive = [r for r in rows if r["status"] in ("ok", "limited")]
    ok = [r for r in rows if r["status"] == "ok"]
    dead = [r for r in rows if r["status"] == "dead"]
    errors = [r for r in rows if r["status"] == "error"]
    skipped = [r for r in rows if r["status"] == "skipped"]

    template = TEMPLATE_FILE.read_text(encoding="utf-8") if TEMPLATE_FILE.exists() else ""

    def key_table():
        if not rows:
            return "> 暂无 Key。把 key 粘进 `keys/keys.txt` 后运行 `python3 scripts/sync.py`。\n"
        head = "| 状态 | 名称 | 模型 | Base URL | Key | 延迟 |\n| :--: | :-- | :-- | :-- | :-- | --: |\n"
        icon = {"ok": "🟢", "limited": "🟡", "dead": "🔴", "error": "⚪", "skipped": "⚫"}
        body = []
        for r in rows:
            latency = f"{r['latency_ms']} ms" if r["latency_ms"] is not None else "—"
            note = f"<br><sub>{r['reason']}</sub>" if r["status"] not in ("ok",) else ""
            body.append(
                f"| {icon.get(r['status'], '⚪')} | {r['name']}{note} | `{r['model'] or '—'}` | "
                f"`{r['base_url']}` | `{r['masked']}` | {latency} |"
            )
        return head + "\n".join(body) + "\n"

    def site_table():
        if not sites:
            return "> 暂无收录。编辑 `sites.json` 添加。\n"
        head = "| 名称 | 免费额度 | 模型 | 网络 | 备注 | 入口 |\n| :-- | :-- | :-- | :--: | :-- | :--: |\n"
        body = []
        for s in sites:
            proxy = s.get("needs_proxy")
            access = "🌐 需代理" if proxy else ("🌏 全球直连" if proxy is False else "—")
            body.append(
                f"| {s.get('name', '—')} | {s.get('free', '—')} | {s.get('models', '—')} | "
                f"{access} | {s.get('note', '—')} | [注册 →]({s.get('url', '#')}) |"
            )
        return head + "\n".join(body) + "\n"

    def premium_block():
        p = cfg.get("premium", {})
        if not p.get("enabled"):
            return ""
        entries = p.get("entries") or []
        if not entries and p.get("url"):
            entries = [{"label": "注册入口", "url": p["url"], "needs_proxy": p.get("needs_proxy")}]
        entries = [e for e in entries if e.get("url")]
        if not entries:
            print("[warn] config.json 的 premium.enabled 为 true 但没有可用入口（premium.entries / premium.url 均为空）", file=sys.stderr)
            return ""
        lines = []
        if p.get("offer"):
            lines.append(p["offer"])
            lines.append("")
        for e in entries:
            icon = "🌐" if e.get("needs_proxy") else "🌏"
            lines.append(f"- {icon} **[{e.get('label') or '注册'} →]({e['url']})**")
        lines.append("")
        if any(e.get("needs_proxy") for e in entries):
            lines.append("> 🌐 需**科学上网**（魔法）｜🌏 全球直连，无需代理")
            lines.append("")
        return "\n".join(lines)

    def ads_block():
        ads = cfg.get("ads") or []
        if not ads:
            return ""
        lines = ["## 赞助", ""]
        for ad in ads:
            title = ad.get("title", "")
            url = ad.get("url", "#")
            desc = ad.get("desc", "")
            lines.append(f"- **[{title}]({url})** — {desc}" if desc else f"- **[{title}]({url})**")
        lines.append("")
        return "\n".join(lines)

    stats = {
        "updated": now,
        "updated_short": now.split(" ")[0],
        "total": len(rows),
        "ok": len(ok),
        "limited": len(alive) - len(ok),
        "dead": len(dead),
        "error": len(errors),
        "skipped": len(skipped),
        "offline": offline,
    }

    values = {
        "title": cfg.get("title", "Free AI Keys"),
        "tagline": cfg.get("tagline", ""),
        "repo_name": cfg.get("repo_name", "free-ai-keys"),
        "updated": now,
        "updated_short": now.split(" ")[0],
        "count_total": len(rows),
        "count_ok": len(ok),
        "count_limited": len(alive) - len(ok),
        "count_alive": len(alive),
        "count_dead": len(dead),
        "count_error": len(errors),
        "count_skipped": len(skipped),
        "key_table": key_table(),
        "site_table": site_table(),
        "premium_block": premium_block(),
        "ads_block": ads_block(),
        "disclaimer_extra": cfg.get("disclaimer_extra", ""),
    }

    if template:
        out = template
        for name, value in values.items():
            out = out.replace("{{" + name + "}}", str(value))
        out = re.sub(r"\{\{[a-z_]+\}\}", "", out)
        out = re.sub(r"\n{3,}", "\n\n", out)
    else:
        out = f"# {values['title']}\n\n{values['tagline']}\n\n{values['key_table']}"

    return out, stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="不联网，复用上次探活结果")
    parser.add_argument("--prune", action="store_true", help="把失效 key 移到 keys/archive/")
    args = parser.parse_args()

    cfg = load_config()
    entries, errors = parse_keys(KEYS_FILE)
    for err in errors:
        print(f"[warn] {err}", file=sys.stderr)

    previous = load_previous()
    if args.offline:
        results = {}
        for e in entries:
            prev = previous.get(mask(e["key"]), {})
            results[e["key"]] = {
                "status": prev.get("status", "skipped"),
                "reason": prev.get("reason", "离线渲染"),
                "latency_ms": prev.get("latency_ms"),
            }
        print(f"[offline] 复用上次结果，共 {len(entries)} 条")
    else:
        print(f"[probe] 正在检测 {len(entries)} 条…")
        results = probe_all(entries, cfg)

    rows = build_rows(entries, results)

    if args.prune:
        moved = archive_dead(entries, rows)
        if moved:
            entries, _ = parse_keys(KEYS_FILE)
            rows = build_rows(entries, results)
        print(f"[prune] 归档 {moved} 条失效 Key")

    readme, stats = render(load_sites(), cfg, rows, args.offline)
    README_FILE.write_text(readme, encoding="utf-8")

    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATUS_FILE.open("w", encoding="utf-8") as fh:
        json.dump({"stats": stats, "results": rows}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print(
        f"[done] 总计 {stats['total']}｜可用 {stats['ok']}｜限流 {stats['limited']}"
        f"｜失效 {stats['dead']}｜异常 {stats['error']}"
    )


if __name__ == "__main__":
    main()
