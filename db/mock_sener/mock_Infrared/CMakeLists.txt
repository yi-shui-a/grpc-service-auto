cmake_minimum_required(VERSION 3.10)
project(mock_Infrared)

# 设置 C 标准
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)

# 设置 CycloneDDS 的路径
set(CYCLONEDDS_HOME "/usr/local/lib/cmake/CycloneDDS/")

# 查找 CycloneDDS 库
find_package(CycloneDDS REQUIRED)

# 设置包含路径
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/StartRequestInfrared
    ${CycloneDDS_INCLUDE_DIRS} # 包含 CycloneDDS 头文件
)

# 设置源文件
set(SOURCES
    mock_Infrared.cpp  # 你的 Publisher Demo 源文件
    ${CMAKE_CURRENT_SOURCE_DIR}/StartRequestInfrared.c
)

# 添加可执行文件
add_executable(mock_Infrared ${SOURCES})

# 链接 CycloneDDS 库
target_link_libraries(mock_Infrared PRIVATE CycloneDDS::ddsc)

# 设置可执行文件的输出目录
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
)