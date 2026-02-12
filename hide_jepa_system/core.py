"""
Hide-JEPA Knowledge Capsule System - Core Implementation
基于 Hide-JEPA 论文思想的知识胶囊系统核心实现

核心创新：
1. 分层感知约束 (Hierarchical-Aware Constraints)
2. 多模态交叉注意力融合 (Multimodal Cross-Attention Fusion)
3. 2D Bucketized Relative Position Encoding
4. 自监督预训练与EMA目标编码器
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import hashlib
import json
from datetime import datetime
import numpy as np


class ModalityType(Enum):
    TEXT = "text"
    VISUAL = "visual"
    STRUCTURE = "structure"
    CODE = "code"
    AUDIO = "audio"


@dataclass
class KnowledgeCapsule:
    """知识胶囊数据结构"""
    capsule_id: str
    origin: Dict[str, Any]
    content: Dict[str, Any]
    semantic_position: Dict[str, str]
    collision_history: List[Dict] = field(default_factory=list)
    cross_domain_links: List[Dict] = field(default_factory=list)
    embedding: Optional[np.ndarray] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "capsule_id": self.capsule_id,
            "origin": self.origin,
            "content": self.content,
            "semantic_position": self.semantic_position,
            "collision_history": self.collision_history,
            "cross_domain_links": self.cross_domain_links,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeCapsule':
        return cls(
            capsule_id=data["capsule_id"],
            origin=data["origin"],
            content=data["content"],
            semantic_position=data["semantic_position"],
            collision_history=data.get("collision_history", []),
            cross_domain_links=data.get("cross_domain_links", []),
            metadata=data.get("metadata", {})
        )


class HierarchicalTaxonomy:
    """分层语义分类体系"""
    
    LEVEL_1_DOMAINS = {
        "AI": ["LLM", "Computer_Vision", "NLP", "Reinforcement_Learning", "Agent"],
        "Science": ["Physics", "Biology", "Chemistry", "Mathematics", "Cognitive_Science"],
        "Philosophy": ["Epistemology", "Metaphysics", "Ethics", "Logic", "Aesthetics"],
        "History": ["Ancient", "Medieval", "Modern", "Contemporary", "Civilization"],
        "Engineering": ["Software", "Hardware", "Systems", "Security", "Performance"]
    }
    
    def __init__(self, num_levels: int = 3):
        self.num_levels = num_levels
    
    def classify(self, content: str, domain_hint: Optional[str] = None) -> Dict[str, str]:
        """基于内容自动分类到分层结构"""
        # 简化的分类逻辑 - 实际应使用NLP模型
        result = {
            "level_1": domain_hint or "AI",
            "level_2": "General",
            "level_3": "Unknown"
        }
        
        # 关键词匹配
        content_lower = content.lower()
        keywords_l2 = {
            "transformer": "Transformers",
            "bert": "NLP",
            "gpt": "LLM",
            "vit": "Computer_Vision",
            "agent": "Agent",
            "reinforcement": "Reinforcement_Learning",
            "je": "Self-Supervised",
            "capsule": "Representation_Learning"
        }
        
        for keyword, category in keywords_l2.items():
            if keyword in content_lower:
                result["level_2"] = category
                break
        
        # 生成唯一level_3
        result["level_3"] = self._generate_level3(content)
        
        return result
    
    def _generate_level3(self, content: str) -> str:
        """生成微观级别的分类标识"""
        hash_val = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"item_{hash_val}"


class OverlappingPatchEmbedding(nn.Module):
    """
    Overlapping Patch Embedding 层
    替换标准线性投影，保持局部连续性
    """
    
    def __init__(self, in_channels: int = 3, embed_dim: int = 768, 
                 patch_size: int = 16, overlap: int = 4):
        super().__init__()
        self.patch_size = patch_size
        self.overlap = overlap
        self stride = patch_size - overlap
        
        # 使用卷积进行overlapping patch embedding
        self.proj = nn.Conv2d(
            in_channels, 
            embed_dim, 
            kernel_size=patch_size,
            stride=self.stride,
            padding=0  # 无padding以保持尺寸一致性
        )
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, Tuple[int, int]]:
        """
        Args:
            x: 输入图像 [B, C, H, W]
        Returns:
            tokens: 嵌入token [B, N, D]
            spatial_shape: 空间形状 (H', W')
        """
        B, C, H, W = x.shape
        spatial_shape = (H - self.patch_size) // self.stride + 1, \
                       (W - self.patch_size) // self.stride + 1
        
        x = self.proj(x)  # [B, D, H', W']
        x = x.flatten(2).transpose(1, 2)  # [B, N, D]
        
        return x, spatial_shape


class BucketizedRelativePositionBias(nn.Module):
    """
    2D Bucketized Relative Position Encoding
    
    解决可变尺度场景中的绝对位置嵌入限制
    确保模型捕捉平移不变的空关系
    """
    
    def __init__(self, num_heads: int = 12, bucket_size: int = 4, 
                 max_distance: int = 128):
        super().__init__()
        self.num_heads = num_heads
        self.bucket_size = bucket_size
        self.max_distance = max_distance
        
        # 计算可能的bucket数量
        self.num_buckets = (2 * max_distance // bucket_size + 1)
        
        # 可学习的相对位置偏置
        self.bias = nn.Parameter(
            torch.zeros(num_heads, self.num_buckets)
        )
        nn.init.trunc_normal_(self.bias, std=0.02)
    
    def get_bucket_id(self, delta_x: torch.Tensor, delta_y: torch.Tensor) -> torch.Tensor:
        """
        将相对坐标映射到bucket ID
        
        Args:
            delta_x, delta_y: 相对坐标 [B, N, N]
        Returns:
            bucket_ids: bucket索引 [B, N, N]
        """
        # 量化到bucket
        delta = torch.stack([delta_x, delta_y], dim=-1)
        abs_delta = torch.abs(delta)
        
        # 桶化处理
        scaled = abs_delta / self.max_distance * (self.num_buckets // 2)
        bucket_ids = torch.clamp(scaled.long(), 0, self.num_buckets - 1)
        
        # 处理符号
        sign = torch.sign(delta).long()
        bucket_ids = bucket_ids * sign + self.num_buckets // 2
        
        return bucket_ids.sum(-1)  # 简化处理
    
    def forward(self, batch_size: int, seq_len: int, 
                relative_coords: Tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
        """
        Args:
            batch_size: 批次大小
            seq_len: 序列长度
            relative_coords: (delta_x, delta_y) 相对坐标
        Returns:
            bias: 位置偏置 [B, N, N]
        """
        delta_x, delta_y = relative_coords
        
        # 获取bucket ID
        bucket_ids = self.get_bucket_id(delta_x, delta_y)
        
        # 索引到偏置
        bias = self.bias[:, bucket_ids]  # [num_heads, B, N, N]
        
        return bias.transpose(0, 1)  # [B, num_heads, N, N]


class CrossAttentionFusion(nn.Module):
    """
    多模态交叉注意力融合模块
    
    整合视觉token与结构化先验知识
    """
    
    def __init__(self, embed_dim: int = 768, num_heads: int = 8,
                 structural_dim: int = 256, dropout: float = 0.1):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        
        # 视觉投影
        self.visual_q = nn.Linear(embed_dim, embed_dim)
        self.visual_k = nn.Linear(embed_dim, embed_dim)
        self.visual_v = nn.Linear(embed_dim, embed_dim)
        
        # 结构化先验投影
        self.structural_k = nn.Linear(structural_dim, embed_dim)
        self.structural_v = nn.Linear(structural_dim, embed_dim)
        
        # 输出投影
        self.output_proj = nn.Linear(embed_dim, embed_dim)
        
        # 层归一化和Dropout
        self.layer_norm1 = nn.LayerNorm(embed_dim)
        self.layer_norm2 = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(dropout)
        
        # FFN
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(embed_dim * 4, embed_dim),
            nn.Dropout(dropout)
        )
    
    def forward(self, visual_tokens: torch.Tensor, 
                structural_tokens: torch.Tensor) -> torch.Tensor:
        """
        Args:
            visual_tokens: 视觉特征 [B, N, D]
            structural_tokens: 结构化先验 [B, M, S]
        Returns:
            fused: 融合后的特征 [B, N, D]
        """
        B, N, D = visual_tokens.shape
        _, M, S = structural_tokens.shape
        
        # 第一步：交叉注意力
        Q = self.visual_q(visual_tokens)
        K = self.structural_k(structural_tokens)
        V = self.structural_v(structural_tokens)
        
        # 多头注意力
        Q = Q.view(B, N, self.num_heads, D // self.num_heads).transpose(1, 2)
        K = K.view(B, M, self.num_heads, D // self.num_heads).transpose(1, 2)
        V = V.view(B, M, self.num_heads, D // self.num_heads).transpose(1, 2)
        
        attn_weights = (Q @ K.transpose(-2, -1)) / (D ** 0.5)
        attn_weights = F.softmax(attn_weights, dim=-1)
        attn_output = attn_weights @ V
        
        attn_output = attn_output.transpose(1, 2).contiguous().view(B, N, D)
        attn_output = self.dropout(self.output_proj(attn_output))
        
        # 残差连接和层归一化
        visual_tokens = self.layer_norm1(visual_tokens + attn_output)
        
        # 第二步：FFN处理
        visual_tokens = self.layer_norm2(visual_tokens + self.ffn(visual_tokens))
        
        return visual_tokens


class HierarchicalRegularization(nn.Module):
    """
    分层正则化模块
    
    确保学习到的表示捕捉分类学关系
    """
    
    def __init__(self, embed_dim: int = 768, num_levels: int = 3,
                 hierarchy_weights: List[float] = None):
        super().__init__()
        
        self.embed_dim = embed_dim
        self.num_levels = num_levels
        
        # 各层级的投影头
        self.level_projectors = nn.ModuleList([
            nn.Linear(embed_dim, embed_dim // 2) for _ in range(num_levels)
        ])
        
        # 层级间的约束矩阵 (软约束)
        if hierarchy_weights is None:
            hierarchy_weights = [1.0, 0.5, 0.25]  # 越高层级权重越大
        self.hierarchy_weights = hierarchy_weights
        
        # 温度参数
        self.temperature = nn.Parameter(torch.ones(1) * 0.1)
    
    def forward(self, representations: torch.Tensor, 
                hierarchy_labels: List[torch.Tensor]) -> Tuple[torch.Tensor, Dict]:
        """
        Args:
            representations: 输入表示 [B, N, D]
            hierarchy_labels: 各层级的标签列表
        Returns:
            loss: 分层正则化损失
            info: 详细信息字典
        """
        total_loss = 0.0
        info = {}
        
        for level, (projector, weight, labels) in enumerate(
                zip(self.level_projectors, self.hierarchy_weights, hierarchy_labels)):
            
            # 投影到层级空间
            projected = projector(representations)  # [B, N, D']
            
            # 层级间的语义相似性约束
            # 使用温度缩放的对比损失
            sim_matrix = projected @ projected.transpose(-2, -1) / self.temperature
            
            # 正样本：同一层级且标签相同的pair
            positive_mask = (labels.unsqueeze(-1) == labels.unsqueeze(-2))
            
            # 层级约束：同父类别的子类别应该有更高的相似性
            # 简化处理：这里使用层级距离加权
            level_weight = weight
            
            level_loss = F.cross_entropy(
                sim_matrix.view(-1, sim_matrix.size(-1)),
                positive_mask.long().view(-1)
            ) * level_weight
            
            total_loss += level_loss
            info[f"level_{level}_loss"] = level_loss.item()
        
        return total_loss, info


class TargetEncoder(nn.Module):
    """
    目标编码器
    
    使用EMA更新机制提供稳定的潜在目标
    """
    
    def __init__(self, encoder: nn.Module, momentum: float = 0.996):
        super().__init__()
        
        self.encoder = encoder
        self.momentum = momentum
        
        # 复制参数作为目标
        self.target_encoder = nn.Module()
        self.target_encoder.load_state_dict(encoder.state_dict())
        
        # 冻结目标编码器
        for param in self.target_encoder.parameters():
            param.requires_grad = False
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """前向传播(使用目标编码器)"""
        with torch.no_grad():
            return self.target_encoder(x)
    
    @torch.no_grad()
    def update_momentum(self):
        """使用EMA更新目标编码器"""
        for encoder_param, target_param in zip(
                self.encoder.parameters(), 
                self.target_encoder.parameters()):
            
            target_param.data = (
                self.momentum * target_param.data + 
                (1 - self.momentum) * encoder_param.data
            )


class ContextEncoder(nn.Module):
    """
    上下文编码器
    
    整合所有增强模块的编码器
    """
    
    def __init__(self, 
                 in_channels: int = 3,
                 embed_dim: int = 768,
                 patch_size: int = 16,
                 overlap: int = 4,
                 num_heads: int = 12,
                 num_layers: int = 12,
                 structural_dim: int = 256,
                 num_levels: int = 3,
                 dropout: float = 0.1):
        super().__init__()
        
        # Patch Embedding
        self.patch_embed = OverlappingPatchEmbedding(
            in_channels, embed_dim, patch_size, overlap
        )
        
        # 位置编码
        self.pos_embed = nn.Parameter(torch.zeros(1, 196, embed_dim))
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        
        # 2D Bucketized Relative Position Encoding
        self.rel_pos_bias = BucketizedRelativePositionBias(
            num_heads=num_heads,
            bucket_size=4,
            max_distance=128
        )
        
        # 多模态交叉注意力融合
        self.caf = CrossAttentionFusion(
            embed_dim=embed_dim,
            num_heads=num_heads,
            structural_dim=structural_dim,
            dropout=dropout
        )
        
        # Transformer层
        self.transformer_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=embed_dim,
                nhead=num_heads,
                dim_feedforward=embed_dim * 4,
                dropout=dropout,
                batch_first=True
            ) for _ in range(num_layers)
        ])
        
        # 分层正则化
        self.hierarchical_reg = HierarchicalRegularization(
            embed_dim=embed_dim,
            num_levels=num_levels
        )
        
        # 输出归一化
        self.output_norm = nn.LayerNorm(embed_dim)
    
    def forward(self, x: torch.Tensor, 
                structural_tokens: Optional[torch.Tensor] = None,
                hierarchy_labels: Optional[List[torch.Tensor]] = None) -> Tuple[torch.Tensor, Dict]:
        """
        Args:
            x: 输入图像 [B, C, H, W]
            structural_tokens: 结构化先验 [B, M, S]
            hierarchy_labels: 各层级的分类标签
        Returns:
            output: 编码后的表示
            info: 包含损失信息的字典
        """
        B, C, H, W = x.shape
        
        # Patch embedding
        tokens, spatial_shape = self.patch_embed(x)
        
        # 添加位置编码
        tokens = tokens + self.pos_embed[:, :tokens.size(1)]
        
        # 结构化先验融合 (如果提供)
        if structural_tokens is not None:
            tokens = self.caf(tokens, structural_tokens)
        
        # Transformer编码
        for i, layer in enumerate(self.transformer_layers):
            # 相对位置编码
            if i == 0:  # 只在第一层使用相对位置偏置
                # 简化：使用绝对位置
                tokens = layer(tokens)
            else:
                tokens = layer(tokens)
        
        # 输出归一化
        tokens = self.output_norm(tokens)
        
        # 分层正则化损失
        hier_loss_info = {}
        if hierarchy_labels is not None:
            hier_loss, hier_loss_info = self.hierarchical_reg(tokens, hierarchy_labels)
        else:
            hier_loss = torch.tensor(0.0, device=x.device)
        
        info = {
            "hierarchical_loss": hier_loss,
            "hierarchical_loss_details": hier_loss_info,
            "spatial_shape": spatial_shape,
            "num_tokens": tokens.size(1)
        }
        
        return tokens, info


class Predictor(nn.Module):
    """
    预测器
    
    给定上下文表示和目标位置，预测目标的潜在表示
    """
    
    def __init__(self, embed_dim: int = 768, 
                 predict_depth: int = 4,
                 num_heads: int = 8,
                 dropout: float = 0.1):
        super().__init__()
        
        self.predictor = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=embed_dim,
                nhead=num_heads,
                dim_feedforward=embed_dim * 4,
                dropout=dropout,
                batch_first=True
            ) for _ in range(predict_depth)
        ])
        
        # 预测头
        self.predict_head = nn.Linear(embed_dim, embed_dim)
    
    def forward(self, context_tokens: torch.Tensor, 
                target_positions: torch.Tensor,
                target_features: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Args:
            context_tokens: 上下文token [B, N_c, D]
            target_positions: 目标位置索引 [B, N_t]
            target_features: 目标特征（用于计算损失）[B, N_t, D]
        Returns:
            predictions: 预测的潜在表示 [B, N_t, D]
            loss: 预测损失（如果提供了target_features）
        """
        # 提取目标位置的上下文
        target_context = context_tokens[torch.arange(context_tokens.size(0)).unsqueeze(-1), 
                                       target_positions]
        
        # 通过预测器
        for layer in self.predictor:
            target_context = layer(target_context)
        
        # 预测头
        predictions = self.predict_head(target_context)
        
        # 计算损失
        loss = None
        if target_features is not None:
            loss = F.mse_loss(predictions, target_features)
        
        return predictions, loss


