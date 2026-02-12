"""
TGS Integrator - 真善美整合者

整合苏格拉底、柏拉图、亚里士多德的智慧
"""

from typing import Dict, List, Any
from .socratic_agent import SocraticAgent
from .platonic_agent import PlatonicAgent
from .aristotelian_agent import AristotelianAgent


class TGSIntegrator:
    """
    真善美整合者
    
    整合三位古典哲学家的智慧，提供全面的分析和评估
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.socratic = SocraticAgent()
        self.platonic = PlatonicAgent()
        self.aristotelian = AristotelianAgent()
        self.dialogue_history = []
    
    def welcome(self) -> str:
        """欢迎"""
        return """
        🏛️⚖️👋 欢迎来到苏柏亚真善美智慧殿堂！
        
        我整合了三位伟大哲学家的智慧：
        
        👤 苏格拉底 - 批判性思维的追问者
           通过问答法引导你思考
        
        🏛️ 柏拉图 - 理想形式的探索者
           帮助你洞见事物的本质
        
        ⚖️ 亚里士多德 - 逻辑与伦理的分析者
           用理性指导实践
        
        请选择你想讨论的话题，我们将开始探索真理之路。
        """
    
    def comprehensive_analysis(self, topic: str) -> Dict:
        """
        综合分析
        
        从三个维度全面分析话题
        """
        # 苏格拉底的批判性分析
        socratic = {
            "approach": "苏格拉底式问答",
            "questions": self.socratic.ask_question(topic, depth=3),
            "reflection": self.socratic.reflect(topic),
            "truth_guidance": self.socratic.guide_to_truth(topic)
        }
        
        # 柏拉图的形式分析
        platonic = {
            "approach": "柏拉图式形式论",
            "form_analysis": self.platonic.extract_form(topic),
            "cave_reflection": self.platonic.cave_analogy(topic),
            "dialectic_method": [
                "收集具体例子",
                "上升到抽象形式",
                "检验一致性",
                "理解形式关系",
                "理解善的形式"
            ]
        }
        
        # 亚里士多德的逻辑分析
        aristotelian = {
            "approach": "亚里士多德式分析",
            "syllogism": self.aristotelian.syllogize(
                f"对「{topic}」的理性思考是正确的",
                f"「{topic}」值得深入探讨"
            ),
            "virtue_analysis": self.aristotelian.golden_mean(topic),
            "causal_analysis": self.aristotelian.causal_analysis(topic)
        }
        
        # 综合结果
        result = {
            "topic": topic,
            "socratic": socratic,
            "platonary": platonic,
            "aristotelian": aristotelian,
            "synthesis": self._synthesize(topic, socratic, platonic, aristotelian),
            "timestamp": self._get_timestamp()
        }
        
        # 记录对话
        self.dialogue_history.append(result)
        
        return result
    
    def _synthesize(
        self, 
        topic: str, 
        socratic: Dict, 
        platonic: Dict, 
        aristotelian: Dict
    ) -> Dict:
        """
        综合分析结果
        """
        return {
            "topic": topic,
            "truth_perspective": {
                "socratic": "通过追问发现真理",
                "platonary": "通过形式论理解本质",
                "aristotelian": "通过逻辑推理得出结论",
                "synthesis": "综合三方观点，真理需要追问+形式+逻辑"
            },
            "goodness_perspective": {
                "ethical_virtue": "德性的培养",
                "practical_wisdom": "实践智慧的应用",
                "eudaimonia": "追求人的繁荣/幸福"
            },
            "beauty_perspective": {
                "harmony": "理性、意志、欲望的和谐",
                "form_beauty": "形式的美",
                "intellectual_joy": "追求智慧的喜悦"
            },
            "integrated_insight": f"""
            关于「{topic}」：
            
            1. 真：通过苏格拉底式的追问，我们发现...
               通过柏拉图的形式论，我们理解...
               通过亚里士多德的逻辑，我们得出结论...
            
            2. 善：这个认识如何指导我们的行动？
               我们应该以中庸之道来实践...
            
            3. 美：最终，这种理解带来的是...
               理性与美德的和谐统一...
            """
        }
    
    def dialogue(self, user_input: str) -> Dict:
        """
        智能对话
        
        根据用户输入选择合适的分析方法
        """
        # 分析用户意图
        intent = self._analyze_intent(user_input)
        
        if intent == "questioning":
            # 苏格拉底式问答
            result = self.socratic.dialogue(user_input)
            result["type"] = "socratic"
        elif intent == "formal":
            # 柏拉图式分析
            result = self.platonic.discuss(user_input)
            result["type"] = "platonic"
        elif intent == "logical":
            # 亚里士多德式分析
            result = self.aristotelian.analyze(user_input)
            result["type"] = "aristotelian"
        else:
            # 综合分析
            result = self.comprehensive_analysis(user_input)
            result["type"] = "integrated"
        
        return result
    
    def _analyze_intent(self, text: str) -> str:
        """
        分析用户意图
        
        简化版本：基于关键词判断
        """
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["为什么", "是否", "怎么", "what", "why", "how"]):
            return "questioning"
        elif any(kw in text_lower for kw in ["本质", "形式", "理想", "nature", "form", "ideal"]):
            return "formal"
        elif any(kw in text_lower for kw in ["逻辑", "推理", "所以", "logic", "therefore"]):
            return "logical"
        else:
            return "integrated"
    
    def evaluate_tgs(self, content: str) -> Dict:
        """
        真善美评估
        
        评估内容的真善美得分
        """
        # 简化的评估实现
        return {
            "truth_score": 0.85,    # 真
            "goodness_score": 0.90,  # 善
            "beauty_score": 0.88,     # 美
            "overall_score": (0.85 + 0.90 + 0.88) / 3,
            "analysis": {
                "truth": "批判性思维和逻辑一致性",
                "goodness": "伦理合规性和包容性",
                "beauty": "智慧整合和涌现创新"
            }
        }
    
    def get_status(self) -> Dict:
        """获取整合者状态"""
        return {
            "status": "active",
            "socratic": self.socratic.get_status(),
            "platonary": self.platonic.get_status(),
            "aristotelian": self.aristotelian.get_status(),
            "dialogues": len(self.dialogue_history),
            "integrator": "苏柏亚真善美整合者"
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


if __name__ == "__main__":
    print("=" * 60)
    print("🌟 苏柏亚真善美整合者演示")
    print("=" * 60)
    
    integrator = TGSIntegrator()
    
    print(integrator.welcome())
    
    print("\n📚 综合分析演示 - 关于「正义」:")
    result = integrator.comprehensive_analysis("正义")
    
    print(f"\n📌 苏格拉底式提问:")
    for q in result["socratic"]["questions"][:2]:
        print(f"  • {q}")
    
    print(f"\n🏛️ 柏拉图形式分析:")
    form = result["platonary"]["form_analysis"]
    print(f"  理想形式: {form['ideal_form']}")
    
    print(f"\n⚖️ 亚里士多德中庸分析:")
    mean = result["aristotelian"]["virtue_analysis"]
    print(f"  美德: {mean['virtue']}")
    print(f"  中庸: {mean['mean']}")
    
    print("\n🌟 真善美评估:")
    eval_result = integrator.evaluate_tgs("测试内容")
    print(f"  真 (Truth): {eval_result['truth_score']:.2f}")
    print(f"  善 (Goodness): {eval_result['goodness_score']:.2f}")
    print(f"  美 (Beauty): {eval_result['beauty_score']:.2f}")
    
    print("\n📊 整合者状态:")
    status = integrator.get_status()
    print(f"  对话数: {status['dialogues']}")
