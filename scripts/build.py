# -*- coding: utf-8 -*-
"""
从 data/sites.json 生成：
  - README.md           仓库主页（参考 panxunying/ai-coding-welfare 的排版风格）
  - docs/index.html     GitHub Pages 单页版
  - 邀请链接.txt         纯文本两列清单（站名 <TAB> 地址）
用法：python scripts/build.py
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "sites.json")

CHECKIN_LABEL = {
    "yes": ("✅", "有签到"),
    "no": ("➖", "无签到"),
    "limited": ("⚠️", "受限"),
    "unknown": ("❓", "待测"),
}


def load():
    with io.open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    d["sites"].sort(key=lambda s: s["host"].lower())
    return d


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_readme(d):
    sites = d["sites"]
    n = len(sites)
    yes = sum(1 for s in sites if s["checkin"] == "yes")

    link_row = " ·\n  ".join(
        '<a href="{u}"><b>{n}</b></a>'.format(u=s["url"], n=esc(s["name"])) for s in sites
    )

    rows = []
    for i, s in enumerate(sites, 1):
        icon, label = CHECKIN_LABEL[s["checkin"]]
        rows.append(
            "| {i} | **{name}** | {icon} {label} | {note} | [点此注册 →]({url}) | `{aff}` |".format(
                i=i, name=esc(s["name"]), icon=icon,
                label=label, note=s["note"], url=s["url"], aff=s["aff"],
            )
        )

    checkin_yes = [s for s in sites if s["checkin"] == "yes"]
    checkin_no = [s for s in sites if s["checkin"] == "no"]
    checkin_lim = [s for s in sites if s["checkin"] in ("limited", "unknown")]

    def bullet_list(items):
        if not items:
            return "（无）\n"
        return "".join(
            "- **{name}** — {note}\n".format(name=esc(s["name"]), note=s["note"])
            for s in items
        )

    return """<h1 align="center">AI 中转站福利导航</h1>

<p align="center">邀请链接合集 · 免费额度 · 白嫖 Claude / GPT / Gemini 的中转站</p>

<p align="center">
  <img src="https://img.shields.io/badge/%E6%94%B6%E5%BD%95%E7%AB%99%E7%82%B9-{n}%20%E4%B8%AA-blue" alt="收录站点">
  <img src="https://img.shields.io/badge/%E6%94%AF%E6%8C%81%E7%AD%BE%E5%88%B0-{yes}%20%E4%B8%AA-brightgreen" alt="支持签到">
  <img src="https://img.shields.io/badge/%E6%9E%B6%E6%9E%84-NewAPI%20%E4%B8%AD%E8%BD%AC-orange" alt="架构">
  <img src="https://img.shields.io/badge/%E6%9B%B4%E6%96%B0-{updated}-informational" alt="更新">
</p>

<p align="center">
  {link_row}
</p>

> [!TIP]
> **全部链接都是邀请链接**，走这些链接注册，站点给的邀请奖励才会算到你头上。所有站点均为第三方运营，请自行判断风险。

---

## 🚀 一分钟上车

| # | 站点 | 签到 | 说明 | 注册 | 邀请码 |
| :-: | :-- | :--: | :-- | :-: | :-: |
{rows}

> **签到**列：✅ 有每日签到 ｜ ➖ 未开签到功能 ｜ ⚠️ 有门槛/需人工过验证 ｜ ❓ 待实测。
>
> **说明**列为实测备注，随站点变动会过期，仅供参考。额度、模型、价格一律以站内实际为准。
>
> 收录 `{n}` 个站，其中 `{yes}` 个确认支持每日签到。数据更新：`{updated}`。

## 📖 怎么用

1. 点上表中的**邀请链接**注册（务必带上 `aff=` 参数，裸链拿不到邀请奖励）
2. 登录后台，在「令牌 / API Keys」里新建一个 Key
3. 客户端把 Base URL 填成 `https://<站点域名>/v1`，Key 填上一步的 Key

