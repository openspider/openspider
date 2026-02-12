"""
Critical Rationalism Engine
批判理性主义引擎

基于卡尔·波普尔和戴维·多伊奇的批判理性主义理论

核心方法论：
- 猜想 (Conjecture)
- 批评 (Criticism)  
- 反驳 (Refutation)
- 错误消除 (Error Elimination)
- 新猜想 (New Conjecture)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ConjectureType(Enum):
    """猜想类型"""
    HYPOTHESIS = "hypothesis"           # 科学假设
    THEORY = "theory"                   # 理论
    PREDICTION = "prediction"           # 预测
    EXPLANATION = "explanation"        # 解释
    SOLUTION = "solution"              # 解决方案


class CriticismType(Enum):
    """批评类型"""
    EMPIRICAL = "empirical"             # 经验性批评
    LOGICAL = "logical"                 # 逻辑性批评
    PRACTICAL = "practical"             # 实践性批评
    ETHICAL = "ethical"                 # 伦理批评
    PEER = "peer"                      # 同侪批评


@dataclass
class Conjecture:
    """猜想"""
    id: str
    content: str
    conjecture_type: ConjectureType
    domain: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    evidence: List[Dict] = field(default_factory=list)
    proposer: str = "anonymous"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.conjecture_type.value,
            "domain": self.domain,
            "timestamp": self.timestamp,
            "evidence": self.evidence,
            "proposer": self.proposer
        }


@dataclass
class Criticism:
    """批评"""
    id: str
    conjecture_id: str
    criticism_type: CriticismType
    content: str
    severity: float  # 0-1, 1表示最严重
    critic: str = "anonymous"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    refutation_attempt: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "conjecture_id": self.conjecture_id,
            "type": self.criticism_type.value,
            "content": self.content,
            "severity": self.severity,
            "critic": self.critic,
            "timestamp": self.timestamp,
            "refutation_attempt": self.refutation_attempt
        }


@dataclass
class Refutation:
    """反驳"""
    id: str
    conjecture_id: str
    criticism_id: str
    result: str  # "refuted", "survived", "modified"
    evidence: Dict
    explanation: str
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "conjecture_id": self.conjecture_id,
            "criticism_id": self.criticism_id,
            "result": self.result,
            "evidence": self.evidence,
            "explanation": self.explanation
        }


class CriticalRationalismEngine:
    """
    批判理性主义引擎
    
    实现知识创造的猜想-批评-反驳循环
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.conjectures: Dict[str, Conjecture] = {}
        self.criticisms: Dict[str, Criticism] = {}
        self.refutations: Dict[str, Refutation] = {}
        self._id_counter = 0
    
    # ==================== Conjecture Phase ====================
    
    def create_conjecture(
        self,
        content: str,
        conjecture_type: ConjectureType,
        domain: str,
        proposer: str = "system",
        evidence: List[Dict] = None
    ) -> Conjecture:
        """
        创建猜想
        
        猜想 = 对问题的尝试性回答
        """
        self._id_counter += 1
        conjecture_id = f"conj_{self._id_counter}"
        
        conjecture = Conjecture(
            id=conjecture_id,
            content=content,
            conjecture_type=conjecture_type,
            domain=domain,
            proposer=proposer,
            evidence=evidence or []
        )
        
        self.conjectures[conjecture_id] = conjecture
        
        return conjecture
    
    def get_conjecture(self, conjecture_id: str) -> Optional[Conjecture]:
        """获取猜想"""
        return self.conjectures.get(conjecture_id)
    
    def list_conjectures(self, domain: str = None) -> List[Conjecture]:
        """列出猜想"""
        conjectures = list(self.conjectures.values())
        if domain:
            conjectures = [c for c in conjectures if c.domain == domain]
        return conjectures
    
    # ==================== Criticism Phase ====================
    
    def add_criticism(
        self,
        conjecture_id: str,
        criticism_type: CriticismType,
        content: str,
        severity: float,
        critic: str = "system"
    ) -> Criticism:
        """
        添加批评
        
        批评 = 寻找猜想的错误
        """
        if conjecture_id not in self.conjectures:
            raise ValueError(f"Conjecture {conjecture_id} not found")
        
        self._id_counter += 1
        criticism_id = f"crit_{self._id_counter}"
        
        criticism = Criticism(
            id=criticism_id,
            conjecture_id=conjecture_id,
            criticism_type=criticism_type,
            content=content,
            severity=severity,
            critic=critic
        )
        
        self.criticisms[criticism_id] = criticism
        
        return criticism
    
    def generate_systematic_criticism(
        self,
        conjecture_id: str,
        critic: str = "system"
    ) -> List[Criticism]:
        """
        生成系统性批评
        
        从多个维度对猜想进行批评
        """
        conjecture = self.conjectures.get(conjecture_id)
        if not conjecture:
            return []
        
        criticisms = []
        
        # 1. 逻辑一致性批评
        criticisms.append(self.add_criticism(
            conjecture_id=conjecture_id,
            criticism_type=CriticismType.LOGICAL,
            content="检查逻辑一致性：猜想内部是否存在矛盾？",
            severity=0.3,
            critic=critic
        ))
        
        # 2. 经验可检验性批评
        criticisms.append(self.add_criticism(
            conjecture_id=conjecture_id,
            criticism_type=CriticismType.EMPIRICAL,
            content="检查经验可检验性：猜想是否可被证伪？",
            severity=0.5,
            critic=critic
        ))
        
        # 3. 实践可行性批评
        criticisms.append(self.add_criticism(
            conjecture_id=conjecture_id,
            criticism_type=CriticismType.PRACTICAL,
            content="检查实践可行性：猜想在现实中是否可行？",
            severity=0.4,
            critic=critic
        ))
        
        # 4. 伦理合规性批评
        criticisms.append(self.add_criticism(
            conjecture_id=conjecture_id,
            criticism_type=CriticismType.ETHICAL,
            content="检查伦理合规性：猜想是否符合伦理规范？",
            severity=0.6,
            critic=critic
        ))
        
        return criticisms
    
    # ==================== Refutation Phase ====================
    
    def attempt_refutation(
        self,
        conjecture_id: str,
        criticism_id: str,
        test_result: Dict,
        explanation: str
    ) -> Refutation:
        """
        尝试反驳
        
        反驳 = 用证据测试猜想
        """
        if conjecture_id not in self.conjectures:
            raise ValueError(f"Conjecture {conjecture_id} not found")
        
        if criticism_id not in self.criticisms:
            raise ValueError(f"Criticism {criticism_id} not found")
        
        self._id_counter += 1
        refutation_id = f"ref_{self._id_counter}"
        
        # 判断反驳结果
