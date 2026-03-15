-- ============================================================
-- AgentsOffice 数据库初始化
-- Docker 首次启动时自动执行
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- 1. 异步任务表
-- ============================================================
CREATE TABLE IF NOT EXISTS tasks (
    task_id     TEXT PRIMARY KEY,
    trace_id    TEXT NOT NULL,
    task_type   TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'running', 'succeeded', 'failed')),
    input       JSONB NOT NULL DEFAULT '{}',
    output      JSONB,
    error       TEXT,
    agent_id    TEXT,
    agent_slug  TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_trace ON tasks (trace_id);
CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks (task_type);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON tasks (created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_agent ON tasks (agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_slug ON tasks (agent_slug);

-- ============================================================
-- 2. Agent 事件日志表
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_events (
    event_id    BIGSERIAL PRIMARY KEY,
    trace_id    TEXT NOT NULL,
    agent_name  TEXT NOT NULL,
    event_type  TEXT NOT NULL,
    session_id  TEXT,
    payload     JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_events_trace ON agent_events (trace_id);
CREATE INDEX IF NOT EXISTS idx_events_agent ON agent_events (agent_name);
CREATE INDEX IF NOT EXISTS idx_events_type ON agent_events (event_type);
CREATE INDEX IF NOT EXISTS idx_events_created ON agent_events (created_at);

-- ============================================================
-- 3. Agent 注册表
-- ============================================================
CREATE TABLE IF NOT EXISTS agents (
    agent_id        TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    slug            TEXT NOT NULL UNIQUE,
    description     TEXT,
    agent_type      TEXT NOT NULL DEFAULT 'general',
    status          TEXT NOT NULL DEFAULT 'idle'
                    CHECK (status IN ('idle', 'running', 'error', 'disabled')),
    model_config    JSONB NOT NULL DEFAULT '{}',
    last_active_at  TIMESTAMPTZ,
    error_message   TEXT,
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agents_slug ON agents (slug);
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents (status);

-- ============================================================
-- 4. Skill 注册表
-- ============================================================
CREATE TABLE IF NOT EXISTS skills (
    skill_id        TEXT PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    description     TEXT,
    skill_type      TEXT NOT NULL DEFAULT 'tool'
                    CHECK (skill_type IN ('tool', 'api', 'knowledge', 'internal')),
    endpoint        TEXT,
    config          JSONB NOT NULL DEFAULT '{}',
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'deprecated', 'disabled')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- 5. Agent-Skill 关联表
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_skills (
    agent_id    TEXT NOT NULL REFERENCES agents(agent_id),
    skill_id    TEXT NOT NULL REFERENCES skills(skill_id),
    config      JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (agent_id, skill_id)
);

-- ============================================================
-- 6. 成本记录表
-- ============================================================
CREATE TABLE IF NOT EXISTS cost_records (
    record_id       BIGSERIAL PRIMARY KEY,
    agent_id        TEXT REFERENCES agents(agent_id),
    agent_slug      TEXT NOT NULL,
    task_id         TEXT,
    trace_id        TEXT NOT NULL,
    model_name      TEXT NOT NULL,
    input_tokens    INT NOT NULL DEFAULT 0,
    output_tokens   INT NOT NULL DEFAULT 0,
    total_tokens    INT NOT NULL DEFAULT 0,
    input_cost      NUMERIC(12, 6) NOT NULL DEFAULT 0,
    output_cost     NUMERIC(12, 6) NOT NULL DEFAULT 0,
    total_cost      NUMERIC(12, 6) NOT NULL DEFAULT 0,
    duration_ms     INT,
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cost_agent_slug ON cost_records (agent_slug);
CREATE INDEX IF NOT EXISTS idx_cost_model ON cost_records (model_name);
CREATE INDEX IF NOT EXISTS idx_cost_created ON cost_records (created_at);

-- ============================================================
-- 7. 模型定价表
-- ============================================================
CREATE TABLE IF NOT EXISTS model_pricing (
    model_name          TEXT PRIMARY KEY,
    display_name        TEXT NOT NULL,
    provider            TEXT NOT NULL DEFAULT 'openai',
    input_price_per_1k  NUMERIC(10, 6) NOT NULL,
    output_price_per_1k NUMERIC(10, 6) NOT NULL,
    is_active           BOOLEAN NOT NULL DEFAULT true,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO model_pricing (model_name, display_name, provider, input_price_per_1k, output_price_per_1k) VALUES
    ('gpt-4o',      'GPT-4o',      'openai',    0.002500, 0.010000),
    ('gpt-4o-mini', 'GPT-4o Mini', 'openai',    0.000150, 0.000600),
    ('claude-sonnet-4-20250514', 'Claude Sonnet 4', 'anthropic', 0.003000, 0.015000),
    ('gemini/gemini-2.5-flash-preview-05-20','Gemini 2.5 Flash','google',0.000150,0.000600),
    ('deepseek/deepseek-chat',   'DeepSeek V3',    'deepseek',  0.000270, 0.001100)
ON CONFLICT (model_name) DO NOTHING;
