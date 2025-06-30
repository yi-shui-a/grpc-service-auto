cmake_minimum_required(VERSION 3.10)
project(test0521_sync_client)

# 设置C++标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_PREFIX_PATH "/usr/local/share/cmake-3.22/Protobuf" ${CMAKE_PREFIX_PATH})
set(CMAKE_PREFIX_PATH "/usr/local/share/cmake-3.22/gRPC" ${CMAKE_PREFIX_PATH})
# 设置 gRPC 的 CMake 模块路径
set(gRPC_DIR "/usr/local/lib/cmake/grpc/")
# 设置 Protobuf 的 CMake 模块路径
set(Protobuf_DIR "/usr/local/lib/cmake/protobuf/")
# 设置 CycloneDDS 的路径
set(CYCLONEDDS_HOME "/usr/local/lib/cmake/CycloneDDS/")

# 查找必要的库
find_package(Threads REQUIRED)
# 查找nlohmann_json库
find_package(nlohmann_json REQUIRED)

# 查找gRPC库
find_package(Protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)
# 查找 CycloneDDS 库
find_package(CycloneDDS REQUIRED)

file(GLOB SOURCES_CPP "${CMAKE_SOURCE_DIR}/*.cpp")

# 添加可执行文件
add_executable( test0521_sync_client
    # 添加cmake目录下的所有cpp文件
    ${SOURCES_CPP}
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_ycl/protos/atomic_service_ycl.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_ycl/protos/atomic_service_ycl.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_zlsc/protos/atomic_service_zlsc.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_zlsc/protos/atomic_service_zlsc.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/RobotPose/protos/RobotPose.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/RobotPose/protos/RobotPose.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/FusionData/protos/FusionData.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/FusionData/protos/FusionData.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_mbsb/protos/atomic_service_mbsb.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_mbsb/protos/atomic_service_mbsb.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_sf/protos/atomic_service_sf.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_sf/protos/atomic_service_sf.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/ImageDetection/protos/ImageDetection.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/ImageDetection/protos/ImageDetection.grpc.pb.cc
    
    
    ${CMAKE_SOURCE_DIR}/../idl/StartRequest/StartRequest.c
    
    ${CMAKE_SOURCE_DIR}/../idl/EndRequest/EndRequest.c
    
)

# 包含目录
target_include_directories( test0521_sync_client PRIVATE
    ${CMAKE_SOURCE_DIR}/
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_ycl/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_ycl/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_zlsc/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_zlsc/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/RobotPose/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/RobotPose/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/FusionData/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/FusionData/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_mbsb/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_mbsb/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_sf/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_sf/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/ImageDetection/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/ImageDetection/protos
    
    
    ${CMAKE_SOURCE_DIR}/../idl/StartRequest 
    
    ${CMAKE_SOURCE_DIR}/../idl/EndRequest 
    
    ${CycloneDDS_INCLUDE_DIRS} # 包含 CycloneDDS 头文件
) 

# 链接库
target_link_libraries( test0521_sync_client PRIVATE
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_ycl/lib/atomic_service_ycl_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_zlsc/lib/atomic_service_zlsc_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/RobotPose/lib/RobotPose_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/FusionData/lib/FusionData_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_mbsb/lib/atomic_service_mbsb_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_service_sf/lib/atomic_service_sf_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/ImageDetection/lib/ImageDetection_sync_server_impl.so  # 动态库路径
    
    nlohmann_json::nlohmann_json
    grpc++
    grpc
    protobuf::libprotobuf
    protobuf::libprotoc
    CycloneDDS::ddsc
    Threads::Threads
)

# 设置可执行文件的输出路径
# 强制导出所有符号
set_target_properties(test0521_sync_client PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../bin
    # 设置可执行文件的前缀为空，这样生成的可执行文件名就不会以 lib 开头
    PREFIX ""
)