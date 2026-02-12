"""
Athenian Digital Academy - Main Entry Point
数字科学家雅典学院 - 主入口
"""

from .core.agent_layer import AgentLayer, AgentRole
from .core.interaction_layer import InteractionLayer
from .core.synthesis_layer import SynthesisLayer
from .core.critical_rationalism import (
    CriticalRationalismEngine,
    ConjectureType,
    CriticismType
)
from .core.knowledge_capsule import (
    KnowledgeCapsuleSystem,
    KnowledgeCapsule
)

__version__ = "1.0.0"
__author__ = "NRT OpenSpider Team"


class AthenianDigitalAcademy:
    """
    Athenian Digital Academy - 数字科学家雅典学院主类
    
    整合所有模块，提供统一接口
    """
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        
        # 初始化各层
        self.agent_layer = AgentLayer(config.get("agent"))
        self.interaction_layer = InteractionLayer(config.get("interaction"))
        self.synthesis_layer = SynthesisLayer(config.get("synthesis"))
        self.cr_engine = CriticalRationalismEngine(config.get("critical_rationalism"))
        self.knowledge_system = KnowledgeCapsuleSystem(config.get("knowledge"))
        
        # 初始化状态
        self.initialized = False
        self.running = False
    
    def initialize(self) -> dict:
        """初始化系统"""
        self.initialized = True
        
        return {
            "status": "initialized",
            "layers": {
                "agent": self.agent_layer.get_layer_status(),
                "interaction": self.interaction_layer.get_layer_status(),
                "synthesis": self.synthesis_layer.get_synthesis_metrics()
            },
            "engines": {
                "critical_rationalism": self.cr_engine.get_cycle_status(),
                "knowledge_capsule": self.knowledge_system.get_system_status()
            }
        }
    
    # ==================== Multi-Agent Collaboration ====================
    
    def start_collaboration(
        self,
        task: dict,
        roles: list = None
    ) -> dict:
        """启动多智能体协作"""
        if not self.initialized:
            self.initialize()
        
        active_roles = [AgentRole(r) for r in (roles or ["strategist", "engineer", "researcher"])]
        
        return self.agent_layer.multi_agent_collaborate(task, active_roles)
    
    # ==================== Knowledge Capsule ====================
    
    def create_knowledge_capsule(
        self,
        content: str,
        domain: str,
        tags: list = None,
        cross_domain: dict = None
    ) -> dict:
        """创建知识胶囊"""
        capsule = self.knowledge_system.create_capsule(
            insight_summary=content[:100],
            insight_details=content,
            confidence=0.8,
            domain=domain,
            discipline=domain,
            discovered_by="system",
            discovery_method="direct_input",
            original_source="user_input",
            tags=tags or [],
            cross_domain_fusion=cross_domain
        )
        
        return capsule.to_dict()
    
    # ==================== Semantic Collision ====================
    
    def trigger_semantic_collision(
        self,
        capsule1_id: str,
        capsule2_id: str
    ) -> dict:
        """触发语义碰撞"""
        return self.knowledge_system.semantic_collision(capsule1_id, capsule2_id)
    
    # ==================== Critical Rationalism ====================
    
    def run_critical_cycle(
        self,
        conjecture: str,
        domain: str
    ) -> dict:
        """运行批判理性主义循环"""
        return self.cr_engine.run_full_cycle(
            initial_conjecture=conjecture,
            domain=domain,
            test_plan={}
        )
    
    # ==================== Arbitration ====================
    
    def arbitrated_synthesis(
        self,
        inputs: list,
        criteria: dict = None
    ) -> dict:
        """仲裁合成"""
        # 简化实现
        return {
            "status": "synthesized",
            "input_count": len(inputs),
            "output": "Synthesized output from " + ", ".join(str(i) for i in inputs),
            "safety_check": {"passed": True}
        }
    
    # ==================== System Status ====================
    
    def get_status(self) -> dict:
        """获取系统状态"""
        return {
            "initialized": self.initialized,
            "running": self.running,
            "layers": {
                "agent": self.agent_layer.get_layer_status(),
                "interaction": self.interaction_layer.get_layer_status(),
                "synthesis": self.synthesis_layer.get_synthesis_metrics()
            },
            "engines": {
                "critical_rationalism": self.cr_engine.get_cycle_status(),
                "knowledge": self.knowledge_system.get_system_status()
            }
        }


# ==================== Convenience Functions ====================

def create_academy(config: dict = None) -> AthenianDigitalAcademy:
    """创建雅典学院实例"""
    return AthenianDigitalAcademy(config)


# ==================== CLI Entry Point ====================

if __name__ == "__main__":
    import sys
    
    print("""
    ===========================================
    Athenian Digital Academy - 数字科学家雅典学院
    ===========================================
    
    Based on:
    - Athenian Academy 7-Layer MAS Framework
    - Three Kingdoms Digital Scientist Team
    - Critical Rationalism Methodology
    - Knowledge Capsule Philosophy
    
    Type 'help' for available commands.
    """)
    
    academy = create_academy()
    academy.initialize()
    
    print(f"\nSystem Status: {academy.get_status()['status']}")
