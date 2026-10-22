<div align="center">

# {{title}}

{{tagline}}

[![注册送$5](https://img.shields.io/badge/注册送-$5-brightgreen)](https://tryapi.tryai.chat/register?aff=TZ9VWQV8ZHED)
[![每日签到](https://img.shields.io/badge/每日还能-签到-blue)](https://tryapi.tryai.chat/register?aff=TZ9VWQV8ZHED)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

**不用挑 Key，不用等更新。注册 → 直接能用。**

</div>

---

## 🎁 免费领取

{{premium_block}}

---

## ⚡ 三步跑通

**1. 注册**（上面任一入口，两个是同一个站）→ 立刻到账 **$5**

**2. 拿 Key**

登录后进控制台，复制你的 API Key。

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

## 📅 每天还能签到

注册之后，**每天登录签到**还能再领一笔免费额度。

- 连续签到有累计奖励，**第 7 天额外给一份大奖**
- 中途断了会重新计算
- 额度是平台额度，可用于上游所有支持的模型（Claude / GPT / Gemini / DeepSeek / Grok / Qwen 等）

具体金额以站内显示为准。

---

## 🔌 官方免费额度（16 家）

不想依赖任何中转？以下都是**厂商自己的免费层**，Key 归你自己，不会被别人用光，也不会突然跑路：

{{site_table}}

{{ads_block}}
---

## ❓ 常见问题

**Q：额度用完了怎么办？**
A：等明天签到，或者充值。仓库里剩下的官方免费渠道也可以直接用。

**Q：为什么注册要科学上网？**
A：注册页在海外。接口本身走全球 CDN，**日常调用不需要代理**。

**Q：额度会过期吗？**
A：不会。注册送的 $5 和签到领的额度都不消耗时间，用完为止。

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
