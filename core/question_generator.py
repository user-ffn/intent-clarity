# -*- coding: utf-8 -*-
"""
问题生成器
根据任务类型和状态生成针对性问题
"""


class QuestionGenerator:
    """问题生成器"""

    MAX_QUESTIONS = 3

    # 高频场景专门问题模板（优先匹配）
    HIGH_FREQ_SCENARIOS = {
        "考研": [
            "考研的主要原因是什么？（提升学历/延缓就业/学术兴趣/其他）",
            "除了考研，你还在考虑工作/出国/gap year吗？",
            "读研之后想做什么？"
        ],
        "转行": [
            "为什么想转行？（当前工作的问题 vs 目标行业的吸引力）",
            "目标行业/岗位是什么？",
            "你有相关技能或经验吗？"
        ],
        "创业": [
            "你有具体的方向了吗？（有明确想法 / 还在探索）",
            "为什么是现在？（时机/资源/机会）",
            "你对风险的承受能力？（可以承受多长时间没收入）"
        ],
        "学Python": [
            "用Python主要做什么？（数据分析/web开发/自动化/AI）",
            "你有编程基础吗？",
            "每天/每周能投入多少时间？"
        ],
        "学AI": [
            "学AI用来做什么？（工作需要/做项目/转行/兴趣）",
            "你有编程基础吗？（Python/数学）",
            "期望多久能上手？"
        ],
        "辞职": [
            "是什么让你想辞职？（具体的事 vs 长期的不满）",
            "辞职后打算做什么？（有明确计划 / 还没想好）",
            "你的财务缓冲能支撑多久？"
        ],
        "找副业": [
            "找副业的主要目的？（增加收入/探索方向/技能变现）",
            "每周能投入多少时间？",
            "你有什么技能/资源可以利用？"
        ],
        "换工作": [
            "想换工作的主要原因？（薪资/成长/环境/方向）",
            "期望的新工作是什么样的？",
            "有什么硬性要求？（地点/薪资/行业）"
        ]
    }

    # 明确任务的问题模板
    CLEAR_TASK_QUESTIONS = {
        "获取信息": [
            "你想了解到什么程度？（简单了解 / 深入理解 / 系统学习）",
            "这个信息你打算用来做什么？"
        ],

        "生成内容": [
            "这个内容的目标受众是谁？",
            "你期望的长度/规模？（简短 / 中等 / 详细）",
            "有什么特别要求或者禁忌吗？"
        ],

        "制定路径": [
            "你学这个主要用来做什么？（这是最重要的）",
            "你现在的水平？（完全零基础 / 有一点基础 / 有相关经验）",
            "你能投入多少时间？（每天/每周）"
        ],

        "辅助决策": [
            "你现在有哪些选项？",
            "如果只能选一个标准，你最在意什么？（时间/收益/风险/成就感）",
            "有什么硬性约束条件吗？（预算/时间/能力）"
        ],

        "创造设计": [
            "这个产品/系统的目标用户是谁？",
            "核心要解决什么问题？",
            "你现在有什么资源？（时间/预算/技术能力）"
        ],

        "问题诊断": [
            "具体情况是怎样的？（现象/数据/截图）",
            "你已经尝试过什么方法？",
            "期望的结果是什么？"
        ]
    }

    def detect_high_freq_scenario(self, user_input):
        """
        检测用户输入是否匹配高频场景

        Args:
            user_input: 用户输入文本

        Returns:
            str or None: 匹配的场景名，没有匹配返回None
        """
        user_input_lower = user_input.lower()

        # 关键词匹配
        keyword_map = {
            "考研": ["考研", "读研", "研究生"],
            "转行": ["转行", "换行业", "改行"],
            "创业": ["创业", "做生意", "开公司"],
            "学Python": ["学python", "python入门", "python基础"],
            "学AI": ["学ai", "学人工智能", "学机器学习", "学深度学习"],
            "辞职": ["辞职", "离职", "quit job"],
            "找副业": ["副业", "兼职", "第二职业"],
            "换工作": ["换工作", "跳槽", "找工作"]
        }

        for scenario, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    return scenario

        return None

    def generate_for_clear_task(self, task_type, current_info, user_input=""):
        """
        为明确任务生成补充问题

        Args:
            task_type: 任务类型
            current_info: 已经知道的信息 dict
            user_input: 用户原始输入（用于检测高频场景）

        Returns:
            list of questions
        """
        # 优先检测高频场景
        scenario = self.detect_high_freq_scenario(user_input)
        if scenario:
            all_questions = self.HIGH_FREQ_SCENARIOS.get(scenario, [])
        else:
            all_questions = self.CLEAR_TASK_QUESTIONS.get(task_type, [])

        # 动态过滤：如果某个信息已经有了，就不问对应的问题
        questions = []
        for q in all_questions[:self.MAX_QUESTIONS]:  # 最多3个问题
            # 简单判断：如果问题关键词在已知信息里，就跳过
            if not self._info_already_known(q, current_info):
                questions.append(q)

        return questions

    def get_priority_questions(self, task_type, current_info, user_input=""):
        """
        返回当前最值得优先补充的问题。

        产品原则：问题不是越多越好，而是优先补齐会改变后续方案的关键信息。
        该方法保留原有 generate_for_clear_task 的兼容性，供验收和上层编排使用。
        """
        questions = self.generate_for_clear_task(
            task_type, current_info, user_input
        )
        return questions[:1]

    def _info_already_known(self, question, current_info):
        """
        判断问题对应的信息是否已经知道

        简化版：检查关键词
        """
        question_lower = question.lower()

        # 受众相关
        if "受众" in question_lower or "给谁" in question_lower or "用户" in question_lower:
            return current_info.get("audience") is not None

        # 长度相关
        if "长度" in question_lower or "规模" in question_lower:
            return current_info.get("length") is not None

        # 水平相关
        if "水平" in question_lower or "基础" in question_lower:
            return current_info.get("level") is not None

        # 时间相关
        if "时间" in question_lower or "投入" in question_lower:
            return current_info.get("time") is not None

        # 目标相关
        if "目标" in question_lower or "目的" in question_lower or "用来做什么" in question_lower:
            return current_info.get("goal") is not None

        # 原因相关
        if "原因" in question_lower or "为什么" in question_lower:
            return current_info.get("reason") is not None

        # 问题诊断相关：现象、已尝试方法和期望结果必须独立记录，
        # 否则用户已经描述“结果”时仍会被重复追问。
        if "具体情况" in question_lower or "现象" in question_lower:
            return current_info.get("context") is not None

        if "尝试过" in question_lower or "方法" in question_lower:
            return current_info.get("attempts") is not None

        if "期望的结果" in question_lower or "期望结果" in question_lower:
            return current_info.get("expected_result") is not None

        # 选项相关
        if "选项" in question_lower or "还在考虑" in question_lower:
            return current_info.get("options") is not None

        return False

    def classify_obstacle(self, user_input):
        """
        区分真障碍、执行困惑和未知状态。

        Args:
            user_input: 用户输入

        Returns:
            str: real_obstacle / execution_confusion / unknown
        """
        # 真障碍信号
        real_obstacle_keywords = [
            "一直想", "一直没", "不敢", "怕", "有没有必要",
            "值不值得", "担心", "顾虑", "犹豫"
        ]

        # 执行困惑信号
        execution_confusion_keywords = [
            "不知道从哪开始", "不知道怎么做", "不知道学什么",
            "怎么入门", "如何开始", "第一步"
        ]

        user_input_lower = user_input.lower()

        # 检测执行困惑（优先级更高，因为更常见）
        for keyword in execution_confusion_keywords:
            if keyword in user_input_lower:
                return "execution_confusion"  # 不是真障碍

        # 检测真障碍
        for keyword in real_obstacle_keywords:
            if keyword in user_input_lower:
                return "real_obstacle"  # 是真障碍

        # 默认：如果说了"但是"/"可是"，倾向于是真障碍
        if "但是" in user_input_lower or "可是" in user_input_lower:
            return "real_obstacle"

        return "unknown"

    def is_real_obstacle(self, user_input):
        """兼容旧接口：仅返回是否识别为真障碍。"""
        return self.classify_obstacle(user_input) == "real_obstacle"

    def generate_confirmation(self, confirmed_info, inferred_info):
        """
        生成确认段落

        区分"已确认"和"推断"信息

        Args:
            confirmed_info: dict，已确认的信息（用户明确说的）
            inferred_info: dict，推断的信息（AI猜测的）

        Returns:
            str，确认段落
        """
        parts = ["让我确认一下：\n"]

        # 已确认部分
        if confirmed_info:
            parts.append("**已确认**：")
            for key, value in confirmed_info.items():
                parts.append(f"- {value}")

        # 推断部分
        if inferred_info:
            parts.append("\n**我推断**：")
            for key, value in inferred_info.items():
                parts.append(f"- {value}")

        parts.append("\n我理解对吗？有需要修正的吗？")

        return "\n".join(parts)


