"""
Digital Scientists - Unified Entry Point
数字科学家套件 - 统一入口

整合所有数字科学家类型
"""

from .suboya_ai_scientist import (
    SuboyaAIScientist,
    create_suboya_scientist
)

from .industry_scientist import (
    IndustryScientist,
    create_industry_scientist
)

from .academic_scientist import (
    AcademicScientist,
    create_academic_scientist
)

from .research_scientist import (
    ResearchScientist,
    create_research_scientist
)

__version__ = "1.0.0"
__author__ = "NRT OpenSpider Team"

__all__ = [
    'SuboyaAIScientist',
    'create_suboya_scientist',
    'IndustryScientist',
    'create_industry_scientist',
    'AcademicScientist',
    'create_academic_scientist',
    'ResearchScientist',
    'create_research_scientist'
]
