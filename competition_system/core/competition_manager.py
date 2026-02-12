"""
Competition System Core - 比赛系统核心
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


class CompetitionStatus(Enum):
    """比赛状态"""
    DRAFT = "draft"         # 草稿
    OPEN = "open"           # 开放报名
    IN_PROGRESS = "ongoing" # 进行中
    CLOSED = "closed"       # 已结束
    EVALUATING = "evaluating"  # 评审中
    COMPLETED = "completed"   # 已完成


class Track(Enum):
    """赛道"""
    RESEARCH = "research"     # 科研
    INDUSTRY = "industry"     # 产业
    INNOVATION = "innovation" # 创新


@dataclass
class Competition:
    """比赛"""
    id: str
    name: str
    description: str
    track: str
    status: str
    start_date: str
    end_date: str
    max_participants: int
    entry_fee: float
    prizes: Dict
    evaluation_criteria: Dict
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "track": self.track,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "max_participants": self.max_participants,
            "entry_fee": self.entry_fee,
            "prizes": self.prizes,
            "evaluation_criteria": self.evaluation_criteria
        }


@dataclass
class Team:
    """参赛团队"""
    id: str
    name: str
    members: List[str]
    competition_id: str
    submission: Dict = None
    score: float = 0.0
    rank: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "members": self.members,
            "competition_id": self.competition_id,
            "submission": self.submission,
            "score": self.score,
            "rank": self.rank
        }


@dataclass
class ScoringResult:
    """评分结果"""
    competition_id: str
    team_id: str
    scores: Dict[str, float]
    total_score: float
    rank: int
    feedback: str
    
    def to_dict(self) -> Dict:
        return {
            "competition_id": self.competition_id,
            "team_id": self.team_id,
            "scores": self.scores,
            "total_score": self.total_score,
            "rank": self.rank,
            "feedback": self.feedback
        }


class CompetitionManager:
    """
    比赛管理器
    
    管理比赛全流程
    """
    
    def __init__(self):
        self.competitions: Dict[str, Competition] = {}
        self.teams: Dict[str, Team] = {}
        self.results: Dict[str, ScoringResult] = {}
        self._init_sample_competitions()
    
    def _init_sample_competitions(self):
        """初始化示例比赛"""
        sample_comps = [
            Competition(
                id="paper_sprint_2026_01",
                name="论文冲刺赛 Q1",
                description="1个月内发表1篇顶会论文",
                track=Track.RESEARCH.value,
                status=CompetitionStatus.OPEN.value,
                start_date="2026-01-15",
                end_date="2026-01-31",
                max_participants=50,
                entry_fee=0,
                prizes={
                    "gold": {"cash": 100000, "title": "论文之星"},
                    "silver": {"cash": 50000, "title": "优秀论文"},
                    "bronze": {"cash": 20000, "title": "潜力论文"}
                },
                evaluation_criteria={
                    "publication_quality": 0.40,
                    "innovation": 0.30,
                    "methodology": 0.20,
                    "writing": 0.10
                }
            ),
            Competition(
                id="industry_analysis_2026_01",
                name="产业分析赛 Q1",
                description="2周完成深度产业分析报告",
                track=Track.INDUSTRY.value,
                status=CompetitionStatus.OPEN.value,
                start_date="2026-01-20",
                end_date="2026-02-03",
                max_participants=100,
                entry_fee=0,
                prizes={
                    "gold": {"cash": 50000, "title": "产业洞察专家"},
                    "silver": {"cash": 20000, "title": "优秀分析师"},
                    "bronze": {"cash": 10000, "title": "潜力分析师"}
                },
                evaluation_criteria={
                    "analysis_depth": 0.30,
                    "insight_quality": 0.30,
                    "business_acumen": 0.25,
                    "presentation": 0.15
                }
            ),
            Competition(
                id="innovation_sprint_2026_01",
                name="创意热身赛 Q1",
                description="1周内生成3个创新方案",
                track=Track.INNOVATION.value,
                status=CompetitionStatus.OPEN.value,
                start_date="2026-01-25",
                end_date="2026-01-31",
                max_participants=200,
                entry_fee=0,
                prizes={
                    "gold": {"cash": 30000, "title": "创新先锋"},
                    "silver": {"cash": 10000, "title": "创意达人"},
                    "bronze": {"cash": 5000, "title": "创新新星"}
                },
                evaluation_criteria={
                    "novelty": 0.40,
                    "feasibility": 0.30,
                    "impact": 0.20,
                    "presentation": 0.10
                }
            )
        ]
        
        for comp in sample_comps:
            self.competitions[comp.id] = comp
    
    # ==================== 比赛管理 ====================
    
    def create_competition(self, config: Dict) -> Competition:
        """创建比赛"""
        comp = Competition(
            id=f"comp_{hash(config['name']) % 10000}",
            name=config["name"],
            description=config.get("description", ""),
            track=config.get("track", Track.INNOVATION.value),
            status=CompetitionStatus.DRAFT.value,
            start_date=config.get("start_date", ""),
            end_date=config.get("end_date", ""),
            max_participants=config.get("max_participants", 100),
            entry_fee=config.get("entry_fee", 0),
            prizes=config.get("prizes", {}),
            evaluation_criteria=config.get("evaluation_criteria", {})
        )
        self.competitions[comp.id] = comp
        return comp
    
    def list_competitions(
        self, 
        status: str = None, 
        track: str = None
    ) -> List[Competition]:
        """列出比赛"""
        result = list(self.competitions.values())
        
        if status:
            result = [c for c in result if c.status == status]
        if track:
            result = [c for c in result if c.track == track]
        
        return result
    
    def get_competition(self, competition_id: str) -> Competition:
        """获取比赛"""
        return self.competitions.get(competition_id)
    
    def open_registration(self, competition_id: str) -> bool:
        """开放报名"""
        comp = self.competitions.get(competition_id)
        if comp:
            comp.status = CompetitionStatus.OPEN.value
            return True
        return False
    
    def start_competition(self, competition_id: str) -> bool:
        """开始比赛"""
        comp = self.competitions.get(competition_id)
        if comp:
            comp.status = CompetitionStatus.IN_PROGRESS.value
            return True
        return False
    
    def close_competition(self, competition_id: str) -> bool:
        """结束比赛"""
        comp = self.competitions.get(competition_id)
        if comp:
            comp.status = CompetitionStatus.CLOSED.value
            return True
        return False
    
    # ==================== 参赛管理 ====================
    
    def enter(
        self, 
        competition_id: str, 
        team_name: str,
        members: List[str]
    ) -> Team:
        """参赛"""
        team = Team(
            id=f"team_{hash(team_name) % 10000}",
            name=team_name,
            members=members,
            competition_id=competition_id
        )
        self.teams[team.id] = team
        return team
    
    def submit(
        self, 
        team_id: str,
        deliverable: Dict,
        description: str = ""
    ) -> bool:
        """提交作品"""
        team = self.teams.get(team_id)
        if team:
            team.submission = {
                "deliverable": deliverable,
                "description": description,
                "timestamp": datetime.now().isoformat()
            }
            return True
        return False
    
    def withdraw(self, team_id: str) -> bool:
        """退出"""
        if team_id in self.teams:
            del self.teams[team_id]
            return True
        return False
    
    # ==================== 评分系统 ====================
    
    def evaluate(
        self, 
        competition_id: str, 
        team_id: str,
        scores: Dict[str, float],
        feedback: str = ""
    ) -> ScoringResult:
        """评分"""
        comp = self.competitions.get(competition_id)
        team = self.teams.get(team_id)
        
        if not comp or not team:
            return None
        
        # 计算总分
        total = 0
        for criterion, weight in comp.evaluation_criteria.items():
            if criterion in scores:
                total += scores[criterion] * weight
        
        result = ScoringResult(
            competition_id=competition_id,
            team_id=team_id,
            scores=scores,
            total_score=total,
            rank=0,  # 待计算
            feedback=feedback
        )
        
        self.results[f"{competition_id}_{team_id}"] = result
        team.score = total
        
        return result
    
    def calculate_rankings(self, competition_id: str) -> List[Team]:
        """计算排名"""
        teams = [t for t in self.teams.values() if t.competition_id == competition_id]
        teams.sort(key=lambda t: t.score, reverse=True)
        
        for i, team in enumerate(teams, 1):
            team.rank = i
        
        return teams
    
    def get_results(
        self, 
        competition_id: str, 
        top_n: int = 10
    ) -> List[ScoringResult]:
        """获取结果"""
        results = []
        for key, result in self.results.items():
            if key.startswith(competition_id):
                results.append(result)
        
        results.sort(key=lambda r: r.total_score, reverse=True)
        return results[:top_n]
    
    # ==================== 统计系统 ====================
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        total_comps = len(self.competitions)
        active_comps = len([c for c in self.competitions.values() if c.status == "open"])
        total_teams = len(self.teams)
        
        # 按赛道统计
        track_stats = {}
        for comp in self.competitions.values():
            track = comp.track
            if track not in track_stats:
                track_stats[track] = 0
            track_stats[track] += 1
        
        return {
            "total_competitions": total_comps,
            "active_competitions": active_comps,
            "total_teams": total_teams,
            "by_track": track_stats,
            "system_status": "operational"
        }
    
    def get_leaderboard(self, track: str = None) -> List[Team]:
        """排行榜"""
        teams = list(self.teams.values())
        teams.sort(key=lambda t: t.score, reverse=True)
        
        if track:
            comp_ids = [c.id for c in self.competitions.values() if c.track == track]
            teams = [t for t in teams if t.competition_id in comp_ids]
        
        return teams[:100]


# ==================== 便捷函数 ====================

def create_competition_manager() -> CompetitionManager:
    """创建比赛管理器"""
    return CompetitionManager()


if __name__ == "__main__":
    print("=" * 60)
    print("🏆 Competition System - Demo")
    print("=" * 60)
    
    manager = CompetitionManager()
    
    print("\n📊 系统统计:")
    stats = manager.get_statistics()
    print(f"   总比赛数: {stats['total_competitions']}")
    print(f"   进行中: {stats['active_competitions']}")
    print(f"   参赛团队: {stats['total_teams']}")
    
    print("\n📋 开放比赛:")
    open_comps = manager.list_competitions(status="open")
    for comp in open_comps:
        print(f"   • {comp.name} ({comp.track})")
        print(f"     {comp.start_date} ~ {comp.end_date}")
    
    print("\n📝 参赛示例:")
    team = manager.enter(
        competition_id="paper_sprint_2026_01",
        team_name="苏柏亚战队",
        members=["研究员A", "研究员B"]
    )
    print(f"   团队: {team.name}")
    print(f"   成员: {team.members}")
    
    print("\n💯 评分示例:")
    result = manager.evaluate(
        competition_id="paper_sprint_2026_01",
        team_id=team.id,
        scores={
            "publication_quality": 85,
            "innovation": 90,
            "methodology": 88,
            "writing": 82
        },
        feedback="优秀的创新性和方法论"
    )
    print(f"   总分: {result.total_score:.1f}")
    
    print("\n🏆 排行榜:")
    rankings = manager.calculate_rankings("paper_sprint_2026_01")
    for i, t in enumerate(rankings[:3], 1):
        print(f"   {i}. {t.name} - {t.score:.1f}分")
