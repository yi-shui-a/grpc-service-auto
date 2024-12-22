from src.utils.Util import Util

# Util.compile_idl("IDLs/example.idl")
# Util.compile_dds("server_src/dds_publisher_formal_demo.cpp")
Util.compileClientDemo(
    service_list=["atomic_service_mbsb", "atomic_service_sf"],
    topic_list=["example"],
    filename="client_formal_demo_with_dds.cpp",
)
Util.compileServerDemo(
    service_list=["atomic_service_mbsb", "atomic_service_sf"],
    filename="serverA_sync_server",
)
