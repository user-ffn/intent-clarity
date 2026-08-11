# -*- coding: utf-8 -*-
"""
任务类型分类模块
将明确的需求分类到5种任务类型
"""


class TaskClassifier:
    """任务类型分类器"""

    # 5种任务类型的关键词
    TASK_PATTERNS = {
        "获取信息": {
            "keywords": [
                "是什么", "什么是", "怎么回事", "为什么",
                "介绍", "解释", "说明", "讲讲",
                "有哪些", "列举", "查", "找"
            ],
            "description": "用户想了解/查询信息"
        },

        "生成内容": {
            "keywords": [
                "写", "生成", "创作", "编写",
                "文章", "报告", "代码", "脚本",
                "方案", "策划", "文案", "故事",
                "翻译", "润色", "改写"
            ],
            "description": "用户想生成具体内容（文章/代码/文案等）"
        },

        "制定路径": {
            "keywords": [
                "学", "掌握", "入门", "提升",
                "计划", "安排", "步骤", "roadmap",
                "怎么学", "如何学", "从哪开始",
                "学习路线", "行动计划"
            ],
            "description": "用户想要学习计划或行动步骤"
        },

        "辅助决策": {
            "keywords": [
                "选", "选择", "还是", "或者",
                "应该", "要不要", "值得", "建议",
                "对比", "比较", "哪个好", "推荐",
                "纠结", "犹豫"
            ],
            "description": "用户面临多个选项，需要帮助决策"
        },

        "创造设计": {
            "keywords": [
                "设计", "做一个", "开发", "搭建",
                "产品", "系统", "工具", "应用",
                "网站", "App", "小程序",
                "架构", "方案", "需求"
            ],
            "description": "用户想从0到1创造一个产品/系统"
        }
    }

    def classify(self, user_input):
        """
        分类任务类型

        返回：
        {
            "task_type": str,  # 5种类型之一，或"未分类"
            "confidence": float,  # 置信度 0-1
            "matched_keywords": list  # 匹配到的关键词
        }
        """
        user_input = user_input.lower()
        scores = {}

        # 对每种类型计算匹配分数
        for task_type, config in self.TASK_PATTERNS.items():
            matched = [
                kw for kw in config["keywords"]
                if kw in user_input
            ]
            scores[task_type] = len(matched)

        # 找到最高分
        if not any(scores.values()):
            return {
                "task_type": "未分类",
                "confidence": 0.0,
                "matched_keywords": []
            }

        max_score = max(scores.values())
        task_type = max(scores, key=scores.get)

        # 计算置信度
        confidence = min(max_score * 0.3, 1.0)  # 每个匹配词+0.3，最高1.0

        matched_keywords = [
            kw for kw in self.TASK_PATTERNS[task_type]["keywords"]
            if kw in user_input
        ]

        return {
            "task_type": task_type,
            "confidence": confidence,
            "matched_keywords": matched_keywords
        }

    def get_clarity_standards(self, task_type):
        """
        根据任务类型返回清晰度标准

        每种任务需要确认的字段不同
        """
        standards = {
            "获取信息": ["要了解什么", "了解到什么程度"],
            "生成内容": ["受众是谁", "主题/内容", "格式/长度"],
            "制定路径": ["目标是什么", "当前水平", "时间预算"],
            "辅助决策": ["有哪些选项", "决策标准", "约束条件"],
            "创造设计": ["目标用户", "核心功能", "资源约束"]
        }

        return standards.get(task_type, ["目标", "要求", "场景"])

    def get_output_format(self, task_type):
        """
        根据任务类型返回输出格式说明
        """
        formats = {
            "获取信息": "直接回答问题，分点说明",
            "生成内容": "直接生成完整内容（文章/代码/文案）",
            "制定路径": "结构化的学习计划或行动步骤",
            "辅助决策": "选项对比分析 + 推荐意见",
            "创造设计": "需求分析 → 方案设计 → MVP建议"
        }

        return formats.get(task_type, "根据需求直接输出结果")


# 测试代码
if __name__ == "__main__":
    classifier = TaskClassifier()

    test_cases = [
        "帮我写一篇介绍我的基金筛选工具的文章",
        "Python和JavaScript哪个更适合我学",
        "给我一个学Python的计划",
        "什么是RESTful API",
        "我想做一个任务管理App"
    ]

    for case in test_cases:
        print(f"\n输入: {case}")
        result = classifier.classify(case)
        print(f"任务类型: {result['task_type']} (置信度: {result['confidence']:.2f})")
        if result['task_type'] != "未分类":
            print(f"清晰度标准: {classifier.get_clarity_standards(result['task_type'])}")
            print(f"输出格式: {classifier.get_output_format(result['task_type'])}")
