from pyvis.network import Network


def generate_topology_view(graph, layer="service", output_file="topo.html"):
    """生成交互式拓扑图（修复版）"""
    vis = Network(height="800px", width="100%", directed=True, notebook=False)

    # 层级配置
    layer_config = {
        "system": {
            "graph": graph.system_graph,
            "group_key": "type",
            "node_color": "#FFB6C1",
            "edge_label": "depends",
        },
        "service": {
            "graph": graph.service_graph,
            "group_key": "system",
            "node_color": "#87CEFA",
            "edge_label": "dependency",
        },
        "interface": {
            "graph": graph.interface_graph,
            "group_key": "service",
            "node_color": "#98FB98",
            "edge_label": "call",
        },
    }

    config = layer_config[layer]
    source_graph = config["graph"]

    # 添加节点（带样式增强）
    for node in source_graph.nodes(data=True):
        node_id = node[0]
        metadata = node[1]

        vis.add_node(
            node_id,
            label=metadata.get("name", node_id),
            group=metadata.get(config["group_key"], "default"),
            title=format_tooltip(metadata),  # 增强的提示信息
            color=config["node_color"],
            shape="box" if layer == "system" else "ellipse",
            size=30 if layer == "system" else 20,
        )

    # 添加边（带样式增强）
    for edge in source_graph.edges(data=True):
        edge_data = edge[2]
        vis.add_edge(
            edge[0],
            edge[1],
            label=edge_data.get(config["edge_label"], ""),
            title=f"Type: {edge_data.get('relation_type','')}\nProtocol: {edge_data.get('protocol','')}",
            arrows="to",
            color="#808080",
            width=2 if edge_data.get("critical") else 1,
            dashes=True if edge_data.get("deprecated") else False,  # 废弃接口虚线
        )

    # 优化布局配置
    vis.set_options(
        """
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 100,
          "damping": 0.4
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      },
      "nodes": {
        "font": {
          "size": 16,
          "face": "Tahoma"
        }
      }
    }
    """
    )
    vis.show(output_file)


def format_tooltip(metadata):
    """生成富文本提示信息（增强容错版）"""
    tooltip = []
    node_type = metadata.get("type", "unknown")

    if node_type == "system":
        tooltip.append(f"📦 System: {metadata.get('name','unnamed')}")
        tooltip.append(f"Services: {len(metadata.get('services',[]))}")

    elif node_type == "service":
        tooltip.append(f"🔧 Service: {metadata.get('name','unnamed')}")
        tooltip.append(f"Interfaces: {len(metadata.get('interfaces',[]))}")
        tooltip.append(f"System: {metadata.get('system','unknown')}")

    elif node_type == "interface":
        tooltip.append(f"🔌 Interface: {metadata.get('name','unnamed')}")
        tooltip.append(f"Protocol: {metadata.get('method','unknown')}")

    elif node_type == "requirement":
        tooltip.append(f"📋 Requirement: {metadata.get('name','unnamed')}")

    elif node_type == "story":
        tooltip.append(f"📖 Story: {metadata.get('name','unnamed')}")

    else:
        tooltip.append("⚠️ Unknown Node Type")

    return "\n".join(tooltip)


def visualize_impact(enhanced_graph, impact, output_file="impact.html"):
    """可视化影响传播路径（修复版）"""
    nt = Network(height="800px", width="100%", directed=True)

    # 样式配置
    node_styles = {
        "system": {"color": "#FFB6C1", "shape": "box", "size": 35},
        "service": {"color": "#87CEFA", "shape": "ellipse", "size": 25},
        "interface": {"color": "#98FB98", "shape": "circle", "size": 20},
    }

    # 收集所有相关节点
    all_nodes = set()

    # 系统层节点
    for sys_id in impact["systems"]:
        all_nodes.add(("system", sys_id))
        # 添加系统相关边
        for edge in enhanced_graph.system_graph.edges(sys_id, data=True):
            nt.add_edge(edge[0], edge[1], **edge[2])

    # 服务层节点
    for svc_id in impact["services"]:
        all_nodes.add(("service", svc_id))
        # 添加服务相关边
        for edge in enhanced_graph.service_graph.edges(svc_id, data=True):
            nt.add_edge(edge[0], edge[1], **edge[2])

    # 接口层节点
    for itf_id in impact["interfaces"]:
        all_nodes.add(("interface", itf_id))
        # 添加接口相关边
        for edge in enhanced_graph.interface_graph.edges(itf_id, data=True):
            nt.add_edge(edge[0], edge[1], **edge[2])

    # 添加节点
    for node_type, node_id in all_nodes:
        # 获取原始节点数据
        if node_type == "system":
            data = enhanced_graph.system_graph.nodes[node_id]
        elif node_type == "service":
            data = enhanced_graph.service_graph.nodes[node_id]
        else:
            data = enhanced_graph.interface_graph.nodes[node_id]

        nt.add_node(
            node_id,
            label=data.get("name", node_id),
            title=format_tooltip(data),
            **node_styles[node_type],
        )

    # 优化布局
    nt.set_options(
        """
    {
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 150,
          "nodeDistance": 200
        },
        "solver": "hierarchicalRepulsion",
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01
        }
      },
    }
    """
    )
    nt.show(output_file)


def add_legend(nt):
    """添加图例节点"""
    legend_nodes = [
        ("System", "system", "#FFB6C1", "box"),
        ("Service", "service", "#87CEFA", "ellipse"),
        ("Interface", "interface", "#98FB98", "circle"),
    ]

    for text, node_type, color, shape in legend_nodes:
        nt.add_node(
            f"legend_{node_type}",
            label=text,
            color=color,
            shape=shape,
            size=20,
            physics=False,
            x=100,
            y=100 + 50 * len(legend_nodes),
        )


def filter_view(nt, keyword):
    """根据关键词过滤节点"""
    for node in nt.nodes:
        if keyword.lower() not in node["label"].lower():
            node["hidden"] = True


def add_performance_heatmap(nt, metrics):
    """添加性能热力图"""
    max_qps = max(metrics.values())
    for node in nt.nodes:
        if node["id"] in metrics:
            # 根据QPS值计算颜色深浅
            intensity = metrics[node["id"]] / max_qps
            node["color"] = f"rgba(255,0,0,{intensity})"
