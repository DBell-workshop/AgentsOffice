<p align="center">
  <a href="README_zh-CN.md">简体中文</a> ·
  <a href="README_zh-TW.md">繁體中文</a> ·
  <a href="README.md">English</a> ·
  <a href="README_ja.md">日本語</a>
</p>

<p align="center">
  <img src="docs/images/demo.gif" width="800" alt="AgentFleet Demo" />
</p>

<h1 align="center">AgentFleet</h1>

<p align="center">
  <strong>给你的 AI 团队一间看得见的办公室</strong><br/>
  <sub>像素风 RPG 多 Agent 协作工作台</sub>
</p>

<p align="center">
  <a href="https://github.com/DBell-workshop/AgentFleet/stargazers"><img src="https://img.shields.io/github/stars/DBell-workshop/AgentFleet?style=social" alt="Stars" /></a>
  <a href="https://github.com/DBell-workshop/AgentFleet/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSL_1.1-blue" alt="License" /></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.9+-green" alt="Python" /></a>
  <a href="#"><img src="https://img.shields.io/badge/frontend-React%20%2B%20Phaser3-purple" alt="Frontend" /></a>
  <a href="https://github.com/DBell-workshop/AgentFleet/releases/latest"><img src="https://img.shields.io/badge/下载-macOS%20DMG-blue" alt="Download" /></a>
</p>

<p align="center">
  <a href="#screenshots">截图</a> ·
  <a href="#features">功能</a> ·
  <a href="#quick-start">快速开始</a> ·
  <a href="#pro-vs-lite">Pro vs Lite</a> ·
  <a href="#support">支持我们</a>
</p>

---

## AgentFleet 是什么？

AgentFleet 是一个**多 Agent 协作工作台**，用像素风 RPG 办公室让你的 AI 团队"可视化地上班"。

定义角色、写提示词、选择场景 —— 几分钟就能搭建属于你的 AI 数字员工团队。

> **和其他"像素办公室"项目不同：我们的 Agent 不只是会走来走去的小人，它们真的在干活。**

| 其他项目 | AgentFleet |
|---------|-------------|
| 纯可视化看板，展示 Agent 状态 | **完整的 AI 工作台**，Agent 有真实协作能力 |
| 需要外接其他 AI 工具才能工作 | **自带 LLM 对话 + 委托引擎**，开箱即用 |
| 单角色演示 | **多角色团队协作**，项目经理自动分配任务 |
| 只能看 | **对话、委托任务、实时跟踪进度** |

---

<a id="screenshots"></a>
## 截图

> 截图来自 **AgentFleet Pro**。Lite（开源版）包含核心像素办公室、Agent 对话和场景系统。

<table>
<tr>
<td width="50%"><img src="docs/images/screenshots/scene-selector.png" alt="场景选择" /><br/><sub>6 个预设场景模板：电商运营、自媒体工作室、客服中心、开发团队、游戏工作室、量化交易</sub></td>
<td width="50%"><img src="docs/images/screenshots/dashboard-dark.png" alt="深色大屏" /><br/><sub>实时运营大屏：Token 用量、成本追踪、Agent 活动监控</sub></td>
</tr>
<tr>
<td><img src="docs/images/screenshots/dashboard-light.png" alt="浅色大屏" /><br/><sub>浅色主题大屏：委托漏斗、模型用量分布</sub></td>
<td><img src="docs/images/screenshots/onboarding-scenes.png" alt="新手引导" /><br/><sub>引导式上手：选择场景，立即开始工作</sub></td>
</tr>
</table>

---

<a id="features"></a>
## 功能

### 🏢 像素风 RPG 办公室
基于 Phaser 3 游戏引擎 —— 2D 像素办公室，每个 Agent 有自己的工位、房间和动画。看它们走动、打字、庆祝。

### 🎭 场景系统
切换预设场景模板，一键重新配置整个团队：
- **自媒体工作室** —— 文案编辑、视频剪辑师、运营策划、美工设计
- **电商运营中心** —— 数据工程师、数据产品经理、运营策划
- **客服中心** —— 接待、投诉处理、跟进回访
- **开发团队、游戏工作室、量化交易**等更多场景

每个场景拥有独立的 Agent 团队、聊天记录和委托记录 —— 完全隔离。

### 🤖 灵活的 Agent 系统
- **无限 Agent**：按需创建任意角色
- **单独模型配置**：每个 Agent 可选择不同的 LLM（Gemini、Claude、GPT、DeepSeek、Qwen）
- **20 个像素角色**外观可选
- **桌面宠物猫咪**随 Agent 工作状态变化（12 种品种！）

