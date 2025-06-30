cmake_minimum_required(VERSION 3.10)
project(atomic_test_zlsc)

# 设置C++标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_PREFIX_PATH "/usr/local/share/cmake-3.22/Protobuf" ${CMAKE_PREFIX_PATH})
set(CMAKE_PREFIX_PATH "/usr/local/share/cmake-3.22/gRPC" ${CMAKE_PREFIX_PATH})
# 设置 gRPC 的 CMake 模块路径
set(gRPC_DIR "/usr/local/lib/cmake/grpc/")
# 设置 Protobuf 的 CMake 模块路径
set(Protobuf_DIR "/usr/local/lib/cmake/protobuf/")

# 查找必要的库
find_package(Threads REQUIRED)
# 查找nlohmann_json库
find_package(nlohmann_json REQUIRED)

# 查找gRPC库
find_package(Protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)

file(GLOB SOURCES_CPP "${CMAKE_SOURCE_DIR}/*.cpp")

# 添加可执行文件
add_executable( atomic_test_zlsc
    # 添加cmake目录下的所有cpp文件
    ${SOURCES_CPP}
    
    ${CMAKE_SOURCE_DIR}/../../atomic_service/atomic_test_zlsc/protos/atomic_test_zlsc.pb.cc
    ${CMAKE_SOURCE_DIR}/../../atomic_service/atomic_test_zlsc/protos/atomic_test_zlsc.grpc.pb.cc
    
)

# 包含目录
target_include_directories( atomic_test_zlsc PRIVATE
    ${CMAKE_SOURCE_DIR}/
    
    ${CMAKE_SOURCE_DIR}/../../atomic_service/atomic_test_zlsc/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../atomic_service/atomic_test_zlsc/protos

) 

# 链接库
target_link_libraries( atomic_test_zlsc PRIVATE
    
    ${CMAKE_SOURCE_DIR}/../../atomic_service/atomic_test_zlsc/lib/atomic_test_zlsc_sync_server_impl.so  # 动态库路径
    
    nlohmann_json::nlohmann_json
    grpc++
    grpc
    protobuf::libprotobuf
    protobuf::libprotoc
    Threads::Threads
)

# 设置可执行文件的输出路径
# 强制导出所有符号
set_target_properties(atomic_test_zlsc PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin
    # 设置可执行文件的前缀为空，这样生成的可执行文件名就不会以 lib 开头
    PREFIX ""
)