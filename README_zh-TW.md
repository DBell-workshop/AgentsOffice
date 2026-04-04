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
  <strong>給你的 AI 團隊一間看得見的辦公室</strong><br/>
  <sub>像素風 RPG 多 Agent 協作工作台</sub>
</p>

<p align="center">
  <a href="https://github.com/DBell-workshop/AgentFleet/stargazers"><img src="https://img.shields.io/github/stars/DBell-workshop/AgentFleet?style=social" alt="Stars" /></a>
  <a href="https://github.com/DBell-workshop/AgentFleet/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSL_1.1-blue" alt="License" /></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.9+-green" alt="Python" /></a>
  <a href="#"><img src="https://img.shields.io/badge/frontend-React%20%2B%20Phaser3-purple" alt="Frontend" /></a>
  <a href="https://github.com/DBell-workshop/AgentFleet/releases/latest"><img src="https://img.shields.io/badge/下載-macOS%20DMG-blue" alt="Download" /></a>
</p>

<p align="center">
  <a href="#screenshots">截圖</a> ·
  <a href="#features">功能</a> ·
  <a href="#quick-start">快速開始</a> ·
  <a href="#pro-vs-lite">Pro vs Lite</a> ·
  <a href="#support">支持我們</a>
</p>

---

## AgentFleet 是什麼？

AgentFleet 是一個**多 Agent 協作工作台**，用像素風 RPG 辦公室讓你的 AI 團隊「可視化地上班」。

定義角色、寫提示詞、選擇場景 —— 幾分鐘就能搭建屬於你的 AI 數位員工團隊。

> **和其他「像素辦公室」專案不同：我們的 Agent 不只是會走來走去的小人，它們真的在幹活。**

| 其他專案 | AgentFleet |
|---------|-------------|
| 純可視化看板，展示 Agent 狀態 | **完整的 AI 工作台**，Agent 有真實協作能力 |
| 需要外接其他 AI 工具才能工作 | **自帶 LLM 對話 + 委託引擎**，開箱即用 |
| 單角色展示 | **多角色團隊協作**，專案經理自動分配任務 |
| 只能看 | **對話、委託任務、即時追蹤進度** |

---

<a id="screenshots"></a>
## 截圖

> 截圖來自 **AgentFleet Pro**。Lite（開源版）包含核心像素辦公室、Agent 對話和場景系統。

<table>
<tr>
<td width="50%"><img src="docs/images/screenshots/scene-selector.png" alt="場景選擇" /><br/><sub>6 個預設場景範本：電商營運、自媒體工作室、客服中心、開發團隊、遊戲工作室、量化交易</sub></td>
<td width="50%"><img src="docs/images/screenshots/dashboard-dark.png" alt="深色大屏" /><br/><sub>即時營運大屏：Token 用量、成本追蹤、Agent 活動監控</sub></td>
</tr>
<tr>
<td><img src="docs/images/screenshots/dashboard-light.png" alt="淺色大屏" /><br/><sub>淺色主題大屏：委託漏斗、模型用量分佈</sub></td>
<td><img src="docs/images/screenshots/onboarding-scenes.png" alt="新手引導" /><br/><sub>引導式上手：選擇場景，立即開始工作</sub></td>
</tr>
</table>

---

<a id="features"></a>
## 功能

### 🏢 像素風 RPG 辦公室
基於 Phaser 3 遊戲引擎 —— 2D 像素辦公室，每個 Agent 有自己的工位、房間和動畫。

### 🎭 場景系統
切換預設場景範本，一鍵重新配置整個團隊：
- **自媒體工作室** —— 文案編輯、影片剪輯師、營運策劃、美工設計
- **電商營運中心** —— 資料工程師、資料產品經理、營運策劃
- **客服中心** —— 接待、投訴處理、跟進回訪
- **開發團隊、遊戲工作室、量化交易**等更多場景

每個場景擁有獨立的 Agent 團隊、聊天記錄和委託記錄 —— 完全隔離。

### 🤖 靈活的 Agent 系統
- **無限 Agent**：按需建立任意角色
- **單獨模型配置**：每個 Agent 可選擇不同的 LLM（Gemini、Claude、GPT、DeepSeek、Qwen）
- **20 個像素角色**外觀可選
- **桌面寵物貓咪**隨 Agent 工作狀態變化（12 種品種！）

