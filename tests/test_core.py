# -*- coding: utf-8 -*-
"""Intent Clarity 核心规则的可重复验收。"""

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.diagnosis import ClarityDiagnosis  # noqa: E402
from core.question_generator import QuestionGenerator  # noqa: E402
from core.router import IntentRouter  # noqa: E402
from core.task_classifier import TaskClassifier  # noqa: E402
from evaluation.build_cases import parse_cases  # noqa: E402


class CoreRoutingTests(unittest.TestCase):
    def test_problem_symptom_has_diagnostic_priority(self):
        result = TaskClassifier().classify("我的产品没人用")
        self.assertEqual(result["task_type"], "问题诊断")

    def test_product_creation_stays_creation_task(self):
        result = TaskClassifier().classify("我想做一个任务管理App")
        self.assertEqual(result["task_type"], "创造设计")

    def test_diagnosis_exposes_missing_dimensions_and_route(self):
        result = ClarityDiagnosis().diagnose("帮我写一篇文章")
        self.assertIn("missing_dimensions", result)
        self.assertIn("clarity", result)
        self.assertIn("route", result)
        self.assertEqual(result["route"], "quick_clarify")

    def test_router_keeps_decision_out_of_deep_exploration(self):
        result = IntentRouter().analyze("我要不要考研")
        self.assertEqual(result["task_type"], "辅助决策")
        self.assertEqual(result["route"], "quick_clarify")

    def test_router_prioritizes_problem_diagnosis(self):
        result = IntentRouter().analyze("我的产品没人用")
        self.assertEqual(result["task_type"], "问题诊断")
        self.assertEqual(result["route"], "problem_diagnosis")

    def test_router_treats_execution_confusion_as_quick_clarify(self):
        result = IntentRouter().analyze("我想自学编程，但不知道从哪开始")
        self.assertEqual(result["route"], "quick_clarify")

    def test_router_requests_missing_material_without_exploration(self):
        result = IntentRouter().analyze("帮我润色这段文字")
        self.assertEqual(result["route"], "direct_execution")

    def test_router_explores_vague_desire_before_recommending(self):
        result = IntentRouter().analyze("我想做点事情")
        self.assertEqual(result["route"], "deep_exploration")

    def test_router_checks_whether_entrepreneurship_has_a_concrete_direction(self):
        result = IntentRouter().analyze("我想创业")
        self.assertEqual(result["route"], "quick_clarify")


class QuestionPolicyTests(unittest.TestCase):
    def test_diagnostic_questions_are_prioritized(self):
        questions = QuestionGenerator().get_priority_questions(
            "问题诊断", {}, "我的产品没人用"
        )
        self.assertEqual(len(questions), 1)
        self.assertIn("具体情况", questions[0])

    def test_execution_confusion_is_not_real_obstacle(self):
        generator = QuestionGenerator()
        self.assertEqual(
            generator.classify_obstacle("我想学编程，但不知道从哪开始"),
            "execution_confusion",
        )
        self.assertEqual(
            generator.classify_obstacle("我一直想学编程，但不敢开始"),
            "real_obstacle",
        )


class EvaluationDatasetTests(unittest.TestCase):
    def test_legacy_acceptance_set_is_structured_into_50_cases(self):
        source = (ROOT / "test-cases.md").read_text(encoding="utf-8")
        cases = parse_cases(source)
        self.assertEqual(len(cases), 50)
        self.assertTrue(all(case["input"] for case in cases))
        self.assertTrue(all("expected_route" in case for case in cases))


if __name__ == "__main__":
    unittest.main(verbosity=2)
