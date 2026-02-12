"""
Demo: Multi-Agent Collaboration
演示：多智能体协作
"""

from athenian_digital_academy import AthenianDigitalAcademy


def demo_collaboration():
    """演示多智能体协作"""
    print("=" * 60)
    print("Athenian Digital Academy - Multi-Agent Collaboration Demo")
    print("=" * 60)
    
    # 创建系统
    academy = AthenianDigitalAcademy()
    academy.initialize()
    
    # 定义任务
    task = {
        "type": "strategic_analysis",
        "content": "分析AI技术在网络安全领域的应用前景",
        "priority": "high"
    }
    
    # 启动协作
    print("\n1. 启动多智能体协作...")
    result = academy.start_collaboration(
        task=task,
        roles=["strategist", "researcher", "engineer"]
    )
    
    print(f"   任务类型: {result['task']['type']}")
    print(f"   参与智能体: {result['synthesis']['participants']}")
    print(f"   输出数量: {result['synthesis']['output_count']}")
    
    # 返回结果
    return result


def demo_knowledge_capsule():
    """演示知识胶囊"""
    print("\n" + "=" * 60)
    print("Knowledge Capsule Demo")
    print("=" * 60)
    
    academy = AthenianDigitalAcademy()
    
    # 创建胶囊
    print("\n2. 创建知识胶囊...")
    capsule = academy.create_knowledge_capsule(
        content="基于Transformer的多模态表示学习在大规模文化数据上展现出显著效果，通过层次化约束实现跨域知识迁移。",
        domain="ai",
        tags=["transformer", "multimodal", "cultural_heritage"],
        cross_domain={
            "domains": ["ai", "cultural_studies"],
            "method": "hierarchical_constraints",
            "insight": "Transformer架构可扩展至文化遗产领域"
        }
    )
    
    print(f"   胶囊ID: {capsule['id']}")
    print(f"   核心洞察: {capsule['core_insight']['summary']}")
    print(f"   跨域融合: {capsule.get('cross_domain_fusion', {})}")
    
    return capsule


def demo_critical_rationalism():
    """演示批判理性主义"""
    print("\n" + "=" * 60)
    print("Critical Rationalism Demo")
    print("=" * 60)
    
    academy = AthenianDigitalAcademy()
    
    # 运行批判循环
    print("\n3. 运行批判理性主义循环...")
    conjecture = "AI模型可以通过自我反思不断提升性能，无需外部干预。"
    
    result = academy.run_critical_cycle(
        conjecture=conjecture,
        domain="ai"
    )
    
    print(f"   原始猜想: {result['original_conjecture']['content'][:50]}...")
    print(f"   批评数量: {len(result['criticisms'])}")
    print(f"   反驳数量: {len(result['refutations'])}")
    print(f"   循环完成: {result['cycle_completed']}")
    
    if result['new_conjecture']:
        print(f"   新猜想: {result['new_conjecture']['content'][:50]}...")
    
    return result


def demo_arbitration():
    """演示仲裁合成"""
    print("\n" + "=" * 60)
    print("Arbitration Synthesis Demo")
    print("=" * 60)
    
    academy = AthenianDigitalAcademy()
    
    # 仲裁合成
    print("\n4. 执行仲裁合成...")
    inputs = [
        {"role": "creative", "content": "创新方案A"},
        {"role": "analytic", "content": "分析方案B"},
        {"role": "safety", "content": "安全审查结果"}
    ]
    
    result = academy.arbitrated_synthesis(inputs)
    
    print(f"   输入数量: {result['input_count']}")
    print(f"   状态: {result['status']}")
    print(f"   安全检查: {result['safety_check']}")
    
    return result


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🧠 Athenian Digital Academy - Complete Demo")
    print("=" * 60)
    
    # 1. 多智能体协作
    demo_collaboration()
    
    # 2. 知识胶囊
    demo_knowledge_capsule()
    
    # 3. 批判理性主义
    demo_critical_rationalism()
    
    # 4. 仲裁合成
    demo_arbitration()
    
    # 获取系统状态
    academy = AthenianDigitalAcademy()
    academy.initialize()
    status = academy.get_status()
    
    print("\n" + "=" * 60)
    print("📊 System Status")
    print("=" * 60)
    print(f"   状态: {status['status']}")
    print(f"   Agent层: {status['layers']['agent']['status']}")
    print(f"   Synthesis层: {status['layers']['synthesis']['layer']}")
    print(f"   包容性提升: {status['layers']['synthesis']['performance']['inclusivity_improvement']}")
    
    print("\n" + "=" * 60)
    print("✅ Demo Completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
