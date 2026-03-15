/**
 * Agent 注册表 — 前端唯一数据源。
 *
 * 从后端 GET /api/v1/office/agent-registry 加载，
 * 用户可通过 UI 自定义 Agent 角色。
 */

export interface AgentRegistryEntry {
  slug: string;
  displayName: string;
  role: string;
  color: string;         // CSS hex color, e.g. "#4ade80"
  roomId: string;        // Phaser room id
  phaserAgentId: string; // Phaser sprite id
  isDispatcher: boolean;
}

/** sprite 映射：slug → 精灵 key。后端不管前端素材，由前端维护。 */
const SPRITE_MAP: Record<string, string> = {
  dispatcher: 'char_01',
  assistant: 'char_02',
  data_engineer: 'char_04',
};
let nextSpriteIndex = 5; // 用户自定义 agent 从 char_05 开始

/** 最大可用精灵数（素材包提供 20 个预制角色） */
const MAX_SPRITES = 20;

export function getSpriteKey(slug: string): string {
  if (SPRITE_MAP[slug]) return SPRITE_MAP[slug];
  // 动态分配（超出上限时循环复用）
  const idx = nextSpriteIndex <= MAX_SPRITES ? nextSpriteIndex : ((nextSpriteIndex - 1) % MAX_SPRITES) + 1;
  const key = `char_${String(idx).padStart(2, '0')}`;
  SPRITE_MAP[slug] = key;
  nextSpriteIndex++;
  return key;
}

/** 已加载的缓存（模块级单例） */
let cachedAgents: AgentRegistryEntry[] | null = null;
let loadPromise: Promise<AgentRegistryEntry[]> | null = null;

/** 硬编码 fallback — 通用版默认 Agent（使用 i18n） */
import { t } from './i18n';

function getFallbackAgents(): AgentRegistryEntry[] {
  return [
    { slug: 'dispatcher', displayName: t('builtin.dispatcher'), role: t('builtin.dispatcher.role'), color: '#ff6b6b', roomId: 'manager', phaserAgentId: 'agt_dispatcher', isDispatcher: true },
    { slug: 'assistant', displayName: t('builtin.assistant'), role: t('builtin.assistant.role'), color: '#4ade80', roomId: 'workspace', phaserAgentId: 'agt_assistant', isDispatcher: false },
    { slug: 'data_engineer', displayName: t('builtin.data_engineer'), role: t('builtin.data_engineer.role'), color: '#a78bfa', roomId: 'datacenter', phaserAgentId: 'agt_data_eng', isDispatcher: false },
  ];
}

/**
 * 加载 Agent 注册表。首次调用会发请求，后续返回缓存。
 * 失败时使用 fallback。
 */
export function loadAgentRegistry(): Promise<AgentRegistryEntry[]> {
  if (cachedAgents) return Promise.resolve(cachedAgents);
  if (loadPromise) return loadPromise;

  loadPromise = fetch('/api/v1/office/agent-registry')
    .then((r) => r.json())
    .then((envelope) => {
      const raw: any[] = envelope?.data?.agents || [];
      if (raw.length === 0) throw new Error('empty registry');
      cachedAgents = raw.map((a) => ({
        slug: a.slug,
        displayName: a.display_name,
        role: a.role || '',
        color: a.color || '#cccccc',
        roomId: a.room_id || 'workspace',
        phaserAgentId: a.phaser_agent_id || '',
        isDispatcher: a.is_dispatcher || false,
      }));
      return cachedAgents;
    })
    .catch(() => {
      cachedAgents = getFallbackAgents();
      return cachedAgents;
    });

  return loadPromise;
}

/** 同步获取已缓存的 agents（未加载时返回 fallback） */
export function getAgentsCached(): AgentRegistryEntry[] {
  return cachedAgents || getFallbackAgents();
}

/** 清除缓存，下次调用 loadAgentRegistry 时重新加载 */
export function invalidateAgentCache(): void {
  cachedAgents = null;
  loadPromise = null;
}
