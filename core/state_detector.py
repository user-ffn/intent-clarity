# -*- coding: utf-8 -*-
"""
状态诊断模块（用于需求不明确时）
基于GPT的二维模型：方向×行动
"""


class StateDetector:
    """用户状态检测器（仅在需求不明确时使用）"""

    # 关键词模式
    PATTERNS = {
        "有行为": ["我想做", "我要", "打算", "准备", "想学", "想写", "想创建"],
        "有迷茫": ["不知道", "迷茫", "困惑", "没方向", "没目标"],
        "有抱怨": ["不行", "不满意", "不喜欢", "受不了", "烦", "讨厌"],
        "有羡慕": ["羡慕", "佩服", "想成为", "希望像", "别人都"],
        "有拖延": ["一直没", "总是拖", "想做但", "迟迟没", "还没开始"],
        "有选择": ["还是", "纠结", "不知道选", "哪个", "或者"]
    }

    def detect(self, user_input):
        """
        检测用户状态

        返回：
        {
            "state": str,  # 二维状态：有方向+有行动 / 有方向+无行动 / 无方向+有动力 / 无方向+无动力
            "detected_patterns": list,  # 检测到的模式
            "strategy": str  # 推荐的探索策略
        }
        """
        user_input = user_input.lower()

        # 检测各种模式
        detected = []
        for pattern, keywords in self.PATTERNS.items():
            if any(kw in user_input for kw in keywords):
                detected.append(pattern)

        # 判断方向维度
        has_direction = "有行为" in detected

        # 判断行动维度
        has_action = not ("有拖延" in detected or "有迷茫" in detected)

        # 确定二维状态
        if has_direction and has_action:
            state = "有方向+有行动"
            strategy = "直接支持"
        elif has_direction and not has_action:
            state = "有方向+无行动"
            strategy = "障碍分析"
        elif not has_direction and has_action:
            state = "无方向+有动力"
            strategy = "经历回忆"
        else:
            state = "无方向+无动力"
            strategy = "情绪理解"

        return {
            "state": state,
            "detected_patterns": detected,
            "strategy": strategy
        }

    def get_questions(self, strategy):
        """
        根据策略返回问题集
        """
        question_sets = {
            "障碍分析": [
                "是什么让你一直没有开始？",
                "如果这个障碍不存在，你会立刻开始吗？",
                "你觉得最小的第一步是什么？"
            ],

            "经历回忆": [
                "过去有没有什么事情，你做的时候特别投入？",
                "有没有什么事情别人觉得麻烦，但你觉得挺有意思？",
                "有没有一次经历，让你觉得'这件事我做得不错'？"
            ],

            "情绪理解": [
                "最近发生什么事情让你有这种感觉？",
                "如果什么都不改变，你觉得三年后会怎样？",
                "你现在最害怕失去什么？"
            ],

            "价值排序": [
                "如果只能选一个，你最在意什么？",
                "五年后回看，哪个选择你会觉得'还好当时选了它'？",
                "假设两个选择结果都一样，你会选哪个？"
            ],

            "五个为什么": [
                "为什么你现在想做这个？",
                "你希望通过这件事达到什么？",
                "如果成功了，你觉得最大的收获是什么？"
            ],

            "理想-现实": [
                "现在最让你不满意的是什么？",
                "如果一年后你状态很好，你觉得每天是什么样？",
                "中间最大的障碍是什么？"
            ],

            "投射提问": [
                "你羡慕他们什么？（具体一点）",
                "如果你也有那样的状态，你最想用它来做什么？",
                "你觉得自己和他们之间，最大的差别是什么？"
            ]
        }

        # 根据detected_patterns选择更精确的策略
        return question_sets.get(strategy, question_sets["五个为什么"])


# 测试代码
if __name__ == "__main__":
    detector = StateDetector()

    test_cases = [
        "我想学AI但一直没开始",
        "我不知道未来干什么",
        "我很羡慕那些创业成功的人",
        "我想做点什么，但不知道做什么"
    ]

    for case in test_cases:
        print(f"\n输入: {case}")
        result = detector.detect(case)
        print(f"状态: {result['state']}")
        print(f"检测到的模式: {result['detected_patterns']}")
        print(f"推荐策略: {result['strategy']}")
        print(f"问题集: {detector.get_questions(result['strategy'])[:2]}")  # 只显示前2个
