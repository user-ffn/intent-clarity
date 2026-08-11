# -*- coding: utf-8 -*-
"""
需求明确度诊断模块
判断用户需求是否明确（行为+目标+场景）
"""


class ClarityDiagnosis:
    """需求明确度诊断器"""

    # 行为关键词（用户说了具体要做什么）
    BEHAVIOR_KEYWORDS = [
        "写", "做", "生成", "创建", "设计", "开发",
        "分析", "总结", "整理", "提取", "翻译",
        "学", "掌握", "了解", "研究",
        "选择", "决定", "判断", "对比",
        "帮我", "给我", "推荐"
    ]

    # 目标关键词（用户说了想达到什么）
    GOAL_KEYWORDS = [
        "为了", "用来", "想要", "希望", "达到",
        "提高", "提升", "改善", "解决", "优化",
        "获得", "赚", "节省", "实现"
    ]

    # 场景关键词（用户说了在什么情况下用）
    SCENE_KEYWORDS = [
        "工作", "项目", "公司", "学校", "课程",
        "日常", "每天", "经常", "平时",
        "面试", "求职", "创业", "副业",
        "发", "分享", "展示", "宣传"
    ]

    # 不明确信号（强烈的不确定性）
    UNCLEAR_SIGNALS = [
        "不知道", "不清楚", "不确定", "不太明白",
        "迷茫", "困惑", "纠结", "犹豫",
        "想做点什么", "做点啥", "干点啥",
        "不知道做什么", "不知道说什么", "不知道怎么说"
    ]

    def diagnose(self, user_input):
        """
        诊断需求明确度

        返回：
        {
            "is_clear": bool,  # 需求是否明确
            "has_behavior": bool,  # 是否有明确行为
            "has_goal": bool,  # 是否有明确目标
            "has_scene": bool,  # 是否有明确场景
            "confidence": float,  # 判断置信度 0-1
            "unclear_signals": list  # 检测到的不明确信号
        }
        """
        user_input = user_input.lower()

        # 检测三个维度
        has_behavior = self._check_keywords(user_input, self.BEHAVIOR_KEYWORDS)
        has_goal = self._check_keywords(user_input, self.GOAL_KEYWORDS)
        has_scene = self._check_keywords(user_input, self.SCENE_KEYWORDS)

        # 检测不明确信号
        unclear_signals = [
            signal for signal in self.UNCLEAR_SIGNALS
            if signal in user_input
        ]

        # 判断逻辑
        if unclear_signals:
            # 有强烈的不确定信号 → 需求不明确
            is_clear = False
            confidence = 0.9
        elif has_behavior and has_goal and has_scene:
            # 三个都有 → 需求明确
            is_clear = True
            confidence = 0.9
        elif has_behavior and (has_goal or has_scene):
            # 行为明确 + (目标或场景) → 灰色地带，需要验证
            is_clear = None  # None = 需要验证
            confidence = 0.6
        else:
            # 其他情况 → 需求不明确
            is_clear = False
            confidence = 0.7

        return {
            "is_clear": is_clear,
            "has_behavior": has_behavior,
            "has_goal": has_goal,
            "has_scene": has_scene,
            "confidence": confidence,
            "unclear_signals": unclear_signals
        }

    def _check_keywords(self, text, keywords):
        """检查文本中是否包含关键词列表中的任意一个"""
        return any(kw in text for kw in keywords)

    def generate_verification_question(self, diagnosis):
        """
        根据诊断结果生成验证问题（用于灰色地带）

        当 is_clear = None 时调用
        """
        if diagnosis["has_behavior"] and not diagnosis["has_goal"]:
            return "你已经决定要做这个了，还是在考虑要不要做？"
        elif diagnosis["has_behavior"] and not diagnosis["has_scene"]:
            return "你打算在什么场景下用这个？（工作/学习/个人项目/其他）"
        else:
            return "你现在是有一个具体的想法，还是还在探索阶段？"


# 测试代码
if __name__ == "__main__":
    diagnoser = ClarityDiagnosis()

    test_cases = [
        "帮我写一篇介绍我的基金筛选工具的文章，发小红书",
        "我想学Python",
        "我想做点什么但不知道做什么",
        "帮我写一篇文章",
        "我不知道未来干什么"
    ]

    for case in test_cases:
        print(f"\n输入: {case}")
        result = diagnoser.diagnose(case)
        print(f"结果: {result}")
        if result["is_clear"] is None:
            print(f"验证问题: {diagnoser.generate_verification_question(result)}")
