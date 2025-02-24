# model/network/impact_analysis.py
from typing import Dict, List, Set
from model.network.graph import EnhancedSystemGraph
from model.definitions.nodes import Interface, Service, System


def enhanced_impact_analysis(
    graph: EnhancedSystemGraph, target_id: str, layer: str, max_depth: int = 3
) -> Dict[str, List[str]]:
    """统一的影响分析入口"""
    return graph.analyze_impact(target_id, layer, max_depth)