# 测试代码
if __name__ == "__main__":
    generator = QuestionGenerator()

    # 测试1：生成内容任务
    print("=== 测试1：生成内容 ===")
    questions = generator.generate_for_clear_task(
        "生成内容",
        {},  # 没有已知信息
        user_input="帮我写一篇文章"
    )
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")

    # 测试2：高频场景 - 考研
    print("\n=== 测试2：高频场景 - 考研 ===")
    questions = generator.generate_for_clear_task(
        "辅助决策",
        {},
        user_input="我要不要考研"
    )
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")

    # 测试3：高频场景 - 学Python
    print("\n=== 测试3：高频场景 - 学Python ===")
    questions = generator.generate_for_clear_task(
        "制定路径",
        {},
        user_input="我想学Python"
    )
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")

    # 测试4：真障碍 vs 执行困惑
    print("\n=== 测试4：真障碍 vs 执行困惑 ===")
    print(f"'我想学编程，但一直没开始' -> 真障碍: {generator.is_real_obstacle('我想学编程，但一直没开始')}")
    print(f"'我想学编程，但不知道从哪开始' -> 真障碍: {generator.is_real_obstacle('我想学编程，但不知道从哪开始')}")

    # 测试5：问题诊断类型
    print("\n=== 测试5：问题诊断 ===")
    questions = generator.generate_for_clear_task(
        "问题诊断",
        {},
        user_input="我的产品没人用"
    )
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")

    # 测试6：确认段落生成
    print("\n=== 测试6：确认段落 ===")
    confirmation = generator.generate_confirmation(
        confirmed_info={
            "task": "你想写一篇文章介绍你的基金筛选工具",
            "platform": "发在小红书"
        },
        inferred_info={
            "audience": "你的目标读者可能是对基金投资感兴趣的小白",
            "goal": "你希望吸引用户来试用你的工具"
        }
    )
    print(confirmation)