### 💬 智能对话
- **群聊**：项目经理自动识别意图并分配给合适的 Agent
- **私聊**：与特定 Agent 一对一深入对话
- **圆桌讨论**：多个 Agent 围绕复杂话题协作讨论

### 📋 委托系统（Pro）
一句话说出需求，AI 团队自动规划并执行：
1. 你说："帮我写一份自媒体运营方案"
2. 项目经理创建 6 步执行计划
3. 团队自动逐步执行
4. 你实时看到每一步的进度更新

### 📊 运营大屏（Pro）
实时监控：Token 用量、成本追踪、Agent 活动、委托漏斗。

### 🐱 桌面宠物
像素猫咪伙伴，住在独立窗口中：
- **待机** —— 呼吸动画
- **打字** —— Agent 工作时的 bongo cat 动画
- **庆祝** —— 任务完成时的星星粒子特效
- **12 种品种** —— 双击切换

---

<a id="quick-start"></a>
## 快速开始

### 桌面应用（推荐）

从 [Releases](https://github.com/DBell-workshop/AgentFleet/releases/latest) 下载最新 DMG：

1. 下载 `AgentFleet_x.x.x_aarch64.dmg`（macOS Apple Silicon）
2. 拖入 Applications
3. 启动 —— 像素风 Loading 页面会在后端启动时显示
4. 在设置中配置 API Key，即可开始对话

> DMG 已通过 Apple 签名和公证 —— 安装零警告。

### 开发模式

```bash
git clone https://github.com/DBell-workshop/AgentFleet.git
cd AgentFleet

# 后端
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_server.py

# 前端（另开终端）
cd frontend && npm install && npm run dev
```

访问 **http://localhost:8000/static/office/**

### Docker

```bash
cp .env.example .env   # 至少添加一个 LLM API Key
docker compose up -d
```

---

<a id="pro-vs-lite"></a>
## Pro vs Lite

| 功能 | Lite（开源版） | Pro |
|------|:------------:|:---:|
| 像素风 RPG 办公室 | ✅ | ✅ |
| Agent 对话（群聊 + 私聊） | ✅ | ✅ |
| 场景模板 | ✅ | ✅ |
| Agent 配置面板 | ✅ | ✅ |
| 圆桌讨论 | ✅ | ✅ |
| 桌面宠物猫咪 | ✅ | ✅ |
| 委托系统 | - | ✅ |
| 运营大屏 | - | ✅ |
| CLI 集成（Claude/Codex） | - | ✅ |
| 桌面应用（Tauri） | - | ✅ |
| 电商报表 Pack | - | ✅ |

> 本仓库为 **Lite** 版。截图中的 Pro 功能仅作展示用途。
>
> 对 Pro 感兴趣？访问 [linkos.cc](https://linkos.cc) 或加入社区。

---

---

## 路线图

- [x] 像素风 RPG 办公室 + Agent 动画
- [x] 场景系统 + 隔离的 Agent 和聊天记录
- [x] 群聊调度 + 私聊 + 圆桌讨论
- [x] 桌面宠物猫咪（12 种品种）
- [x] LLM 成本追踪
- [x] 委托系统 / 运营大屏 / macOS 桌面应用（Pro）
- [ ] Windows / Linux 桌面应用
- [ ] 移动端响应式布局
- [ ] 更多场景模板

---

<a id="support"></a>
## 支持这个项目

**⭐ [Star 这个仓库](https://github.com/DBell-workshop/AgentFleet)** —— 最简单的支持方式

---

## 社区

<p align="center">
  <a href="https://discord.gg/3Cpe5H6m"><img src="https://img.shields.io/badge/Discord-加入服务器-5865F2?logo=discord&logoColor=white" alt="Discord" /></a>
</p>

---

## 贡献

- 提 [Issue](https://github.com/DBell-workshop/AgentFleet/issues) 报告 Bug 或建议功能
- 提交 PR 贡献代码
- 在 [Discussions](https://github.com/DBell-workshop/AgentFleet/discussions) 交流想法

---

## 许可证

[Business Source License 1.1](LICENSE) · ✅ 个人/学习/研究 · ❌ 商业使用需授权 · 📅 2030 年转为 Apache 2.0

---

<p align="center">
  <sub>Built with ❤️ by the AgentFleet Team</sub>
</p>