class HideJEPAKnowledgeSystem(nn.Module):
    """
    Hide-JEPA 知识胶囊系统主类
    
    整合所有模块，实现自监督学习的知识表示和胶囊生成
    """
    
    def __init__(self,
                 in_channels: int = 3,
                 embed_dim: int = 768,
                 patch_size: int = 16,
                 num_heads: int = 12,
                 num_layers: int = 12,
                 structural_dim: int = 256,
                 num_levels: int = 3,
                 momentum: float = 0.996,
                 dropout: float = 0.1):
        super().__init__()
        
        # 组件
        self.context_encoder = ContextEncoder(
            in_channels, embed_dim, patch_size, num_heads,
            num_layers, structural_dim, num_levels, dropout
        )
        
        self.target_encoder = TargetEncoder(
            nn.Sequential(
                OverlappingPatchEmbedding(in_channels, embed_dim, patch_size),
                nn.TransformerEncoder(
                    nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads),
                    num_layers=num_layers
                )
            ),
            momentum=momentum
        )
        
        self.predictor = Predictor(embed_dim, predict_depth=4, num_heads=num_heads)
        
        # 分层分类器
        self.taxonomy = HierarchicalTaxonomy(num_levels)
        
        # 胶囊存储
        self.capsules: Dict[str, KnowledgeCapsule] = {}
    
    def forward(self, x: torch.Tensor,
                structural_tokens: Optional[torch.Tensor] = None,
                hierarchy_labels: Optional[List[torch.Tensor]] = None,
                mask: Optional[torch.Tensor] = None) -> Dict[str, Any]:
        """
        主前向传播
        
        Args:
            x: 输入 [B, C, H, W]
            structural_tokens: 结构化先验 [B, M, S]
            hierarchy_labels: 分层标签列表
            mask: 掩码 [B, N] (1=保留, 0=掩码)
        Returns:
            output: 包含预测、损失等信息的字典
        """
        B, C, H, W = x.shape
        N = (H // 16) * (W // 16)  # 假设patch_size=16
        
        # 采样上下文和目标块
        if mask is None:
            # 默认：保留25%作为上下文，掩码75%
            mask = torch.rand(B, N) < 0.25
            mask = mask.to(x.device)
        
        context_mask = ~mask
        target_mask = mask
        
        # 获取目标token
        target_features = self.target_encoder(x)
        
        # 上下文编码
        context_tokens, info = self.context_encoder(
            x, structural_tokens, hierarchy_labels
        )
        
        # 获取掩码位置的上下文
        target_positions = torch.nonzero(target_mask).split(1, dim=1)
        
        # 预测
        predictions, pred_loss = self.predictor(
            context_tokens, 
            [pos.squeeze(-1) for pos in target_positions],
            target_features
        )
        
        return {
            "predictions": predictions,
            "prediction_loss": pred_loss,
            "hierarchical_loss": info.get("hierarchical_loss"),
            "hierarchical_loss_details": info.get("hierarchical_loss_details"),
            "context_tokens": context_tokens,
            "target_features": target_features
        }
    
    def generate_capsule(self, 
                        content: str,
                        source: str = "unknown",
                        domain: str = "AI",
                        modalities: List[str] = None) -> KnowledgeCapsule:
        """
        从内容生成知识胶囊
        
        Args:
            content: 文本内容
            source: 来源标识
            domain: 领域标签
            modalities: 模态列表
        Returns:
            capsule: 知识胶囊
        """
        # 生成分类
        semantic_pos = self.taxonomy.classify(content, domain)
        
        # 生成唯一ID
        timestamp = datetime.now().isoformat()
        content_hash = hashlib.md5(f"{content}{timestamp}".encode()).hexdigest()
        capsule_id = f"KC-{timestamp[:10]}-{content_hash[:8]}"
        
        # 创建胶囊
        capsule = KnowledgeCapsule(
            capsule_id=capsule_id,
            origin={
                "source": source,
                "timestamp": timestamp,
                "modalities": modalities or ["text"]
            },
            content={
                "raw_content": content,
                "core_insight": self._extract_core_insight(content),
                "context": domain
            },
            semantic_position=semantic_pos,
            collision_history=[],
            cross_domain_links=[],
            metadata={
                "generation_time": timestamp,
                "domain": domain
            }
        )
        
        # 存储
        self.capsules[capsule_id] = capsule
        
        return capsule
    
    def _extract_core_insight(self, content: str) -> str:
        """提取核心洞见（简化版）"""
        # 实际应使用NLP模型
        sentences = content.split('.')
        return sentences[0] if sentences else content[:100]
    
    def semantic_collision(self, 
                         capsule1: KnowledgeCapsule,
                         capsule2: KnowledgeCapsule) -> Dict:
        """
        语义碰撞：发现两个胶囊之间的关联和冲突
        
        Returns:
            collision_result: 包含相似度、关联洞见等
        """
        # 简化：基于层级结构的相似性
        pos1 = capsule1.semantic_position
        pos2 = capsule2.semantic_position
        
        # 计算层级重叠
        overlaps = sum(1 for k in pos1 if k in pos2 and pos1[k] == pos2[k])
        similarity = overlaps / len(pos1)
        
        # 生成洞见
        insights = []
        if pos1.get("level_1") != pos2.get("level_1"):
            insights.append(f"跨领域连接: {pos1.get('level_1')} ↔ {pos2.get('level_1')}")
        
        return {
            "similarity": similarity,
            "overlap_levels": overlaps,
            "insights": insights,
            "collision_type": "semantic_bridge" if similarity > 0 else "divergent"
        }
    
    def retrieve(self, 
                query: str, 
                top_k: int = 5,
                level_filter: Optional[Dict] = None) -> List[Tuple[KnowledgeCapsule, float]]:
        """
        检索知识胶囊
        
        Args:
            query: 查询文本
            top_k: 返回top_k结果
            level_filter: 层级过滤条件
        Returns:
            results: 按相似度排序的胶囊列表
        """
        # 生成分类
        query_pos = self.taxonomy.classify(query)
        
        # 简化检索：基于层级匹配
        results = []
        for capsule in self.capsules.values():
            score = 0.0
            
            # 层级匹配得分
            for level, pos in capsule.semantic_position.items():
                if query_pos.get(level) == pos:
                    score += 1.0
            
            # 文本相似性（简化）
            if query.lower() in capsule.content.get("raw_content", "").lower():
                score += 0.5
            
            if score > 0:
                results.append((capsule, score))
        
        # 排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]


# 工厂函数
def create_hide_jepa_system(config: Optional[Dict] = None) -> HideJEPAKnowledgeSystem:
    """创建Hide-JEPA知识系统的工厂函数"""
    if config is None:
        config = {
            "embed_dim": 768,
            "num_heads": 12,
            "num_layers": 12,
            "structural_dim": 256,
            "num_levels": 3
        }
    
    return HideJEPAKnowledgeSystem(
        in_channels=config.get("in_channels", 3),
        embed_dim=config.get("embed_dim", 768),
        num_heads=config.get("num_heads", 12),
        num_layers=config.get("num_layers", 12),
        structural_dim=config.get("structural_dim", 256),
        num_levels=config.get("num_levels", 3)
    )


if __name__ == "__main__":
    # 示例使用
    system = create_hide_jepa_system()
    
    # 生成胶囊
    capsule1 = system.generate_capsule(
        content="Hide-JEPA proposes Hierarchical-Aware Constraints for cultural representation learning",
        source="ICML 2026 Paper",
        domain="AI",
        modalities=["text", "visual"]
    )
    
    capsule2 = system.generate_capsule(
        content="Self-supervised learning via JEPA captures high-level semantics",
        source="Meta AI Research",
        domain="AI",
        modalities=["text"]
    )
    
    # 语义碰撞
    collision = system.semantic_collision(capsule1, capsule2)
    print(f"Semantic Collision Result: {collision}")
    
    # 检索
    results = system.retrieve("JEPA hierarchical constraints", top_k=5)
    print(f"Retrieval Results: {len(results)} capsules found")
