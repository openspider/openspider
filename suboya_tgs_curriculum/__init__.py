"""
Suboya TGS Curriculum - Main Entry Point
苏柏亚真善美精神课程系统 - 主入口
"""

from .core.tgs_core import (
    TGSCore,
    SocraticModule,
    PlatonicModule,
    AristotelianModule,
    Philosopher,
    Dimension,
    WisdomInsight,
    TGSEvaluation,
    create_tgs_explorer
)

from .agents.socratic_agent import SocraticAgent
from .agents.platonic_agent import PlatonicAgent
from .agents.aristotelian_agent import AristotelianAgent
from .agents.tgs_integrator import TGSIntegrator

__version__ = "1.0.0"
__author__ = "NRT OpenSpider Team"

__all__ = [
    'TGSCore',
    'SocraticModule',
    'PlatonicModule', 
    'AristotelianModule',
    'Philosopher',
    'Dimension',
    'WisdomInsight',
    'TGSEvaluation',
    'create_tgs_explorer',
    'SocraticAgent',
    'PlatonicAgent',
    'AristotelianAgent',
    'TGSIntegrator'
]


def create_curriculum_explorer(mode: str = "integrated") -> TGSCore:
    """
    创建课程探索者
    
    Args:
        mode: 模式 ("socratic", "platonic", "aristotelian", "integrated")
        
    Returns:
        TGSCore实例
    """
    return TGSCore(mode=mode)
