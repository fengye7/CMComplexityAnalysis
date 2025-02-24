import os

# 项目根目录
BASE_PATH = os.path.dirname(__file__)
# 系统拓扑文件路径
SYSTEM_RELATIONS_PATH = os.path.join(BASE_PATH, "data/systems/system_relations.json")
# 服务拓扑文件路径
SERVICE_RELATIONS_PATH = os.path.join(BASE_PATH, "data/services/service_relations.json")
# 其他文件路径目录
SYSTEM_SERVICE_DIR = os.path.join(BASE_PATH, "data/systems_services/")
SERVICE_INTERFACE_DIR = os.path.join(BASE_PATH, "data/services_interfaces/")

INTERFACE_UPSTREAM_DIR = os.path.join(BASE_PATH, "data/interfaces/upstream/")
INTERFACE_DOWNSTREAM_DIR = os.path.join(BASE_PATH, "data/interfaces/downstream/")

# print(BASE_PATH)
# print(SYSTEM_RELATIONS_PATH)
# print(SERVICE_RELATIONS_PATH)
# print(SYSTEM_SERVICE_DIR)
# print(SERVICE_INTERFACE_DIR)
# print(INTERFACE_UPSTREAM_DIR)
# print(INTERFACE_DOWNSTREAM_DIR)
