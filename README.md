<div align="center">

# Free AI Keys

每日检测的免费 AI API Key，失效即删

[![可用](https://img.shields.io/badge/可用-0-brightgreen)](data/status.json)
[![检测时间](https://img.shields.io/badge/updated-2026-10-22-blue)](data/status.json)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**最近检测 2026-10-22 11:29 UTC** ｜ 可用 **0** ｜ 正常 0 ｜ 限流 0 ｜ 已失效 0 ｜ 异常 0 ｜ 共 0

<sub>每日自动探活。失效即删，不保留死链。</sub>

</div>

---

## ⚡ 三行接入

```bash
export OPENAI_BASE_URL="https://api.example.com/v1"
export OPENAI_API_KEY="sk-此处换成下表所属的-key"
```

```python
from openai import OpenAI

client = OpenAI(base_url="https://api.example.com/v1", api_key="sk-...")
print(client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "hi"}],
).choices[0].message.content)
```

兼容任何接受 `baseURL` + `apiKey` 的工具：Cursor、Cline、Aider、Open WebUI、LobeChat、Chatbox、NextChat 等。

> 注意：**Base URL 与 Key 必须配套**。A 站的 Key 发给 B 站地址只会 401。

---

## 🔑 今日 Key

> 暂无 Key。把 key 粘进 `keys/keys.txt` 后运行 `python3 scripts/sync.py`。

**状态说明**：🟢 正常 ｜ 🟡 限流（额度用完，等重置）｜ 🔴 鉴权失败 ｜ ⚪ 上游错误 ｜ ⚫ 未检测

> Key 在上表里做了遮罩，完整值见 [`keys/keys.txt`](keys/keys.txt)。失效的 Key 会被移入 [`keys/archive/`](keys/archive/)，不删除、可追溯。

---

## 🎁 官方免费额度

以下都是**厂商自己的免费层**，自己注册、key 归自己，不会被别人用光，也不会突然跑路。想长期白嫖，优先用这些：

| 名称 | 免费额度 | 模型 | 网络 | 备注 | 入口 |
| :-- | :-- | :-- | :--: | :-- | :--: |
| 智谱 BigModel | GLM-4-Flash 系列长期免费 | GLM-4-Flash / GLM-4V-Flash | 🌏 全球直连 | 国内直连，注册即用 | [注册 →](https://bigmodel.cn/) |
| 硅基流动 SiliconFlow | 多款小参数模型免费 | Qwen / GLM / DeepSeek 部分型号 | 🌏 全球直连 | 国内直连，OpenAI 兼容 | [注册 →](https://cloud.siliconflow.cn/) |
| GitHub Models | GitHub 账号免费调用，按天限次 | GPT / Llama / Phi / Mistral | 🌐 需代理 | 有 GitHub 账号即可，适合测试 | [注册 →](https://github.com/marketplace/models) |
| Google AI Studio | Gemini 免费层，按天限次 | Gemini 全系 | 🌐 需代理 | 额度较宽，需代理 | [注册 →](https://aistudio.google.com/apikey) |
| Groq | 免费层限速，不限量 | Llama / Qwen / Kimi | 🌐 需代理 | 速度极快，适合低延迟场景 | [注册 →](https://console.groq.com/keys) |
| OpenRouter | 带 :free 后缀的模型免费 | 多家中转，型号最全 | 🌐 需代理 | 一个 key 打通多家上游 | [注册 →](https://openrouter.ai/keys) |
| Cloudflare Workers AI | 每日免费 neuron 额度 | Llama / Qwen / Mistral | 🌏 全球直连 | 需部署 Worker 转发，全球可用 | [注册 →](https://dash.cloudflare.com/) |
| Mistral | 免费实验层 | Mistral / Codestral | 🌐 需代理 | Codestral 适合写代码 | [注册 →](https://console.mistral.ai/api-keys/) |

---

## 稳定通道

免费 Key 日抛且限流。需要稳定、不限速、支持 Claude Code / Codex 的通道，用下面这个：

- **接口地址**：`https://api.tryaigc.cn/v1`
  <sub>接口走全球 CDN，调用不需要代理</sub>
- **注册入口**：**[TryAPI →](https://tryapi.tryai.chat/register?aff=TZ9VWQV8ZHED)**

> ⚠️ 注册页需**科学上网**（魔法）才能打开；接口地址走全球 CDN，调用无需代理。

---

## ⚠️ 免责声明

- 本仓库所有 Key 均来自公开渠道或自有额度，**仅用于学习、测试、个人研究**，禁止商业使用、二次售卖、批量注册、模型训练。
- 免费 Key **随时可能失效、限流、被封**。本仓库不承诺可用性，不承担任何因使用导致的损失。
- 请勿在使用中提交隐私数据、商业机密、客户信息。免费通道的上游可能会记录请求内容用于改进服务。
- 使用第三方中转服务存在「降智」「掺水」「跑路」风险，**不要充值大额资金，不要绑定主账号**。
- 所有名称与入口归各自所有者，本仓库仅做索引。如有侵权，请开 Issue 联系删除。

---

## 🤝 贡献

- 有新 Key / 新站点：直接开 Issue 或 PR，标题写清楚。
- 报告失效：附上表里的名称即可，不用贴完整 Key。
- 想长期免费：优先用上面「官方免费额度」里的厂商额度，那才是真正不会消失的。

<div align="center">

**如果这个仓库帮你省了钱，点个 ⭐ 就是最好的支持。**

<sub>自动生成于 2026-10-22 11:29 UTC ｜ 请勿手动编辑本文件</sub>

</div>