### 💬 智慧對話
- **群聊**：專案經理自動識別意圖並分配給合適的 Agent
- **私聊**：與特定 Agent 一對一深入對話
- **圓桌討論**：多個 Agent 圍繞複雜話題協作討論

### 📋 委託系統（Pro）
一句話說出需求，AI 團隊自動規劃並執行。

### 📊 營運大屏（Pro）
即時監控：Token 用量、成本追蹤、Agent 活動、委託漏斗。

### 🐱 桌面寵物
像素貓咪夥伴，住在獨立視窗中 —— 12 種品種，雙擊切換。

---

<a id="quick-start"></a>
## 快速開始

### 桌面應用（推薦）

從 [Releases](https://github.com/DBell-workshop/AgentFleet/releases/latest) 下載最新 DMG：

1. 下載 `AgentFleet_x.x.x_aarch64.dmg`（macOS Apple Silicon）
2. 拖入 Applications
3. 啟動 —— 像素風 Loading 頁面會在後端啟動時顯示
4. 在設定中配置 API Key，即可開始對話

> DMG 已通過 Apple 簽名和公證 —— 安裝零警告。

### 開發模式

```bash
git clone https://github.com/DBell-workshop/AgentFleet.git
cd AgentFleet

# 後端
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_server.py

# 前端（另開終端）
cd frontend && npm install && npm run dev
```

訪問 **http://localhost:8000/static/office/**

### Docker

```bash
cp .env.example .env   # 至少添加一個 LLM API Key
docker compose up -d
```

---

<a id="pro-vs-lite"></a>
## Pro vs Lite

| 功能 | Lite（開源版） | Pro |
|------|:------------:|:---:|
| 像素風 RPG 辦公室 | ✅ | ✅ |
| Agent 對話（群聊 + 私聊） | ✅ | ✅ |
| 場景範本 | ✅ | ✅ |
| Agent 配置面板 | ✅ | ✅ |
| 圓桌討論 | ✅ | ✅ |
| 桌面寵物貓咪 | ✅ | ✅ |
| 委託系統 | - | ✅ |
| 營運大屏 | - | ✅ |
| CLI 整合（Claude/Codex） | - | ✅ |
| 桌面應用（Tauri） | - | ✅ |
| 電商報表 Pack | - | ✅ |

> 本倉庫為 **Lite** 版。截圖中的 Pro 功能僅作展示用途。
>
> 對 Pro 感興趣？訪問 [linkos.cc](https://linkos.cc) 或加入社群。

---

---

## 路線圖

- [x] 像素風 RPG 辦公室 + Agent 動畫
- [x] 場景系統 + 隔離的 Agent 和聊天記錄
- [x] 群聊調度 + 私聊 + 圓桌討論
- [x] 桌面寵物貓咪（12 種品種）
- [x] LLM 成本追蹤
- [x] 委託系統 / 營運大屏 / macOS 桌面應用（Pro）
- [ ] Windows / Linux 桌面應用
- [ ] 行動裝置響應式佈局
- [ ] 更多場景範本

---

<a id="support"></a>
## 支持這個專案

**⭐ [Star 這個倉庫](https://github.com/DBell-workshop/AgentFleet)** —— 最簡單的支持方式

---

## 社群

<p align="center">
  <a href="https://discord.gg/3Cpe5H6m"><img src="https://img.shields.io/badge/Discord-加入伺服器-5865F2?logo=discord&logoColor=white" alt="Discord" /></a>
</p>

---

## 貢獻

- 提 [Issue](https://github.com/DBell-workshop/AgentFleet/issues) 回報 Bug 或建議功能
- 提交 PR 貢獻程式碼
- 在 [Discussions](https://github.com/DBell-workshop/AgentFleet/discussions) 交流想法

---

## 授權條款

[Business Source License 1.1](LICENSE) · ✅ 個人/學習/研究 · ❌ 商業使用需授權 · 📅 2030 年轉為 Apache 2.0

---

<p align="center">
  <sub>Built with ❤️ by the AgentFleet Team</sub>
</p>
