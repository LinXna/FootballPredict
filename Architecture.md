# FootballPredict Architecture (V2.0)

## 1. Overall Architecture

系统采用分层结构：
Data → Features → Models → Ensemble → Live Runtime → Snapshot → Evaluation → Learning


---

## 2. Core Modules

### 2.1 Models Layer
- EloModel（ranking system）
- PoissonModel（goal distribution）

### 2.2 Feature Layer
- basic_features
- h2h features
- rolling form

### 2.3 Live System
- Event-driven execution
- State mutation controlled by processor
- Queue-based event buffering

---

## 3. Critical Data Flow
WebSocket → Event → Queue → Processor → State → Predictor → Snapshot → Replay → Evaluation

---

## 4. Learning System (IMPORTANT)
Snapshot → Feedback Loop → Reward Engine → Weight Updater → Evolution


⚠️ 注意：
- Learning 不允许直接修改 live state
- 所有更新必须通过 evolution layer

---

## 5. Separation Rules

- live/ 不能直接调用 learning/
- learning/ 只能读取 snapshot
- models/ 不可依赖 live/