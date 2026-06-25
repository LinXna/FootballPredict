# ⚽ FootballPredict V2.0

一个融合统计建模（Elo / Poisson）+ 实时事件驱动（Live System）+ 快照回放（Snapshot / Replay）+ 自学习优化（Learning / Evolution）的足球比赛预测系统。

---

# 📌 一、系统定位

本项目不是单一预测模型，而是一个：

> “可回放、可学习、可演化的比赛预测引擎”

核心目标：
- 实时比赛概率预测
- 历史比赛可复现回放
- 多模型融合（Elo + Poisson）
- 长期权重自适应优化

---

# 🏗 二、整体架构

## 系统分层结构

Data Layer → Feature Engineering → Model Layer → Ensemble Layer → Live Runtime → Snapshot System → Replay & Evaluation → Learning System → Evolution Layer

---

## 核心实时数据流

WebSocket Event → MatchEvent → EventQueue → EventProcessor → MatchState → Predictor (Elo + Poisson) → Snapshot → Replay / Evaluation

---

## 学习闭环（严格隔离）

Snapshot → Feedback Loop → Reward Engine → Weight Updater → Evolution Layer

⚠️ 重要规则：
- learning 不能直接修改 live state
- learning 只能基于 snapshot
- evolution 才能影响模型权重

---

# 📁 三、项目结构

models/        # 基础统计模型（Elo / Poisson）
core/          # 核心预测管线
live/          # 实时比赛执行系统
features/      # 特征工程
learning/      # 自学习系统
evolution/     # 权重演化系统
data/          # 数据处理与加载

---

# ⚙️ 四、核心模块说明

## 1️⃣ models（统计模型层）

EloModel：球队强弱评分系统  
PoissonModel：进球分布建模  

---

## 2️⃣ live（实时系统）

职责：
- 接收比赛事件（WebSocket）
- 事件队列缓存
- 状态更新（MatchState）
- 实时预测输出

原则：
> 所有状态变化必须由事件驱动

---

## 3️⃣ features（特征工程）

- 基础统计特征
- H2H（历史交锋）
- form（近期状态）

---

## 4️⃣ learning（学习系统）

- feedback_loop：误差反馈
- reward_engine：奖励函数
- weight_updater：权重更新

限制：
- 只能读取 snapshot
- 禁止直接修改 live runtime

---

## 5️⃣ evolution（演化系统）

职责：
- 长期权重调整
- 防止短期噪声影响模型
- 稳定系统预测能力

---

# 🔄 五、运行模式

## Backtest（回测）
python main.py --mode backtest

## Benchmark（基准测试）
python main.py --mode benchmark

## Live（实时模式）
python main.py --mode live

---

# 🧪 六、启动方式

pip install -r requirements.txt
python main.py

---

# 📊 七、关键设计原则

## 1️⃣ 分层隔离
live ❌ 不允许调用 learning  
learning ❌ 不允许修改 live  
models ❌ 不依赖 live  

---

## 2️⃣ 数据不可逆原则
- snapshot 是唯一事实记录
- replay 必须可复现
- 不允许 runtime 修改历史数据

---

## 3️⃣ 事件驱动原则
状态变化 = event → processor → state

禁止：
- 直接修改 state
- 跳过 event system

---

## 4️⃣ 学习闭环隔离
learning 只能：
- 读取 snapshot
- 计算 reward
- 输出权重更新

不能：
- 访问 runtime
- 修改 match state

---

# ⚠️ 八、系统限制说明

当前系统处于：

V2.0 架构冻结阶段（Architecture Freeze）

允许：
- 模块内部优化
- 模型参数优化

禁止：
- 改变数据流结构
- 破坏 learning/lives 分层
- 引入跨层依赖

---

# 📌 九、系统特点总结

✔ 支持实时预测  
✔ 支持历史回放  
✔ 支持双模型融合（Elo + Poisson）  
✔ 支持自学习优化  
✔ 支持长期权重演化  

---

# 🚀 十、未来优化方向

- 引入 xG（expected goals）替代伪标签 Poisson
- learning → Bayesian calibration
- live event compression optimization
- ensemble dynamic weighting

---

# 🧠 备注（中文说明）

本 README 已根据 V2.0 实际代码结构重写，重点强化：
- live / learning 隔离
- snapshot 可追溯性
- replay 一致性
- 模型层职责边界
- 系统工程稳定性