```bash
# 拉模型列表
curl -s https://<站点域名>/v1/models \\
  -H "Authorization: Bearer <你的KEY>"

# 对话测试
curl -s https://<站点域名>/v1/chat/completions \\
  -H "Authorization: Bearer <你的KEY>" \\
  -H "Content-Type: application/json" \\
  -d '{{"model":"<模型ID>","messages":[{{"role":"user","content":"只回复两个字：可用"}}],"max_tokens":40}}'
```

Claude Code / Codex CLI 之类的工具，把 `ANTHROPIC_BASE_URL` 或 `OPENAI_BASE_URL` 指向站点地址、`*_API_KEY` 填 Key 即可，协议基本都是 OpenAI 兼容。

## 🔍 站点分类

### ✅ 有每日签到（{yes} 个）

{checkin_yes}

### ➖ 未开签到（{no} 个）

{checkin_no}

### ⚠️ 受限 / 待实测（{lim} 个）

{checkin_lim}

## ⚠️ 免责声明

- 本仓库**仅做链接收集与实测记录**，与任何站点均无隶属或合作关系。
- 所有站点均为**第三方独立运营**，充值、额度、数据安全等风险请自行评估；本仓库不对任何站点的服务质量、存续时间作担保。
- 中转站可能随时跑路、改价、清库。**不要在其中存放敏感数据，也不要在多个站复用同一个密码**（撞库风险）。
- 收录不代表推荐。请遵守各站点自身的服务条款。

## 🙏 说明

