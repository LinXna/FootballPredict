# V1.7 Architecture.md

## 1. 文档目的（Architecture Baseline）

本文档定义 V1.7 的唯一架构基线（Architecture Baseline）。

所有后续开发、代码评审、重构均以本文档为准。

如果代码与本文档冲突，应优先修改代码，而不是修改架构。

---

# 2. Architecture Goals

V1.7 目标：

* 单场比赛运行时隔离（Match Runtime Isolation）
* 多比赛并发（Multi Match）
* 实时预测（Live Prediction）
* WebSocket Streaming
* HTTP API
* Replay 能力
* 可扩展状态存储（State Store）

---

# 3. Architecture Layers

系统采用五层架构。

```
Client
    │
    ▼
Application Layer
(app/)
    │
    ▼
Management Layer
(LiveManager)
    │
    ▼
Runtime Layer
(MatchRuntime)
    │
    ▼
Business Layer
(Processor / Predictor / Adjuster)
    │
    ▼
Core Layer
(Pipeline / Model)
```

依赖方向只能自上而下。

禁止反向依赖。

---

# 4. Module Responsibilities

## app/

职责：

* FastAPI
* WebSocket
* HTTP
* Dependency Injection
* 生命周期启动

禁止：

* 修改 MatchState
* 调 Predictor
* 调 Processor
* 调 Pipeline

---

## LiveManager

职责：

* 管理多个 MatchRuntime
* 创建比赛
* 删除比赛
* 路由事件
* 生命周期管理

禁止：

* 保存 MatchState
* 预测
* 更新事件
* Feature Engineering

---

## MatchRuntime

职责：

* 单场比赛运行时
* 保存本场状态
* 驱动事件处理
* 驱动预测流程

禁止：

* 管理其他比赛
* HTTP
* WebSocket

---

## EventProcessor

职责：

* 处理 Event
* 更新 MatchState

禁止：

* 调 Pipeline
* 管理 Runtime

---

## LivePredictor

职责：

* Feature
* 调 Core Pipeline
* 返回预测结果

禁止：

* 修改 MatchState

---

## Core Pipeline

职责：

* 模型推理
* Feature → Probability

禁止：

* 保存比赛状态
* WebSocket
* Event

---

# 5. Dependency Rules

允许：

```
app
 ↓
LiveManager
 ↓
MatchRuntime
 ↓
Processor
 ↓
Predictor
 ↓
Core Pipeline
```

禁止：

```
app
 ↓
Pipeline
```

禁止：

```
Processor
 ↓
Manager
```

禁止：

```
Pipeline
 ↓
Runtime
```

禁止：

```
Predictor
 ↓
State Mutation
```

---

# 6. Match Lifecycle

```
create_match()

↓

MatchRuntime.start()

↓

process_event()

↓

predict()

↓

publish()

↓

remove_match()
```

MatchRuntime 生命周期由 LiveManager 管理。

---

# 7. Project Structure

```
app/
    run.py
    api.py
    websocket.py
    dependencies.py

core/
    pipeline.py
    feature.py
    model.py

live/
    manager.py
    runtime.py
    pipeline.py
    predictor.py
    processor.py
    adjuster.py
    queue.py
    state.py
    events.py
    replay.py
    state_store.py

tests/
```

---

# 8. Compatibility Decision

当前保留：

```
live/pipeline.py
```

原因：

* 避免大规模 import 修改。
* 保持 V1.7 工程稳定。

当前定位：

LivePipeline 为 Facade（外观层）。

职责：

* 对外提供统一 Live 接口。
* 内部调用 LiveManager。

禁止：

* 保存 MatchState。
* 创建 Predictor。
* 创建 Processor。
* 保存 Runtime。

未来（V2.0）评估是否重命名为：

```
live/engine.py
```

该变更不属于 V1.7 范围。

---

# 9. Code Review Checklist

每次提交必须检查：

* 是否违反依赖方向？
* 是否跨层调用？
* 是否新增状态？
* 是否新增生命周期？
* 是否绕过 LiveManager？
* 是否修改了 MatchRuntime 边界？
* 是否修改了 Pipeline 职责？

任一项为"是"，必须重新评审。

---

# 10. Architecture Freeze

自 V1.7 起：

未经 Architecture Review，

禁止：

* 新增层级
* 修改模块职责
* 修改依赖方向
* 引入新的 Runtime
* 引入新的 Pipeline

所有架构调整必须先更新 Architecture.md，再进入代码实现。
