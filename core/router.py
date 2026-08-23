# -*- coding: utf-8 -*-
"""统一路由层：把清晰度、任务类型和障碍状态收敛成下一步产品行为。"""

from core.diagnosis import ClarityDiagnosis
from core.question_generator import QuestionGenerator
from core.state_detector import StateDetector
from core.task_classifier import TaskClassifier


class IntentRouter:
    """避免单一关键词模块直接决定完整对话路径。"""

    def __init__(self):
        self.diagnoser = ClarityDiagnosis()
        self.classifier = TaskClassifier()
        self.question_generator = QuestionGenerator()
        self.state_detector = StateDetector()

    def analyze(self, user_input):
        """返回可供 Skill 或上层应用使用的统一判断摘要。"""
        diagnosis = self.diagnoser.diagnose(user_input)
        task = self.classifier.classify(user_input)
        obstacle = self.question_generator.classify_obstacle(user_input)
        state = self.state_detector.detect(user_input)
        route, reason = self._choose_route(diagnosis, task, obstacle, user_input)

        return {
            "clarity": diagnosis["clarity"],
            "task_type": task["task_type"],
            "user_state": state["state"],
            "obstacle_type": obstacle,
            "missing_dimensions": diagnosis["missing_dimensions"],
            "route": route,
            "reason": reason,
        }

    def _choose_route(self, diagnosis, task, obstacle, user_input):
        task_type = task["task_type"]

        # 已知失败现象需要先收集排查信息，而非被“产品/代码”等名词带偏。
        if task_type == "问题诊断":
            return "problem_diagnosis", "用户已描述失败现象，先定位原因"

        # 决策题与执行困惑都已有可行动对象，不应被不确定词送入泛化探索。
        if task_type == "辅助决策":
            return "quick_clarify", "先补齐选项、标准和约束"
        if obstacle == "execution_confusion":
            return "quick_clarify", "用户缺少起步路径，不做心理障碍深挖"

        # “我想创业”属于高风险但方向尚未落地的表达。首轮只确认
        # 是否已有具体方向；根据回答再进入快速澄清或深度探索。
        if self.question_generator.detect_high_freq_scenario(user_input) == "创业":
            return "quick_clarify", "先确认创业方向是否具体"

        # 缺少待处理材料时，索取材料本身就是直接推进任务，不属于需求探索。
        if self._is_material_request(user_input):
            return "direct_execution", "先索取完成任务必需的原始材料"

        if diagnosis["clarity"] == "unclear":
            return "deep_exploration", "缺少可行动方向，需要先理解用户状态"
        if diagnosis["clarity"] == "clear":
            return "direct_execution", "关键信息已经足够，直接开始"
        return "quick_clarify", "已有行动意图，只补充最关键的执行信息"

    @staticmethod
    def _is_material_request(user_input):
        text = user_input.lower()
        task_words = ("润色", "改写", "翻译", "总结", "提取")
        reference_words = ("这段", "以下", "这篇", "这份")
        return any(word in text for word in task_words) and any(
            word in text for word in reference_words
        )
