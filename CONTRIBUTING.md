# Contributing to AgentsOffice

感谢你对 AgentsOffice 的关注！我们欢迎各种形式的贡献。

## 如何参与

### 报告 Bug

- 使用 [Bug Report](https://github.com/DBell-workshop/ecommerce-ai-lab/issues/new?template=bug_report.md) 模板提交 Issue
- 描述复现步骤、期望行为和实际行为
- 附上浏览器控制台截图（如有）

### 提出功能建议

- 使用 [Feature Request](https://github.com/DBell-workshop/ecommerce-ai-lab/issues/new?template=feature_request.md) 模板提交 Issue
- 描述使用场景和期望的效果

### 提交代码

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/your-feature`
3. 提交改动：`git commit -m "feat: add your feature"`
4. 推送分支：`git push origin feat/your-feature`
5. 创建 Pull Request

### Commit 规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat:     新功能
fix:      Bug 修复
docs:     文档更新
refactor: 代码重构（不影响功能）
test:     测试相关
chore:    构建/工具/依赖变更
```

示例：`feat(agent): add create/delete Agent lifecycle`

## 开发环境

### 前置要求

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose（PostgreSQL）

### 启动开发环境

```bash
# 1. 数据库
docker compose up -d

# 2. 后端
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 编辑 .env 填入 API Key
uvicorn app.main:app --reload --port 8001

# 3. 前端（开发模式，支持热更新）
cd frontend
npm install
npm run dev
```

### 项目结构

```
app/                    # FastAPI 后端
├── office/             #   AgentsOffice 容器层（路由、存储）
├── services/           #   业务服务（Agent 调度、LLM、比价）
├── db/                 #   数据库模型
└── static/office/      #   前端构建产物

frontend/               # React + Phaser 前端
├── src/react/          #   React 组件（面板、对话框）
├── src/phaser/         #   Phaser 场景（RPG 办公室）
└── src/shared/         #   共享类型、事件总线、注册表
```

### 构建前端

```bash
cd frontend
npm run build          # 输出到 ../app/static/office/
```

## 代码风格

- **后端**：Python，遵循 PEP 8，使用 type hints
- **前端**：TypeScript，使用 React Hooks，内联 CSS（monospace 像素风）
- 保持简洁，不过度工程化

## 许可证

提交代码即表示你同意将贡献按 [BSL 1.1](LICENSE) 许可发布。