.criticisms[        severity = selfcriticism_id].severity
        test_passed = test_result.get("passed", False)
        
        if test_passed:
            if severity > 0.7:
                result = "refuted"  # 严重错误，猜想被反驳
            else:
                result = "modified"  # 需要修正
        else:
            result = "survived"  # 猜想存活
        
        refutation = Refutation(
            id=refutation_id,
            conjecture_id=conjecture_id,
            criticism_id=criticism_id,
            result=result,
            evidence=test_result,
            explanation=explanation
        )
        
        self.refutations[refutation_id] = refutation
        
        return refutation
    
    # ==================== Error Elimination ====================
    
    def eliminate_errors(self, conjecture_id: str) -> Dict:
        """
        消除错误
        
        根据反驳结果更新猜想
        """
        conjecture = self.conjectures.get(conjecture_id)
        if not conjecture:
            return {"error": "Conjecture not found"}
        
        refutations = [r for r in self.refutations.values() if r.conjecture_id == conjecture_id]
        
        survived = [r for r in refutations if r.result == "survived"]
        refuted = [r for r in refutations if r.result == "refuted"]
        modified = [r for r in refutations if r.result == "modified"]
        
        # 如果被严重反驳，标记为无效
        if len(refuted) > len(survived):
            conjecture.status = "refuted"
        else:
            # 否则进行修正
            for r in modified:
                conjecture.content += f"\n[修正]: {r.explanation}"
            conjecture.status = "refined"
        
        return {
            "conjecture_id": conjecture_id,
            "status": conjecture.status,
            "survived_count": len(survived),
            "refuted_count": len(refuted),
            "modified_count": len(modified)
        }
    
    # ==================== New Conjecture ====================
    
    def refine_conjecture(
        self,
        original_id: str,
        new_content: str,
        evidence: List[Dict] = None
    ) -> Conjecture:
        """
        精化猜想
        
        基于批评和反驳创建新猜想
        """
        original = self.conjectures.get(original_id)
        if not original:
            raise ValueError(f"Original conjecture {original_id} not found")
        
        return self.create_conjecture(
            content=new_content,
            conjecture_type=original.conjecture_type,
            domain=original.domain,
            proposer=original.proposer,
            evidence=evidence or []
        )
    
    # ==================== Cycle Visualization ====================
    
    def get_cycle_status(self) -> Dict:
        """获取循环状态"""
        return {
            "status": "active",
            "conjectures": len(self.conjectures),
            "criticisms": len(self.criticisms),
            "refutations": len(self.refutations),
            "cycle": {
                "phase": "Conjecture → Criticism → Refutation → Error Elimination → New Conjecture",
                "progress": f"{len(self.conjectures)} → {len(self.criticisms)} → {len(self.refutations)}"
            }
        }
    
    def run_full_cycle(
        self,
        initial_conjecture: str,
        domain: str,
        test_plan: Dict
    ) -> Dict:
        """
        运行完整循环
        
        端到端的猜想-批评-反驳流程
        """
        # 1. 创建猜想
        conjecture = self.create_conjecture(
            content=initial_conjecture,
            conjecture_type=ConjectureType.HYPOTHESIS,
            domain=domain
        )
        
        # 2. 系统性批评
        criticisms = self.generate_systematic_criticism(conjecture.id)
        
        # 3. 尝试反驳
        refutations = []
        for criticism in criticisms:
            # 模拟测试
            test_result = {"passed": True}  # 简化：假设测试通过
            refutation = self.attempt_refutation(
                conjecture_id=conjecture.id,
                criticism_id=criticism.id,
                test_result=test_result,
                explanation="测试通过"
            )
            refutations.append(refutation)
        
        # 4. 错误消除
        elimination = self.eliminate_errors(conjecture.id)
        
        # 5. 如果需要，创建新猜想
        new_conjecture = None
        if elimination["status"] == "refined":
            new_conjecture = self.refine_conjecture(
                original_id=conjecture.id,
                new_content=initial_conjecture + " (refined)",
                evidence=[{"elimination": elimination}]
            )
        
        return {
            "original_conjecture": conjecture.to_dict(),
            "criticisms": [c.to_dict() for c in criticisms],
            "refutations": [r.to_dict() for r in refutations],
            "elimination": elimination,
            "new_conjecture": new_conjecture.to_dict() if new_conjecture else None,
            "cycle_completed": True
        }
