cmake_minimum_required(VERSION 3.10)
project(plane_attack_sync_client)

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
add_executable( plane_attack_sync_client
    # 添加cmake目录下的所有cpp文件
    ${SOURCES_CPP}
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_radar/protos/atomic_attack_radar.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_radar/protos/atomic_attack_radar.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_infrared/protos/atomic_attack_infrared.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_infrared/protos/atomic_attack_infrared.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_decode/protos/atomic_attack_decode.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_decode/protos/atomic_attack_decode.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_fusion/protos/atomic_attack_fusion.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_fusion/protos/atomic_attack_fusion.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_detect/protos/atomic_attack_detect.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_detect/protos/atomic_attack_detect.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_range/protos/atomic_attack_range.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_range/protos/atomic_attack_range.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_lock/protos/atomic_attack_lock.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_lock/protos/atomic_attack_lock.grpc.pb.cc
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_release/protos/atomic_attack_release.pb.cc
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_release/protos/atomic_attack_release.grpc.pb.cc
    
    
    ${CMAKE_SOURCE_DIR}/../idl/StartRequestRadar/StartRequestRadar.c
    
    ${CMAKE_SOURCE_DIR}/../idl/StartRequestInfrared/StartRequestInfrared.c
    
    ${CMAKE_SOURCE_DIR}/../idl/endResponseSF/endResponseSF.c
    
)

# 包含目录
target_include_directories( plane_attack_sync_client PRIVATE
    ${CMAKE_SOURCE_DIR}/
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_radar/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_radar/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_infrared/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_infrared/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_decode/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_decode/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_fusion/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_fusion/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_detect/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_detect/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_range/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_range/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_lock/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_lock/protos
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_release/sync_server_impl
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_release/protos
    
    
    ${CMAKE_SOURCE_DIR}/../idl/StartRequestRadar 
    
    ${CMAKE_SOURCE_DIR}/../idl/StartRequestInfrared 
    
    ${CMAKE_SOURCE_DIR}/../idl/endResponseSF 
    
    ${CycloneDDS_INCLUDE_DIRS} # 包含 CycloneDDS 头文件
) 

# 链接库
target_link_libraries( plane_attack_sync_client PRIVATE
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_radar/lib/atomic_attack_radar_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_infrared/lib/atomic_attack_infrared_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_decode/lib/atomic_attack_decode_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_fusion/lib/atomic_attack_fusion_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_detect/lib/atomic_attack_detect_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_range/lib/atomic_attack_range_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_lock/lib/atomic_attack_lock_sync_server_impl.so  # 动态库路径
    
    ${CMAKE_SOURCE_DIR}/../../../atomic_service/atomic_attack_release/lib/atomic_attack_release_sync_server_impl.so  # 动态库路径
    
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
set_target_properties(plane_attack_sync_client PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/../bin
    # 设置可执行文件的前缀为空，这样生成的可执行文件名就不会以 lib 开头
    PREFIX ""
)