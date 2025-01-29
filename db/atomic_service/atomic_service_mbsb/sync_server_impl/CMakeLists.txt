# 设置 CMake 最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(atomic_service_mbsb_sync_server)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 嵌套调用 atomic_src 目录下的 CMakeLists.txt
add_subdirectory(../atomic_src ${CMAKE_CURRENT_BINARY_DIR}/atomic_src)

# 添加头文件搜索路径
include_directories(
    ${PROJECT_SOURCE_DIR}/../atomic_include
    ${PROJECT_SOURCE_DIR}/../protos
)

# 指定源文件
set(SOURCE_FILES atomic_service_mbsb_sync_server_impl.cpp)

# 确保 SOURCE_FILES 变量不为空
if(NOT SOURCE_FILES)
    message(FATAL_ERROR "No source files found for atomic_service_mbsb_sync_server_impl.")
endif()

# 生成动态链接库
add_library(atomic_service_mbsb_sync_server_impl SHARED ${SOURCE_FILES})

# 设置动态库的输出路径
set_target_properties(atomic_service_mbsb_sync_server_impl PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../bin
    # 设置库的前缀为空，这样生成的库名就不会以 lib 开头
    PREFIX ""
)

# 链接 atomic_service_mbsb 静态库
target_link_libraries(atomic_service_mbsb_sync_server_impl
    atomic_service_mbsb
    grpc++
    grpc
    protobuf
)
