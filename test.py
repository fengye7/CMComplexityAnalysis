# test.py
from model.definitions.nodes import (
    Interface,
    Requirement,
    Service,
    Story,
    System,
    Task,
    TestReport,
)
from model.network.graph import TopologyGraph
from model.network.impact_analysis import enhanced_impact_analysis
from model.network.view import generate_topology_view, visualize_impact


def main():
    # 构建测试数据
    order_system = System("sys001", "订单系统", "订单处理核心系统")
    payment_service = Service("svc001", "支付服务", "支付流程管理", order_system)
    pay_api = Interface("itf001", "支付接口", "完成支付接口的实现", payment_service)

    # 构建需求链
    test_report = TestReport("report001", "测试报告", "支付超时测试报告")
    task = Task("task001", "超时配置调整", "调整支付超时参数", test_report)
    story = Story(
        "story001", "支付超时优化", "优化支付超时机制", order_system, [pay_api]
    )
    story.tasks.append(task)

    req = Requirement("req001", "支付优化需求", "提升支付成功率")
    req.stories.append(story)

    # 初始化网络
    graph = TopologyGraph()
    graph.add_system(order_system)
    graph.add_service(payment_service)
    graph.add_interface(pay_api)
    graph.link_requirement(req)

    # 执行影响分析
    impact = enhanced_impact_analysis(graph, "itf001", "interface")
    print(f"受影响的系统: {impact['systems']}")
    print(f"关联的需求: {impact['requirements']}")

    # 生成可视化
    generate_topology_view(graph, layer="service", output_file="service_topo.html")
    visualize_impact(graph, impact, output_file="impact.html")


if __name__ == "__main__":
    main()

# # 可视化结果
# graph.visualize_impact(impact, "payment_impact.html")


# class TestDataBuilder:
#     @staticmethod
#     def create_sample_graph():
#         # 初始化图结构
#         enhanced_graph = EnhancedSystemGraph()

#         # 构建系统
#         order_system = System("sys001", "订单系统", "订单处理核心系统")
#         enhanced_graph.add_system(order_system)

#         # 构建服务
#         payment_service = Service("svc001", "支付服务", "处理支付流程", order_system)
#         inventory_service = Service("svc002", "库存服务", "管理商品库存", order_system)
#         enhanced_graph.add_service(payment_service)
#         enhanced_graph.add_service(inventory_service)

#         # 构建接口
#         pay_api = Interface("itf001", "支付接口", "执行支付操作", payment_service)
#         stock_api = Interface(
#             "itf002", "库存查询接口", "检查商品库存", inventory_service
#         )
#         pay_api.downstream.append(stock_api)
#         enhanced_graph.add_interface(pay_api)
#         enhanced_graph.add_interface(stock_api)

#         # 建立服务依赖
#         payment_service.dependencies.append(inventory_service)
#         enhanced_graph.update_service_dependencies()

#         return enhanced_graph


# # 生成拓扑可视化
# enhanced_graph = TestDataBuilder.create_sample_graph()
# generate_topology_view(enhanced_graph, layer="service", output_file="service_topo.html")
# generate_topology_view(
#     enhanced_graph, layer="interface", output_file="interface_topo.html"
# )

# # 模拟变更影响
# impact = {
#     "systems": {"sys001"},
#     "services": {"svc001", "svc002"},
#     "interfaces": {"itf001", "itf002"},
# }

# # 生成影响可视化
# visualize_impact(enhanced_graph, impact, output_file="impact_view.html")


# # 测试数据构建
# def test_case():
#     graph = EnhancedSystemGraph()

#     # 构建系统
#     order_system = System("sys001", "订单系统", "订单处理核心系统")
#     graph.add_system(order_system)

#     # 构建服务
#     payment_service = Service("svc001", "支付服务", "处理支付流程", order_system)
#     graph.add_service(payment_service)

#     # 构建需求
#     req = Requirement("req001", "支付优化", "提升支付成功率")
#     story = Story("story001", "超时优化", "优化支付超时机制", order_system, [])
#     req.stories.append(story)
#     graph.link_requirement(req)

#     # 生成视图
#     generate_topology_view(graph, layer="system", output_file="test_topo.html")


# # 执行测试
# test_case()
