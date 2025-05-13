# 设置 CMake 最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(atomic_service_sf_sync_client_impl)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置编译选项以确保符号导出
set(CMAKE_CXX_VISIBILITY_PRESET default)
set(CMAKE_VISIBILITY_INLINES_HIDDEN OFF)
set(CMAKE_SHARED_LINKER_FLAGS "-Wl,--export-dynamic")
# 添加编译选项，确保符号可见
add_compile_options(-fvisibility=default)


# 设置 gRPC 的 CMake 模块路径
set(gRPC_DIR "/usr/local/lib/cmake/grpc/")
# 设置 Protobuf 的 CMake 模块路径
set(Protobuf_DIR "/usr/local/lib/cmake/protobuf/")


# 添加头文件搜索路径
include_directories(
    ${PROJECT_SOURCE_DIR}/../atomic_include
    ${PROJECT_SOURCE_DIR}/../protos
)

# 添加 gRPC 和 Protobuf 库
find_package(Protobuf REQUIRED)
find_package(gRPC REQUIRED)

# 嵌套调用 atomic_src 目录下的 CMakeLists.txt
add_subdirectory(${PROJECT_SOURCE_DIR}/../atomic_src ${PROJECT_BINARY_DIR}/atomic_src)


# 指定源文件
set(SOURCE_FILES atomic_service_sf_sync_client_impl.cpp)

# 确保 SOURCE_FILES 变量不为空
if(NOT SOURCE_FILES)
    message(FATAL_ERROR "No source files found for atomic_service_sf_sync_client_impl.")
endif()

# 生成动态链接库
add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES})

# 显式声明 atomic_service_sf_sync_client_impl 依赖于 atomic_service_sf
# 确保了在构建 atomic_service_sf_sync_client_impl 之前，atomic_service_sf 已经构建完成
add_dependencies(${PROJECT_NAME} atomic_service_sf)

# 链接 atomic_service_sf 静态库
target_link_libraries(${PROJECT_NAME}
    -Wl,--whole-archive ${PROJECT_SOURCE_DIR}/../lib/atomic_service_sf.a -Wl,--no-whole-archive
    grpc++
    grpc
    protobuf
)

# 设置动态库的输出路径
# 强制导出所有符号
set_target_properties(${PROJECT_NAME} PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../lib
    # 设置库的前缀为空，这样生成的库名就不会以 lib 开头
    PREFIX ""
    CXX_VISIBILITY_PRESET default
    VISIBILITY_INLINES_HIDDEN OFF
)