- 数据源：`data/sites.json`，执行 `python scripts/build.py` 重新生成 README 与网页版。
- 网页版：<https://posstos.github.io/ai-relay-welfare/>
- 纯文本清单：`邀请链接.txt`
""".format(
        n=n, yes=yes, updated=d["updated"], link_row=link_row,
        rows="\n".join(rows),
        checkin_yes=bullet_list(checkin_yes),
        checkin_no=bullet_list(checkin_no),
        checkin_lim=bullet_list(checkin_lim),
        no=len(checkin_no), lim=len(checkin_lim),
    )


def build_html(d):
    sites = d["sites"]
    n = len(sites)
    yes = sum(1 for s in sites if s["checkin"] == "yes")

    cards = []
    for s in sites:
        icon, label = CHECKIN_LABEL[s["checkin"]]
        cls = s["checkin"]
        cards.append("""      <article class="card" data-checkin="{cls}" data-search="{srch}">
        <div class="card-head">
          <h3 class="card-title">{name}</h3>
          <span class="badge badge-{cls}">{icon} {label}</span>
        </div>
        <p class="note">{note}</p>
        <div class="aff-row"><span class="aff-label">邀请码</span><code class="aff">{aff}</code></div>
        <div class="actions">
          <a class="btn btn-primary" href="{url}" target="_blank" rel="noopener">注册</a>
          <button class="btn btn-ghost" type="button" data-copy="{url}">复制链接</button>
        </div>
      </article>""".format(
            cls=cls, icon=icon, label=label,
            srch=esc((s["name"] + " " + s["host"] + " " + s["aff"]).lower()),
            name=esc(s["name"]), host=s["host"], note=s["note"],
            aff=s["aff"], url=s["url"],
        ))

    tpl = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 中转站福利导航 · 邀请链接合集</title>
<meta name="description" content="AI 中转站邀请链接合集，__N__ 个站点，免费额度、签到福利一览。">
<style>
  :root {
    --bg: #f6f7f9;
    --panel: #ffffff;
    --text: #16181d;
    --muted: #6b7280;
    --line: #e4e6eb;
    --brand: #2f6df6;
    --brand-soft: #eaf1ff;
    --ok: #12805c;
    --ok-soft: #e6f6ef;
    --warn: #9a6400;
    --warn-soft: #fdf3e0;
    --off: #6b7280;
    --off-soft: #eef0f3;
    --radius: 12px;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #14161a;
      --panel: #1c1f26;
      --text: #e9ecf1;
      --muted: #9aa3b2;
      --line: #2b3038;
      --brand: #6f9dff;
      --brand-soft: #1e2b47;
      --ok: #4ed3a3;
      --ok-soft: #16302a;
      --warn: #f0b357;
      --warn-soft: #33291a;
      --off: #9aa3b2;
      --off-soft: #262a31;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font: 15px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
          "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .wrap { max-width: 1120px; margin: 0 auto; padding: 40px 20px 64px; }
  header.hero { text-align: center; margin-bottom: 28px; }
  header.hero h1 { margin: 0 0 10px; font-size: clamp(24px, 4vw, 34px); letter-spacing: -.3px; }
  header.hero p.sub { margin: 0 0 18px; color: var(--muted); font-size: 15px; }
  .stats { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 8px; }
  .stat {
    background: var(--panel); border: 1px solid var(--line); border-radius: 999px;
    padding: 6px 14px; font-size: 13px; color: var(--muted);
  }
  .stat b { color: var(--text); font-size: 14px; }
  .toolbar {
    display: flex; gap: 10px; flex-wrap: wrap; align-items: center;
    margin: 26px 0 18px;
  }
  .toolbar input[type=search] {
    flex: 1; min-width: 220px; padding: 10px 14px; font-size: 14px;
    color: var(--text); background: var(--panel);
    border: 1px solid var(--line); border-radius: 10px; outline: none;
  }
  .toolbar input[type=search]:focus { border-color: var(--brand); }
  .chips { display: flex; gap: 8px; flex-wrap: wrap; }
  .chip {
    padding: 8px 13px; font-size: 13px; cursor: pointer; user-select: none;
    background: var(--panel); border: 1px solid var(--line); border-radius: 999px;
    color: var(--muted); white-space: nowrap;
  }
  .chip[aria-pressed="true"] { background: var(--brand-soft); border-color: var(--brand); color: var(--brand); font-weight: 600; }
  .grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); }
  .card {
    display: flex; flex-direction: column; gap: 0;
    background: var(--panel); border: 1px solid var(--line);
    border-radius: var(--radius); padding: 16px 16px 14px;
  }
  .card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
  .card-title { margin: 0; font-size: 16px; font-weight: 650; }
  .badge {
    flex: none; font-size: 11px; padding: 3px 9px; border-radius: 999px;
    font-weight: 600; white-space: nowrap;
  }
  .badge-yes { background: var(--ok-soft); color: var(--ok); }
  .badge-no { background: var(--off-soft); color: var(--off); }
  .badge-limited { background: var(--warn-soft); color: var(--warn); }
  .badge-unknown { background: var(--off-soft); color: var(--off); }
  .host {
    margin: 5px 0 10px; font-size: 12px; color: var(--muted);
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    word-break: break-all;
  }
  .note { margin: 0 0 12px; font-size: 13px; color: var(--muted); flex: 1; }
  .aff-row { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
  .aff-label { font-size: 12px; color: var(--muted); }
  .aff {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 12px; background: var(--bg); border: 1px solid var(--line);
    padding: 2px 7px; border-radius: 6px; word-break: break-all;
  }
  .actions { display: flex; gap: 8px; }
  .btn {
    flex: 1; text-align: center; text-decoration: none; cursor: pointer;
    font-size: 13px; font-weight: 600; padding: 8px 12px; border-radius: 9px;
    border: 1px solid transparent; font-family: inherit;
  }
  .btn-primary { background: var(--brand); color: #fff; }
  .btn-primary:hover { filter: brightness(1.08); }
  .btn-ghost { background: transparent; border-color: var(--line); color: var(--muted); }
  .btn-ghost:hover { border-color: var(--brand); color: var(--brand); }
  .empty { padding: 48px 0; text-align: center; color: var(--muted); display: none; }
  footer {
    margin-top: 44px; padding-top: 22px; border-top: 1px solid var(--line);
    font-size: 13px; color: var(--muted);
  }
  footer p { margin: 0 0 8px; }
  footer .warn { color: var(--warn); }
  .toast {
    position: fixed; left: 50%; bottom: 28px; transform: translate(-50%, 20px);
    background: var(--text); color: var(--bg); font-size: 13px; font-weight: 600;
    padding: 9px 18px; border-radius: 999px; opacity: 0; pointer-events: none;
    transition: opacity .18s, transform .18s;
  }
  .toast.show { opacity: 1; transform: translate(-50%, 0); }
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>AI 中转站福利导航</h1>
    <p class="sub">邀请链接合集 · 免费额度 · 白嫖 Claude / GPT / Gemini 的中转站</p>
    <div class="stats">
      <span class="stat">收录 <b>__N__</b> 个站</span>
      <span class="stat">支持签到 <b>__YES__</b> 个</span>
      <span class="stat">更新 <b>__UPDATED__</b></span>
    </div>
  </header>

  <div class="toolbar">
    <input type="search" id="q" placeholder="搜站点 / 域名 / 邀请码…" autocomplete="off">
    <div class="chips" id="chips">
      <button class="chip" type="button" data-filter="all" aria-pressed="true">全部</button>
      <button class="chip" type="button" data-filter="yes" aria-pressed="false">✅ 有签到</button>
      <button class="chip" type="button" data-filter="no" aria-pressed="false">➖ 无签到</button>
      <button class="chip" type="button" data-filter="limited" aria-pressed="false">⚠️ 受限</button>
      <button class="chip" type="button" data-filter="unknown" aria-pressed="false">❓ 待测</button>
    </div>
  </div>

  <main class="grid" id="grid">
__CARDS__
  </main>
  <p class="empty" id="empty">没有匹配的站点</p>

  <footer>
    <p>全部链接均为<b>邀请链接</b>，走这些链接注册，站点给的邀请奖励才会算到你头上。</p>
    <p class="warn">⚠️ 所有站点均为第三方独立运营，可能随时跑路、改价、清库。不要存放敏感数据，不要在多个站复用同一密码。收录不代表推荐。</p>
    <p>数据源 <code>data/sites.json</code> ｜ 更新 __UPDATED__ ｜ <a href="https://github.com/posstos/ai-relay-welfare">GitHub 仓库</a></p>
  </footer>
</div>

<div class="toast" id="toast">已复制</div>

<script>
(function () {
  var grid = document.getElementById('grid');
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));
  var q = document.getElementById('q');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var empty = document.getElementById('empty');
  var toast = document.getElementById('toast');
  var filter = 'all';

  function apply() {
    var kw = q.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {
      var okKw = !kw || c.dataset.search.indexOf(kw) !== -1;
      var okF = filter === 'all' || c.dataset.checkin === filter;
      var show = okKw && okF;
      c.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    empty.style.display = shown ? 'none' : 'block';
  }

  q.addEventListener('input', apply);
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      filter = chip.dataset.filter;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      apply();
    });
  });

  var t;
  function flash(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(t);
    t = setTimeout(function () { toast.classList.remove('show'); }, 1400);
  }

  grid.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy]');
    if (!btn) return;
    var text = btn.dataset.copy;
    function done() { flash('邀请链接已复制'); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
    } else {
      fallback(text, done);
    }
  });

  function fallback(text, cb) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); cb(); } catch (err) { flash('复制失败，请手动复制'); }
    document.body.removeChild(ta);
  }
})();
</script>
</body>
</html>
"""
    return (tpl.replace("__N__", str(n))
               .replace("__YES__", str(yes))
               .replace("__UPDATED__", d["updated"])
               .replace("__CARDS__", "\n".join(cards)))


def build_txt(d):
    lines = []
    for s in d["sites"]:
        lines.append("{}\t{}".format(s["host"], s["url"]))
    return "\n".join(lines) + "\n"


def write(path, text):
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("  written: {} ({} bytes)".format(os.path.relpath(path, ROOT), len(text.encode("utf-8"))))


def main():
    d = load()
    print("sites: {}".format(len(d["sites"])))
    write(os.path.join(ROOT, "README.md"), build_readme(d))
    write(os.path.join(ROOT, "docs", "index.html"), build_html(d))
    write(os.path.join(ROOT, "邀请链接.txt"), build_txt(d))
    write(os.path.join(ROOT, "docs", ".nojekyll"), "")
    print("done.")


if __name__ == "__main__":
    main()
