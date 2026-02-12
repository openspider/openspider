"""
Knowledge Capsule System
知识胶囊系统

基于Kai的知识胶囊哲学：
- Encapsulate (封装): 可复用的知识单元
- Traceability (溯源): 追踪每个想法的来源
- Semantic Collision (语义碰撞): 跨域思想的相遇
- Cross-domain Fusion (跨域融合): AI+科学+哲学+历史
- Historical Reproduction (历史复现): 用现代眼光发现旧知识
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib


@dataclass
class CoreInsight:
    """核心洞察"""
    summary: str
    details: str
    confidence: float  # 0-1
    sources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "summary": self.summary,
            "details": self.details,
            "confidence": self.confidence,
            "sources": self.sources
        }


@dataclass
class CapsuleContext:
    """胶囊上下文"""
    domain: str
    discipline: str
    tags: List[str] = field(default_factory=list)
    related_capsules: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "domain": self.domain,
            "discipline": self.discipline,
            "tags": self.tags,
            "related_capsules": self.related_capsules
        }


@dataclass
class CapsuleOrigin:
    """胶囊溯源"""
    discovered_by: str
    discovery_date: str
    discovery_method: str
    original_source: str
    verification_status: str = "pending"
    
    def to_dict(self) -> Dict:
        return {
            "discovered_by": self.discovered_by,
            "discovery_date": self.discovery_date,
            "discovery_method": self.discovery_method,
            "original_source": self.original_source,
            "verification_status": self.verification_status
        }


@dataclass
class CapsuleEvolution:
    """胶囊演进"""
    version: str
    modified_date: str
    modifications: List[str] = field(default_factory=list)
    improvement_notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "modified_date": self.modified_date,
            "modifications": self.modifications,
            "improvement_notes": self.improvement_notes
        }


@dataclass
class CrossDomainFusion:
    """跨域融合"""
    domains_involved: List[str]
    fusion_method: str
    emergent_insight: str
    novelty_score: float  # 0-1
    fusion_evidence: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "domains_involved": self.domains_involved,
            "fusion_method": self.fusion_method,
            "emergent_insight": self.emergent_insight,
            "novelty_score": self.novelty_score,
            "fusion_evidence": self.fusion_evidence
        }


@dataclass
class KnowledgeCapsule:
    """
    知识胶囊
    
    结构：
    - core_insight: 核心洞察
    - context: 上下文
    - origin: 溯源
    - evolution: 演进
    - cross_domain_fusion: 跨域融合
    """
    id: str
    core_insight: CoreInsight
    context: CapsuleContext
    origin: CapsuleOrigin
    evolution: CapsuleEvolution
    cross_domain_fusion: Optional[CrossDomainFusion] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """生成胶囊ID"""
        content = f"{self.core_insight.summary}{self.context.domain}{datetime.now().isoformat()}"
        return f"KC-{datetime.now().strftime('%Y-%m-%d')}-{hashlib.md5(content.encode()).hexdigest()[:8]}"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "core_insight": self.core_insight.to_dict(),
            "context": self.context.to_dict(),
            "origin": self.origin.to_dict(),
            "evolution": self.evolution.to_dict(),
            "cross_domain_fusion": self.cross_domain_fusion.to_dict() if self.cross_domain_fusion else None
        }
    
    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        md = f"""# {self.id}

## 💎 Core Insight
**{self.core_insight.summary}**
- Details: {self.core_insight.details}
- Confidence: {self.core_insight.confidence:.2f}
- Sources: {', '.join(self.core_insight.sources)}

## 📊 Context
- Domain: {self.context.domain}
- Discipline: {self.context.discipline}
- Tags: {', '.join(self.context.tags)}
- Related Capsules: {', '.join(self.context.related_capsules)}

## 🔗 Origin
- Discovered by: {self.origin.discovered_by}
- Date: {self.origin.discovery_date}
- Method: {self.origin.discovery_method}
- Source: {self.origin.original_source}
- Verification: {self.origin.verification_status}

