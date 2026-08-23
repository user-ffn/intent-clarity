# Intent Clarity

**Tagline**: I got you.

> 通过诊断式提问帮用户澄清模糊需求，然后直接执行。

---

## 这是什么？

Intent Clarity 是一个面向 Claude Code 与 Codex 的 Agent Skill，帮助“有初步想法、但难以转化为可执行 AI 任务”的用户澄清需求并直接推进任务。

An Agent Skill (Claude Code & Codex) that helps users clarify vague intentions through diagnostic questioning,
then executes directly.

**不是**帮你生成更好的 prompt，**而是**识别用户当前最关键的信息缺口，澄清后直接开始执行。

---

## 为什么需要它？

很多人用 AI 时遇到的问题：
- ❌ "我想做点什么，但不知道做什么"
- ❌ "我想学AI，但不知道从哪开始"
- ❌ "我有个模糊的想法，但不知道怎么表达"

传统 AI 的回答：
- 🤖 "请明确你的需求"
- 🤖 "你可以这样问我..."
- 🤖 "我需要更多信息"

**Intent Clarity 的做法**：
- ✅ 每轮只问一个最影响下一步的问题，避免把对话变成表单
- ✅ 区分“已确认”和“推断”，不过度解释
- ✅ 根据需求状态选择澄清、探索、诊断或直接执行
- ✅ 澄清完直接执行，无缝衔接

---

## 工作原理

### 1. 快速澄清（已有行动目标，但缺少关键信息）

用户："帮我写一篇文章"

Intent Clarity：
- 判断：需求明确（行为清晰，缺细节）
- 每轮问一个补充问题（主题、受众或格式）
- 确认理解
- **直接开始写文章**

### 2. 深度探索（需求不明确时）

用户："我想做点什么但不知道做什么"

Intent Clarity：
- 判断：需求不明确
- 状态诊断（无方向+有动力）
- 用"经历回忆"策略提问（4-5个问题）
- 逐步聚焦到具体方向
- **给出具体建议并开始执行**

### 3. 问题诊断（已出现失败现象时）

用户：“我的产品没人用”

Intent Clarity：
- 先区分是“没人看到产品”，还是“试用后没有继续使用”
- 了解已尝试的方法与期望结果
- **定位问题后给出排查或修复路径**

### 4. 直接执行（目标清楚，或只缺待处理材料时）

用户：“帮我润色这段文字”

Intent Clarity：
- 索取原文
- **拿到材料后直接完成任务，不进行无关追问**

---

## 安装

### Claude Code

```bash
# 1. 克隆仓库
git clone https://github.com/user-ffn/intent-clarity.git

# 2. 复制到 Claude Code 技能目录
cp -r intent-clarity/skill ~/.claude/skills/intent-clarity
```

或者直接下载 `skill/SKILL.md`，放到 `~/.claude/skills/intent-clarity/` 目录下。

### Codex CLI

```bash
# 1. 克隆仓库
git clone https://github.com/user-ffn/intent-clarity.git

# 2. 复制到 Codex 技能目录
cp -r intent-clarity/codex ~/.codex/skills/intent-clarity
```

Codex 版内容和 Claude 版一致，仅 frontmatter 做了适配（Codex 不支持 `whenToUse` 字段，
触发条件合并进了 `description`）。两份文件由 `scripts/sync-codex.py` 从同一份源
（`skill/SKILL.md`）生成，**只需要维护 `skill/SKILL.md`**，改完跑一下脚本即可同步：

```bash
python scripts/sync-codex.py
```

### 核心规则验收

```bash
python evaluation/build_cases.py
python -m unittest discover -s tests -v
```

验收脚本会检查 50 个场景化用例是否完整生成；自动化测试只验证核心规则，
Skill 的实际对话表现仍需要在 Claude Code 或 Codex 中进行人工对话验收。

---

## 使用

### 自动触发

当你的表达包含以下特征时，Intent Clarity 会自动启动：
- "不知道怎么说/表达/描述"
- "想做X但..."
- "迷茫/困惑/不知道"

### 手动调用

```
/intent-clarity 我想做点什么但不知道做什么
```

或简写：
```
/ic 帮我想想我适合做什么
```

---

## 示例

### 示例1：写文章（快速澄清）

```
你：帮我写一篇文章

Intent Clarity：
这篇文章的主题是什么？

你：介绍我做的基金筛选工具

Intent Clarity：
打算发在哪？给谁看？

你：小红书，给对基金感兴趣的小白

Intent Clarity：
你希望读者看完有什么感受？

你：觉得这个工具有用，想试试

Intent Clarity：
让我确认一下：

已确认：
- 你想写一篇文章介绍你的基金筛选工具
- 发在小红书，给对基金感兴趣的小白看
- 希望读者觉得有用，想试试

我推断：
- 文章风格要通俗易懂（针对小白）
- 重点是实用性和易用性

对吗？

你：对

Intent Clarity：
好，我现在开始写。

# 基金太难选？这个工具3分钟帮你找到靠谱基金

[完整文章...]
```

