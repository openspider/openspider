"""
Competition System - 比赛系统
"""

from .core.competition_manager import (
    CompetitionManager,
    Competition,
    Team,
    ScoringResult,
    create_competition_manager
)

__version__ = "1.0.0"
__author__ = "NRT OpenSpider Team"

__all__ = [
    'CompetitionManager',
    'Competition',
    'Team',
    'ScoringResult',
    'create_competition_manager'
]
