# Agent Memory System

AI Agent 长期记忆管理系统，采用分层架构 + 优先级机制，实现高效记忆存储与检索。

## 特性

- **L0/L1/L2 分层体系** - 按需加载，节省 token
- **P0/P1/P2 优先级** - 永久/90天/30天 TTL
- **Q1/Q2/Q3 写入决策** - 避免记忆过载
- **自动化工具** - 搜索、归档、知识提炼

## 文件结构

```
agent-memory/
├── SKILL.md                    # 架构说明
└── scripts/
    ├── memory_search.py        # 语义搜索
    ├── memory_get.py           # 精确读取
    ├── memory-janitor.py       # 自动清理
    └── memory-compounding.py   # 知识提炼
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/tonyjianchina/agent-memory.git
cd agent-memory
```

### 2. 配置权限

```bash
chmod +x scripts/*.py
```

### 3. 使用工具

```bash
# 搜索记忆
python3 scripts/memory_search.py "关键词"

# 读取记忆片段
python3 scripts/memory_get.py MEMORY.md --from 1 --lines 50

# 清理过期记忆
python3 scripts/memory-janitor.py

# 提炼知识
python3 scripts/memory-compounding.py
```

## 架构详解

详见 [SKILL.md](./SKILL.md)

## License

MIT