### 示例2：不知道做什么（深度探索）

```
你：我想做点什么，但不知道做什么

Intent Clarity：
过去有没有什么事情，你做的时候特别投入？

你：高中时帮同学做PPT挺开心的

Intent Clarity：
你觉得那时候为什么开心？

你：能帮到别人，而且做出来的东西好看

Intent Clarity：
有没有什么事情别人觉得麻烦，但你觉得挺有意思？

你：整理信息、排版、配色

Intent Clarity：
让我确认一下：

已确认：
- 你喜欢创造视觉化的内容
- 你对整理信息、排版有兴趣
- 你希望能帮助到别人

我推断：
- 你可能适合做内容创作/信息可视化相关的事
- 你重视"有用"和"好看"的结合

对吗？

你：对，有道理

Intent Clarity：
明白了，那我给你3个具体方向，你可以今天就开始试：

1. **AI辅助的信息可视化**
   [详细展开...]

2. **小红书/即刻的图文创作**
   [详细展开...]

3. **帮产品/项目做落地页设计**
   [详细展开...]

你觉得哪个最有意思？我可以详细展开。
```

---

## 设计原则

### 1. 不追求完全理解，追求"够用"
不会无限提问，够用就停（最多4-5个问题）。

### 2. 区分"已确认"和"推断"
在确认理解时，明确标注哪些是用户说的，哪些是AI猜的。

### 3. 无缝衔接，直接执行
澄清完不让你复制prompt去别的地方，直接开始干活。

### 4. 动态调整，不走死流程
根据你的回答实时调整，不是机械地问问题。

### 5. 保持温度，不要机械
对话，不是表单填空。

---

## 核心技术

- **需求明确度诊断**：行为+目标+场景三维判断
- **任务类型分类**：6种任务（信息/内容/路径/决策/设计/问题诊断）
- **状态检测**：二维模型（方向×行动）
- **动态问题生成**：优先补充会改变后续方案的关键信息
- **不确定性管理**：区分已确认信息和推断信息
- **可重复验收**：将 50 个场景化用例结构化，分别评估路由、首问有效性、过度提问和任务启动

---

## 项目结构

```
intent-clarity/
├── core/                      # 核心逻辑（可复用）
│   ├── diagnosis.py           # 需求明确度诊断
│   ├── task_classifier.py     # 任务类型分类
│   ├── state_detector.py      # 状态检测
│   ├── question_generator.py  # 问题生成
│   └── router.py              # 统一路由：收敛诊断、任务和障碍判断
├── skill/                     # Claude Code 技能包（唯一维护源）
│   └── SKILL.md
├── codex/                     # Codex CLI 技能包（由 skill/SKILL.md 自动生成）
│   └── SKILL.md
├── scripts/
│   └── sync-codex.py          # skill/SKILL.md → codex/SKILL.md 同步脚本
├── evaluation/
│   ├── cases.json              # 从 test-cases.md 生成的 50 个结构化用例
│   └── build_cases.py          # 验收集生成脚本
├── tests/
│   └── test_core.py            # 核心路由与问题策略测试
├── examples/                  # 示例对话
└── README.md                  # 本文件
```

---

## 路线图

### v0.1（历史版本）
- ✅ 核心诊断逻辑
- ✅ 5种任务类型分类
- ✅ 快速澄清 + 深度探索两条路径
- ✅ Claude Code Skill 实现
- ✅ Codex CLI Skill 实现

### v1.2（评估闭环升级）
- ✅ 正式纳入“问题诊断”任务类型
- ✅ 诊断结果补充清晰度、缺失维度和推荐路径
- ✅ 区分真障碍与执行困惑，并优先处理执行困惑
- ✅ 将 50 个验收用例结构化
- ✅ 增加核心规则自动化测试
- ✅ Claude / Codex Skill 规则同步

### 后续方向
- ⏳ Web 版本（如果需要）
- ⏳ 数据埋点和使用分析
- ⏳ 更多语言支持

---

## 为什么叫 Intent Clarity？

- **Intent**：意图，你真正想要什么
- **Clarity**：清晰化，帮你想清楚
- **I got you**：我懂你

从 "Prompt Clarity"（帮你生成更好的prompt）
到 "Intent Clarity"（帮你理清真正的意图）

这个改名体现了产品理念的升级：
- 旧版：工具视角（生成prompt）
- 新版：伙伴视角（理解你，帮你做）

---

## 作者

这个项目来自一个产品思考：

大部分人不是不会用AI，而是不知道怎么把模糊需求说清楚。

与其让用户"学会提问"，不如让AI"学会理解"。

---

## License

MIT

---

## 致谢

感谢所有在迷茫中挣扎的人，这个工具是为你们做的。

**I got you.**