## 🔄 Evolution
- Version: {self.evolution.version}
- Modified: {self.evolution.modified_date}
- Modifications: {', '.join(self.evolution.modifications)}
- Improvements: {', '.join(self.evolution.improvement_notes)}

"""
        if self.cross_domain_fusion:
            md += f"""## 🌐 Cross-Domain Fusion
- Domains: {', '.join(self.cross_domain_fusion.domains_involved)}
- Method: {self.cross_domain_fusion.fusion_method}
- Emergent Insight: {self.cross_domain_fusion.emergent_insight}
- Novelty Score: {self.cross_domain_fusion.novelty_score:.2f}

"""
        return md


class KnowledgeCapsuleSystem:
    """
    知识胶囊系统
    
    实现知识封装、溯源、语义碰撞和跨域融合
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.capsules: Dict[str, KnowledgeCapsule] = {}
        self.semantic_index: Dict[str, List[str]] = {}  # 语义索引
        self.collision_pairs: List[Dict] = []  # 碰撞记录
        self._id_counter = 0
    
    # ==================== Capsule Management ====================
    
    def create_capsule(
        self,
        insight_summary: str,
        insight_details: str,
        confidence: float,
        domain: str,
        discipline: str,
        discovered_by: str,
        discovery_method: str,
        original_source: str,
        tags: List[str] = None,
        cross_domain_fusion: Dict = None
    ) -> KnowledgeCapsule:
        """
        创建知识胶囊
        
        封装：创建可复用的知识单元
        """
        self._id_counter += 1
        
        # 核心洞察
        core_insight = CoreInsight(
            summary=insight_summary,
            details=insight_details,
            confidence=confidence,
            sources=[original_source]
        )
        
        # 上下文
        context = CapsuleContext(
            domain=domain,
            discipline=discipline,
            tags=tags or []
        )
        
        # 溯源
        origin = CapsuleOrigin(
            discovered_by=discovered_by,
            discovery_date=datetime.now().isoformat(),
            discovery_method=discovery_method,
            original_source=original_source
        )
        
        # 演进
        evolution = CapsuleEvolution(
            version="1.0",
            modified_date=datetime.now().isoformat(),
            modifications=["Initial creation"],
            improvement_notes=[]
        )
        
        # 跨域融合
        fusion = None
        if cross_domain_fusion:
            fusion = CrossDomainFusion(
                domains_involved=cross_domain_fusion.get("domains", []),
                fusion_method=cross_domain_fusion.get("method", ""),
                emergent_insight=cross_domain_fusion.get("insight", ""),
                novelty_score=cross_domain_fusion.get("novelty", 0.5)
            )
        
        # 创建胶囊
        capsule = KnowledgeCapsule(
            id=f"KC-{datetime.now().strftime('%Y-%m-%d')}-{self._id_counter:04d}",
            core_insight=core_insight,
            context=context,
            origin=origin,
            evolution=evolution,
            cross_domain_fusion=fusion
        )
        
        # 存储
        self.capsules[capsule.id] = capsule
        
        # 更新语义索引
        self._update_semantic_index(capsule)
        
        return capsule
    
    def get_capsule(self, capsule_id: str) -> Optional[KnowledgeCapsule]:
        """获取胶囊"""
        return self.capsules.get(capsule_id)
    
    def list_capsules(self, domain: str = None) -> List[KnowledgeCapsule]:
        """列出胶囊"""
        capsules = list(self.capsules.values())
        if domain:
            capsules = [c for c in capsules if c.context.domain == domain]
        return capsules
    
    def update_capsule(
        self,
        capsule_id: str,
        new_insight: str = None,
        improvement_notes: List[str] = None
    ) -> KnowledgeCapsule:
        """
        更新胶囊
        
        演进：记录胶囊的演化历史
        """
        capsule = self.capsules.get(capsule_id)
        if not capsule:
            raise ValueError(f"Capsule {capsule_id} not found")
        
        # 更新演进
        capsule.evolution.version = f"{float(capsule.evolution.version) + 0.1:.1f}"
        capsule.evolution.modified_date = datetime.now().isoformat()
        
        if new_insight:
            capsule.core_insight.details = new_insight
        
        if improvement_notes:
            capsule.evolution.improvement_notes.extend(improvement_notes)
        
        return capsule
    
    # ==================== Traceability ====================
    
    def trace_origin(self, capsule_id: str) -> Dict:
        """
        溯源
        
        追踪胶囊的发现历史
        """
        capsule = self.capsules.get(capsule_id)
        if not capsule:
            return {"error": "Capsule not found"}
        
        return {
            "capsule_id": capsule_id,
            "origin": capsule.origin.to_dict(),
            "evolution": capsule.evolution.to_dict(),
            "lineage": f"Created by {capsule.origin.discovered_by} on {capsule.origin.discovery_date}"
        }
    
    def verify_source(self, capsule_id: str, verification_result: str) -> Dict:
        """验证来源"""
        capsule = self.capsules.get(capsule_id)
        if not capsule:
            return {"error": "Capsule not found"}
        
        capsule.origin.verification_status = verification_result
        
        return {
            "capsule_id": capsule_id,
            "verification": verification_result
        }
    
    # ==================== Semantic Collision ====================
    
    def semantic_collision(
        self,
        capsule1_id: str,
        capsule2_id: str
    ) -> Dict:
        """
        语义碰撞
        
        发现两个胶囊之间的关联和冲突
        """
        capsule1 = self.capsules.get(capsule1_id)
        capsule2 = self.capsules.get(capsule2_id)
        
        if not capsule1 or not capsule2:
            return {"error": "One or both capsules not found"}
        
        # 分析碰撞
        domains = [capsule1.context.domain, capsule2.context.domain]
        domain_overlap = len(set(domains)) < len(domains)
        
        collision_analysis = {
            "capsule1": capsule1_id,
            "capsule2": capsule2_id,
            "domains": domains,
            "domain_overlap": domain_overlap,
            "collision_type": self._analyze_collision_type(capsule1, capsule2),
            "insights": self._extract_collision_insights(capsule1, capsule2),
            "collision_strength": self._calculate_collision_strength(capsule1, capsule2)
        }
        
        # 记录碰撞
        self.collision_pairs.append({
            "pair": [capsule1_id, capsule2_id],
            "analysis": collision_analysis,
            "timestamp": datetime.now().isoformat()
        })
        
        return collision_analysis
    
    def _analyze_collision_type(
        self,
        c1: KnowledgeCapsule,
        c2: KnowledgeCapsule
    ) -> str:
        """分析碰撞类型"""
        if c1.context.domain == c2.context.domain:
            return "intra_domain"  # 同域增强
        else:
            return "cross_domain"  # 跨域融合
    
    def _extract_collision_insights(
        self,
        c1: KnowledgeCapsule,
        c2: KnowledgeCapsule
    ) -> List[str]:
        """提取碰撞洞察"""
        insights = []
        
        # 洞察1：概念关联
        if c1.core_insight.summary != c2.core_insight.summary:
            insights.append(f"Both capsules address {c1.context.domain} and {c2.context.domain}")
        
        # 洞察2：方法论融合
        insights.append(f"Methodology from {c1.context.discipline} can inform {c2.context.discipline}")
        
        return insights
    
    def _calculate_collision_strength(
        self,
        c1: KnowledgeCapsule,
        c2: KnowledgeCapsule
    ) -> float:
        """计算碰撞强度"""
        # 基于置信度和跨域程度
        base_strength = (c1.core_insight.confidence + c2.core_insight.confidence) / 2
        
        # 如果跨域，增加强度
        if c1.context.domain != c2.context.domain:
            base_strength *= 1.2
        
        return min(base_strength, 1.0)
    
    # ==================== Cross-Domain Fusion ====================
    
    def create_fusion(
        self,
        capsule_ids: List[str],
        fusion_method: str
    ) -> KnowledgeCapsule:
        """
        创建跨域融合胶囊
        
        基于多个胶囊创建新的融合洞察
        """
        capsules = [self.capsules[id] for id in capsule_ids if id in self.capsules]
        
        if len(capsules) < 2:
            raise ValueError("Need at least 2 capsules to create fusion")
        
        # 提取共同洞察
        common_insights = []
        for c in capsules:
            common_insights.append(c.core_insight.summary)
        
        # 创建新胶囊
        fusion_capsule = self.create_capsule(
            insight_summary=f"Fusion of {len(capsules)} domains",
            insight_details="; ".join(common_insights),
            confidence=sum(c.core_insight.confidence for c in capsules) / len(capsules),
            domain="fusion",
            discipline="cross_domain",
            discovered_by="system",
            discovery_method="semantic_collision",
            original_source="Cross-domain fusion",
            tags=["fusion", "cross_domain"],
            cross_domain_fusion={
                "domains": list(set(c.context.domain for c in capsules)),
                "method": fusion_method,
                "insight": f"Merged insights from {', '.join(c.context.domain for c in capsules)}",
                "novelty": 0.8
            }
        )
        
        return fusion_capsule
    
    # ==================== Historical Reproduction ====================
    
    def reproduce_historical_knowledge(
        self,
        historical_text: str,
        modern_analysis: str,
        domain: str
    ) -> KnowledgeCapsule:
        """
        历史复现
        
        重新发现历史知识并用现代视角分析
        """
        return self.create_capsule(
            insight_summary=f"Historical insight from {domain}",
            insight_details=f"Historical: {historical_text}\n\nModern Analysis: {modern_analysis}",
            confidence=0.7,
            domain=domain,
            discipline="historical_studies",
            discovered_by="system",
            discovery_method="historical_reproduction",
            original_source=historical_text[:100] + "...",
            tags=["historical", "reproduction"]
        )
    
    # ==================== Index Management ====================
    
    def _update_semantic_index(self, capsule: KnowledgeCapsule):
        """更新语义索引"""
        keywords = [
            capsule.context.domain,
            capsule.context.discipline
        ] + capsule.context.tags
        
        for keyword in keywords:
            if keyword not in self.semantic_index:
                self.semantic_index[keyword] = []
            if capsule.id not in self.semantic_index[keyword]:
                self.semantic_index[keyword].append(capsule.id)
    
    def search_by_keyword(self, keyword: str) -> List[KnowledgeCapsule]:
        """关键词搜索"""
        capsule_ids = self.semantic_index.get(keyword, [])
        return [self.capsules[id] for id in capsule_ids if id in self.capsules]
    
    def search_by_domain(self, domain: str) -> List[KnowledgeCapsule]:
        """领域搜索"""
        return self.list_capsules(domain)
    
    # ==================== Export ====================
    
    def export_to_json(self) -> Dict:
        """导出为JSON"""
        return {
            "total_capsules": len(self.capsules),
            "collision_events": len(self.collision_pairs),
            "capsules": {k: v.to_dict() for k, v in self.capsules.items()}
        }
    
    def export_to_markdown(self, output_path: str):
        """导出为Markdown"""
        content = "# Knowledge Capsule Collection\n\n"
        content += f"Total: {len(self.capsules)} capsules\n\n"
        
        for capsule in self.capsules.values():
            content += capsule.to_markdown()
            content += "\n---\n\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "total_capsules": len(self.capsules),
            "collision_events": len(self.collision_pairs),
            "indexed_keywords": len(self.semantic_index),
            "domains": list(set(c.context.domain for c in self.capsules.values()))
        }
