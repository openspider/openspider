"""
Socratic Agent - 苏格拉底智能体

实现苏格拉底式对话和批判性思维
"""

from typing import Dict, List, Any


class SocraticAgent:
    """
    苏格拉底智能体
    
    通过提问引导思考，培养批判性思维
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = "苏格拉底"
        self.role = "批判性思维引导者"
        self.dialogue_history = []
    
    def greet(self) -> str:
        """问候"""
        return """
        👋 你好！我是苏格拉底。
        
        我相信"未经审视的人生不值得过"。
        让我们通过对话来探索真理。
        
        请告诉我你想讨论的话题。
        """
    
    def ask_question(self, topic: str, depth: int = 3) -> List[str]:
        """
        深度提问
        
        针对话题进行层层深入的追问
        """
        questions = []
        
        # 第一层：定义
        questions.append(f"「{topic}」这个词对你来说意味着什么？")
        
        # 第二层：理由
        questions.append(f"为什么你认为「{topic}」是这样的？")
        
        # 第三层：反面
        questions.append(f"如果有人不同意你的观点，他们会说什么？")
        
        # 第四层：应用
        questions.append(f"「{topic}」在日常生活中是如何体现的？")
        
        return questions[:depth]
    
    def dialogue(self, user_input: str) -> Dict:
        """
        苏格拉底式对话
        
        对用户输入进行分析和追问
        """
        # 分析输入
        analysis = {
            "input": user_input,
            "assumptions": [],
            "implications": [],
            "questions": self.ask_question(user_input)
        }
        
        # 记录对话
        self.dialogue_history.append({
            "user": user_input,
            "analysis": analysis,
            "timestamp": self._get_timestamp()
        })
        
        return analysis
    
    def reflect(self, statement: str) -> Dict:
        """
        反思性回应
        
        温和但深入地质疑
        """
        return {
            "type": "reflection",
            "statement": statement,
            "question": f"我想更了解你的观点。「{statement}」——你为什么这么认为？",
            "guidance": "让我们一起探索这个问题的本质。"
        }
    
    def guide_to_truth(self, topic: str) -> Dict:
        """
        真理引导
        
        引导用户接近真理
        """
        return {
            "topic": topic,
            "method": "问答法",
            "steps": [
                "澄清概念：明确「{topic}」的含义",
                "检验假设：什么是你认为理所当然的？",
                "寻找证据：有什么支持你的观点？",
                "考虑反面：如果相反的情况成立呢？",
                "得出结论：基于以上分析，真理是什么？"
            ],
            "final_question": f"经过这番讨论，你对「{topic}」有什么新的理解？"
        }
    
    def get_status(self) -> Dict:
        """获取智能体状态"""
        return {
            "name": self.name,
            "role": self.role,
            "dialogues": len(self.dialogue_history),
            "status": "active"
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


if __name__ == "__main__":
    print("=" * 60)
    print("👤 苏格拉底智能体演示")
    print("=" * 60)
    
    agent = SocraticAgent()
    
    print(agent.greet())
    
    print("\n📚 关于「正义」的深度提问:")
    questions = agent.ask_question("正义", depth=4)
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    
    print("\n🌟 真理引导:")
    guide = agent.guide_to_truth("正义")
    for step in guide["steps"][:2]:
        print(f"  • {step}")
    
    print("\n📊 智能体状态:")
    status = agent.get_status()
    print(f"  名称: {status['name']}")
    print(f"  角色: {status['role']}")
    print(f"  对话数: {status['dialogues']}")
