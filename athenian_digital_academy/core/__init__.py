"""
Athenian Digital Academy - Core Engine
数字科学家雅典学院 - 核心引擎

基于雅典学院7层MAS框架 + 三国数字科学家团队 + 批判理性主义方法论
"""

from .agent_layer import AgentLayer
from .interaction_layer import InteractionLayer
from .synthesis_layer import SynthesisLayer
from .critical_rationalism import CriticalRationalismEngine
from .knowledge_capsule import KnowledgeCapsuleSystem

__all__ = [
    'AgentLayer',
    'InteractionLayer', 
    'SynthesisLayer',
    'CriticalRationalismEngine',
    'KnowledgeCapsuleSystem'
]
