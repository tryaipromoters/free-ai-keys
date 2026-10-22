<div align="center">

# {{title}}

{{tagline}}

[![每日签到](https://img.shields.io/badge/签到-$0.1%20–%20$0.3%20%2F%20天-brightgreen)](https://tryapi.tryai.chat/register?aff=TZ9VWQV8ZHED)
[![7天大奖](https://img.shields.io/badge/第7天-$3%20–%20$5-blue)](https://tryapi.tryai.chat/register?aff=TZ9VWQV8ZHED)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**不用挑 Key，不用等更新。注册 → 签到 → 直接用。**

</div>

---

## 🎁 免费领取

{{premium_block}}

---

## ⚡ 三步跑通

**1. 注册**（上面任一入口，两个是同一个站）

**2. 签到领额度**

登录后打开「签到」，领当天额度。

**3. 换上 Base URL 直接用**

```bash
export OPENAI_BASE_URL="https://api.tryai.chat/v1"
export OPENAI_API_KEY="sk-你的key"
```

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.tryai.chat/v1",
    api_key="sk-你的key",
)

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

兼容任何接受 `baseURL` + `apiKey` 的工具：**Cursor / Cline / Aider / Claude Code / Codex / Open WebUI / LobeChat / Chatbox / NextChat** 等，填 Base URL 和 Key 即可。

---

## 📅 签到规则

| 天 | 额度 |
| :--: | :-- |
| 第 1–6 天 | **$0.1 – $0.3** 随机（每天一次） |
| **第 7 天** | **$3 – $5** 终极大奖 |
| 第 8 天 | 回到第 1 天，重新循环 |

**三条规则要知道：**

1. **每天必须先成功调用 1 次，才能签当天的到。** 白嫖党进不来，额度留给真用的人。
2. **断签会重置进度。** 第 7 天的大奖只有连续签满 7 天才能拿到，中途断了就从头开始。
3. **额度是平台额度，用完即止**，可以用于上游所有支持的模型（Claude / GPT / Gemini / DeepSeek / Grok / Qwen 等）。

> 实际到账金额是**加权随机**的：多数情况落在低区间，偶尔会高于预期。写「$0.1–$0.3」是区间，不是均值。

---

## 🔌 官方免费额度（16 家）

不想依赖任何中转？以下都是**厂商自己的免费层**，Key 归你自己，不会被别人用光，也不会突然跑路：

{{site_table}}

{{ads_block}}
---

## ❓ 常见问题

**Q：签到提示「今日未满足条件」？**
A：你今天还没成功调用过。先随便发一个请求（哪怕 1 个 token），再来签到。

**Q：额度用完了怎么办？**
A：等明天签到，或者充值。仓库里剩下的官方免费渠道也可以直接用。

**Q：为什么注册要科学上网？**
A：注册页在海外。接口本身走全球 CDN，**日常调用不需要代理**。

**Q：Key 会过期吗？**
A：不会。签到给的是余额，不消耗时间，只消耗额度。

**Q：上游会看到我的数据吗？**
A：会。免费通道的上游可能记录请求内容用于改进服务，**不要提交隐私或商业机密**。

---

## ⚠️ 免责声明

- 本仓库仅做信息汇总与入口索引，不运营、不担保任何第三方服务。
- 免费额度、规则、可用性**随时可能变化**，以站点实时页面为准。
- 请勿用于商业转售、批量注册、模型训练等违反上游条款的用途。
- 使用第三方中转存在「降智」「掺水」「跑路」风险，**不要充值大额资金，不要绑定主账号**。
{{disclaimer_extra}}

---

## 🤝 贡献

- 发现新的官方免费渠道：开 PR，附上**官方文档链接**和额度说明。
- 报告额度/规则变化：开 Issue，写清楚哪一条不对。
- 只收**能自己注册拿到 key 的官方渠道**，不收来路不明的 key 池。

<div align="center">

**如果这个仓库帮你省了钱，点个 ⭐ 就是最好的支持。**

<sub>由 scripts/sync.py 生成 ｜ 请勿手动编辑本文件</sub>

</div>
