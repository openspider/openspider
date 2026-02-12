#!/usr/bin/env python3
"""
Hide-JEPA Knowledge System - Daily Report Generator Application
知识胶囊系统应用于日报生成场景
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/hide_jepa_system')

from core import (
    HideJEPAKnowledgeSystem,
    KnowledgeCapsule,
    create_hide_jepa_system
)
from datetime import datetime
import json


class DailyReportGenerator:
    """
    日报生成器应用
    
    利用 Hide-JEPA 系统自动生成和更新日报
    """
    
    def __init__(self):
        self.system = create_hide_jepa_system()
        self.daily_reports = {}
    
    def ingest_paper(self, paper_info: Dict) -> KnowledgeCapsule:
        """
        摄入论文信息
        
        Args:
            paper_info: {
                "title": str,
                "authors": List[str],
                "venue": str,
                "abstract": str,
                "content": str,
                "domain": str
            }
        """
        # 构建内容描述
        content = f"""
        Paper: {paper_info['title']}
        Authors: {', '.join(paper_info['authors'])}
        Venue: {paper_info['venue']}
        Abstract: {paper_info['abstract']}
        """
        
        capsule = self.system.generate_capsule(
            content=content + "\n" + paper_info.get('content', ''),
            source=paper_info['venue'],
            domain=paper_info.get('domain', 'AI'),
            modalities=['text', 'visual' if paper_info.get('has_figures') else 'text']
        )
        
        # 添加论文特定的元数据
        capsule.origin['authors'] = paper_info['authors']
        capsule.origin['venue'] = paper_info['venue']
        capsule.metadata['paper_info'] = paper_info
        
        return capsule
    
    def ingest_industry_news(self, news_info: Dict) -> KnowledgeCapsule:
        """
        摄入产业新闻
        """
        content = f"""
        Title: {news_info['title']}
        Company: {news_info.get('company', 'Unknown')}
        Category: {news_info.get('category', 'General')}
        Summary: {news_info['summary']}
        """
        
        capsule = self.system.generate_capsule(
            content=content,
            source=news_info.get('source', 'Industry News'),
            domain=news_info.get('domain', 'Industry'),
            modalities=['text']
        )
        
        capsule.metadata['funding'] = news_info.get('funding')
        capsule.metadata['category'] = news_info.get('category')
        
        return capsule
    
    def generate_daily_summary(self, date: str) -> Dict:
        """
        生成日报摘要
        """
        # 检索所有相关胶囊
        results = self.system.retrieve(
            query=f"AI research {date}",
            top_k=50,
            level_filter={"level_1": "AI"}
        )
        
        # 分类整理
        summary = {
            "date": date,
            "generated_at": datetime.now().isoformat(),
            "sections": {
                "research_frontier": [],
                "industry_moves": [],
                "policy_updates": [],
                "key_insights": []
            },
            "knowledge_capsules_used": []
        }
        
        for capsule, score in results:
            capsule_data = capsule.to_dict()
            summary["knowledge_capsules_used"].append({
                "id": capsule.capsule_id,
                "score": score,
                "domain": capsule.semantic_position.get("level_2")
            })
            
            # 分类到各板块
            domain = capsule.semantic_position.get("level_1", "Other")
            
            if domain == "AI":
                summary["sections"]["research_frontier"].append({
                    "insight": capsule.content.get("core_insight", ""),
                    "source": capsule.origin.get("source", ""),
                    "score": score
                })
            elif domain == "Industry":
                summary["sections"]["industry_moves"].append({
                    "content": capsule.content.get("core_insight", ""),
                    "score": score
                })
            elif domain == "Policy":
                summary["sections"]["policy_updates"].append({
                    "update": capsule.content.get("core_insight", ""),
                    "score": score
                })
        
        # 生成关键洞见
        summary["sections"]["key_insights"] = self._generate_key_insights(results)
        
        # 存储日报
        self.daily_reports[date] = summary
        
        return summary
    
    def _generate_key_insights(self, results: List) -> List[Dict]:
        """生成关键洞见列表"""
        insights = []
        
        # 分析跨域碰撞
        domains_seen = set()
        for capsule, score in results[:20]:
            pos = capsule.semantic_position
            domain = pos.get("level_1")
            domains_seen.add(domain)
            
            # 检测跨域融合
            if len(domains_seen) > 1:
                collision = self.system.semantic_collision(
                    capsule, 
                    results[0][0]  # 与第一个胶囊比较
                )
                
                if collision["similarity"] < 0.5:  # 不同领域
                    insights.append({
                        "type": "cross_domain_bridge",
                        "description": f"连接 {pos.get('level_1')} 与其他领域",
                        "strength": collision["similarity"]
                    })
        
        return insights
    
    def suggest_research_directions(self) -> List[Dict]:
        """
        基于知识库建议研究方向
        """
        # 检索最新前沿
        results = self.system.retrieve(
            query="self-supervised representation learning",
            top_k=20
        )
        
        suggestions = []
        for capsule, score in results:
            # 分析缺失的方向
            content = capsule.content.get("raw_content", "")
            
            if "hierarchical" not in content.lower() and score > 0.3:
                suggestions.append({
                    "direction": "分层表示学习",
                    "reason": f"基于 {capsule.origin.get('source', '未知来源')} 的研究发现",
                    "priority": score
                })
        
        return sorted(suggestions, key=lambda x: x["priority"], reverse=True)


# 演示代码
def demo():
    """演示系统使用"""
    
    print("=" * 60)
    print("Hide-JEPA Knowledge System - Demo")
    print("=" * 60)
    
    # 初始化系统
    generator = DailyReportGenerator()
    
    # 1. 摄入论文示例（基于你下载的Hide-JEPA论文）
    print("\n[1] Ingesting Hide-JEPA Paper...")
    paper_info = {
        "title": "Hide-JEPA: Hierarchical-Aware Joint Embedding Predictive Architecture for Structured Cultural Representation Learning",
        "authors": ["Anonymous Submission"],
        "venue": "ICML 2026",
        "abstract": """Joint Embedding Predictive Architecture (JEPA) has emerged as a powerful paradigm for self-supervised learning, yet its efficacy remains under-explored in domains characterized by complex hierarchical semantics and implicit spatial relationships, such as architectural heritage.""",
        "domain": "AI",
        "content": """
        Core innovations:
        1. Hierarchical-Aware Constraints: Regularize latent space based on multi-level semantic taxonomy
        2. Multimodal Cross-Attention Fusion: Integrate visual tokens with structural geometry
        3. 2D Bucketized Relative Position Encodings: Enhanced spatial reasoning
        
        Dataset: YAIG-mini (11,804 images, 3-level hierarchical annotations)
        Results: ~80% accuracy on 35-way classification
        """,
        "has_figures": True
    }
    
    capsule = generator.ingest_paper(paper_info)
    print(f"  Created capsule: {capsule.capsule_id}")
    print(f"  Semantic position: {capsule.semantic_position}")
    
    # 2. 摄入产业新闻
    print("\n[2] Ingesting Industry News...")
    news_info = {
        "title": "OpenAI Announces GPT-5 Preview",
        "company": "OpenAI",
        "category": "Product Launch",
        "source": "Tech News",
        "summary": "GPT-5 expected Q1 2026 with enhanced agent capabilities",
        "domain": "Industry",
        "funding": None
    }
    
    news_capsule = generator.ingest_industry_news(news_info)
    print(f"  Created capsule: {news_capsule.capsule_id}")
    
    # 3. 生成日报
    print("\n[3] Generating Daily Summary...")
    today = datetime.now().strftime("%Y-%m-%d")
    summary = generator.generate_daily_summary(today)
    
    print(f"\nDaily Report Summary ({today}):")
    print(f"  Capsules used: {len(summary['knowledge_capsules_used'])}")
    print(f"  Research items: {len(summary['sections']['research_frontier'])}")
    print(f"  Industry items: {len(summary['sections']['industry_moves'])}")
    print(f"  Key insights: {len(summary['sections']['key_insights'])}")
    
    # 4. 语义碰撞演示
    print("\n[4] Demonstrating Semantic Collision...")
    collision = generator.system.semantic_collision(capsule, news_capsule)
    print(f"  Collision type: {collision['collision_type']}")
    print(f"  Similarity: {collision['similarity']:.3f}")
    print(f"  Insights: {collision['insights']}")
    
    # 5. 检索演示
    print("\n[5] Demonstrating Retrieval...")
    results = generator.system.retrieve(
        query="JEPA hierarchical representation learning",
        top_k=5
    )
    print(f"  Found {len(results)} relevant capsules")
    for capsule, score in results:
        print(f"    - {capsule.capsule_id}: score={score:.3f}")
    
    # 6. 研究方向建议
    print("\n[6] Research Direction Suggestions...")
    suggestions = generator.suggest_research_directions()
    for suggestion in suggestions[:3]:
        print(f"  [{suggestion['priority']:.2f}] {suggestion['direction']}")
        print(f"       Reason: {suggestion['reason']}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)
    
    return generator, summary


if __name__ == "__main__":
    generator, summary = demo()
    
    # 保存示例胶囊信息
    print("\n" + "=" * 60)
    print("Sample Capsule Data:")
    print("=" * 60)
    
    # 获取系统中的所有胶囊
    for capsule_id, capsule in generator.system.capsules.items():
        print(f"\nCapsule: {capsule_id}")
        print(json.dumps(capsule.to_dict(), indent=2, ensure_ascii=False))
        break  # 只打印一个示例
