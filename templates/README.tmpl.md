<div align="center">

# {{title}}

{{tagline}}

[![可用](https://img.shields.io/badge/可用-{{count_ok}}-brightgreen)](data/status.json)
[![检测时间](https://img.shields.io/badge/updated-{{updated_short}}-blue)](data/status.json)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**最近检测 {{updated}}** ｜ 可用 **{{count_alive}}** ｜ 正常 {{count_ok}} ｜ 限流 {{count_limited}} ｜ 已失效 {{count_dead}} ｜ 异常 {{count_error}} ｜ 共 {{count_total}}

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

{{key_table}}

**状态说明**：🟢 正常 ｜ 🟡 限流（额度用完，等重置）｜ 🔴 鉴权失败 ｜ ⚪ 上游错误 ｜ ⚫ 未检测

> Key 在上表里做了遮罩，完整值见 [`keys/keys.txt`](keys/keys.txt)。失效的 Key 会被移入 [`keys/archive/`](keys/archive/)，不删除、可追溯。

---

## 🎁 官方免费额度

以下都是**厂商自己的免费层**，自己注册、key 归自己，不会被别人用光，也不会突然跑路。想长期白嫖，优先用这些：

{{site_table}}

---

## 稳定通道

{{premium_block}}

{{ads_block}}

---

## ⚠️ 免责声明

- 本仓库所有 Key 均来自公开渠道或自有额度，**仅用于学习、测试、个人研究**，禁止商业使用、二次售卖、批量注册、模型训练。
- 免费 Key **随时可能失效、限流、被封**。本仓库不承诺可用性，不承担任何因使用导致的损失。
- 请勿在使用中提交隐私数据、商业机密、客户信息。免费通道的上游可能会记录请求内容用于改进服务。
- 使用第三方中转服务存在「降智」「掺水」「跑路」风险，**不要充值大额资金，不要绑定主账号**。
- 所有名称与入口归各自所有者，本仓库仅做索引。如有侵权，请开 Issue 联系删除。
{{disclaimer_extra}}

---

## 🤝 贡献

- 有新 Key / 新站点：直接开 Issue 或 PR，标题写清楚。
- 报告失效：附上表里的名称即可，不用贴完整 Key。
- 想长期免费：优先用上面「官方免费额度」里的厂商额度，那才是真正不会消失的。

<div align="center">

**如果这个仓库帮你省了钱，点个 ⭐ 就是最好的支持。**

<sub>自动生成于 {{updated}} ｜ 请勿手动编辑本文件</sub>

</div>
