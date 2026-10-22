<div align="center">

# {{title}}

{{tagline}}

[![收录](https://img.shields.io/badge/收录-{{site_count}}%20%2B%201%20家-brightgreen)](sites.json)
[![更新](https://img.shields.io/badge/更新-{{updated_short}}-blue)](sites.json)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**不卖 Key，不搞套路。只是把「哪里能免费拿到 AI 额度」整理清楚。**

</div>

---

## 📌 最新羊毛

{{premium_block}}

---

## 🧾 全部免费渠道

{{deals_table}}

**怎么选？**

- **想立刻用、不想折腾** → 最上面几行，注册就能拿
- **想自己掌控、长期稳定** → 智谱 / 硅基流动 / Cloudflare，Key 归你自己
- **只是想试一下模型效果** → OVHcloud 和 LLM7 不用注册就能打

---

## ⚡ 5 分钟接上

拿到任意一个 Base URL + Key 后，所有主流工具都是同一套配法。

### 命令行验证

```bash
curl "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"hi"}]}'
```

### Python

```python
from openai import OpenAI

client = OpenAI(base_url="你的 Base URL", api_key="你的 Key")

resp = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

### 热门工具

这些是目前最主流的 AI 编程工具，都支持自定义 Base URL + Key：

| 工具 | 类型 | 说明 |
| :-- | :-- | :-- |
| **[OpenCode](https://opencode.ai)** | 终端 Agent | 最流行的开源终端编码 Agent，支持 75+ 家 provider，MIT |
| **[Claude Code](https://www.anthropic.com/claude-code)** | 终端 Agent | Anthropic 官方，agentic 能力最强 |
| **[Codex CLI](https://github.com/openai/codex)** | 终端 Agent | OpenAI 官方，OS 级沙箱，Apache-2.0 |
| **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** | 终端 Agent | Google 官方，免费层额度最大 |
| **[Cursor](https://cursor.com)** | IDE | AI 原生编辑器，日常写代码最顺手 |
| **[Cline](https://cline.bot)** | VS Code 插件 | 开源，支持任意 provider |
| **[Aider](https://github.com/Aider-AI/aider)** | 终端工具 | 老牌，git 集成紧密 |
| **[Cherry Studio](https://cherry-ai.com)** | 桌面客户端 | 国内主流，多模型切换方便 |
| **[LobeChat](https://lobehub.com)** | 桌面 / Web | 界面好看，插件生态丰富 |
| **[Open WebUI](https://openwebui.com)** | 自部署 Web | 团队内部用，私有化部署 |

> 所有工具填的都是「Base URL + API Key」这两项。

### 常用模型名

各家命名不完全一致，下面是当前主流模型：

| 模型 | 说明 |
| :-- | :-- |
| `deepseek-v4.1-flash` | DeepSeek 主力，1M 上下文，性价比极高 |
| `kimi-k3` | Moonshot，1M 上下文，agentic 强 |
| `glm-5.3` | 智谱，开源权重 |
| `gpt-6.1-sol` | OpenAI 旗舰 |
| `claude-opus-5.5` | Anthropic 旗舰 |
| `gemini-4-argon` | Google 旗舰 |

> 具体可用模型以各站点 `/models` 接口返回为准。

---

## ❓ 关于这个仓库

**这里是什么？**
一份持续维护的「免费 AI 额度」清单。所有条目都指向**官方或自营的注册页**，你注册后拿自己的 Key。

**为什么不直接发 Key？**
公开贴出来的 Key 几分钟内就会被爬虫扫走，等你打开时已经失效了。注册领取的 Key 是你自己的，不会被人抢。

**收录标准是什么？**
只收**能自己注册拿到 Key** 的渠道。不收来路不明的 Key 池，不收需要倒卖的账号。

**怎么判断哪个靠谱？**
优先官方免费层（智谱、Google、Groq 这类），它们不会突然跑路。中转站类的建议**不要充值大额、不要绑定主账号**。

**发现信息过时？**
开 Issue 或 PR，附上官方页面链接。核实后会更新。

---

## ⚠️ 免责声明

- 本仓库仅做信息汇总，**不运营、不担保**任何第三方服务。
- 免费额度、规则、可用性**随时可能变化**，以站点实时页面为准。
- 请勿用于商业转售、批量注册、模型训练等违反上游条款的用途。
- 免费通道的上游可能记录请求内容，**不要提交隐私或商业机密**。
{{disclaimer_extra}}

---

<div align="center">

**如果这个仓库帮你省了钱，点个 ⭐ 就是最好的支持。**

<sub>由 scripts/sync.py 生成 ｜ 请勿手动编辑本文件</sub>

</div>
