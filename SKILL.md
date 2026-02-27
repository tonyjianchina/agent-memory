---
name: agent-memory
description: |
  AI Agent 长期记忆管理系统。采用分层架构+LTL+优先级机制，实现高效记忆存储与检索。
  用于：(1) 构建 AI agent 的持久记忆系统 (2) 管理多级记忆存储 (3) 自动记忆归档与清理
  (4) 基于语义检索的记忆召回。适用于需要长期上下文记忆的 AI 助手场景。
---

# Agent Memory System

AI Agent 长期记忆管理系统，基于分层架构实现高效记忆存储与检索。

## 核心概念

### L0/L1/L2 分层体系

| 层级 | 位置 | 内容 | 何时读取 |
|------|------|------|----------|
| **L0** | `.abstract` | 目录概览 | 始终最先 |
| **L1** | `insights/`, `lessons/`, `MEMORY.md` | 提炼的模式和教训 | 按需召回 |
| **L2** | `memory/YYYY-MM-DD.md` | 每日完整日志 | 深挖时读 |

> **90% 查询只需要 L0 + L1，省 token**

### 优先级 + TTL

所有条目带优先级标签：

| 标签 | 含义 | TTL |
|------|------|-----|
| **[P0]** | 永久重要，永不过期 | 永久 |
| **[P1]** | 中期相关 | 90 天 |
| **[P2]** | 临时备忘 | 30 天 |

### Q1/Q2/Q3 写入决策框架

写入记忆文件前必问：

- **Q1**: 下次醒来不看这条，会做错事吗？ → **[P0]**
- **Q2**: 某天可能需要查这条吗？ → **[P1]**
- **Q3**: 以上都不是？ → 留日志，不进长期记忆

## 文件结构

```
workspace/
├── .abstract                    # L0: 目录概览 (auto-gen)
├── MEMORY.md                    # L1: 长期记忆精华
├── SESSION-STATE.md             # 当前任务缓冲
├── GROUP_MEMORY.md              # 群聊记忆
├── insights/                    # L1: 月度洞察
│   └── YYYY-MM.md
├── lessons/                     # L1: 可执行教训
│   └── lessons.jsonl
└── memory/                      # L2: 每日日志
    ├── YYYY-MM-DD.md
    └── archive/                 # 过期归档
```

## 工具脚本

### 语义检索

```bash
python3 tools/memory_search.py <关键词>
```

在 MEMORY.md + memory/*.md 中语义搜索，返回匹配片段。

### 精确读取

```bash
python3 tools/memory_get.py <文件路径> --from <行号> --lines <行数>
```

安全读取记忆文件的指定行，用于获取精确上下文。

### 自动清理

```bash
python3 tools/memory-janitor.py
```

自动清理过期记忆：
- P1 条目：90 天后归档
- P2 条目：30 天后归档

### 知识提炼

```bash
python3 tools/memory-compounding.py
```

从每日日志提取洞察到 L1 层：
- 分析日志中的模式
- 生成 insights/ 月度洞察
- 写入 lessons/ 教训

## 使用流程

### 每轮对话开始

1. 读取 `SOUL.md` — 身份定义
2. 读取 `USER.md` — 用户信息
3. 读取 `SESSION-STATE.md` — 当前任务
4. 读取当日和昨日日志
5. 读取 `MEMORY.md`（主会话）或 `GROUP_MEMORY.md`（群聊）

### 写入新记忆

1. 问 Q1/Q2/Q3 确定优先级
2. 选择目标文件（P0→MEMORY.md, P1→insights/, P2→memory/)
3. 标注优先级标签
4. 简洁写入

### 检索记忆

1. 先读 L0 `.abstract` 了解结构
2. 用 `memory_search.py` 语义搜索
3. 用 `memory_get.py` 精确读取
4. 按需加载 L1/L2

## 安全准则

- **绝不泄露**：账号信息、API key、密码、Token 等敏感信息
- **保密原则**：用户的所有私密数据严格保密
- **按需加载**：不要把全部记忆塞进 context

---

> 记住：Q1/Q2/Q3 before every write!
