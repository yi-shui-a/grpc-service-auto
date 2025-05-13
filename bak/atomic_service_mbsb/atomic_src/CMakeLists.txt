# 设置 CMake 最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(atomic_service_mbsb)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 添加头文件搜索路径
include_directories(${PROJECT_SOURCE_DIR}/atomic_include)

# 指定源文件目录
file(GLOB_RECURSE SOURCES "${PROJECT_SOURCE_DIR}/*.cpp")

# 生成静态链接库，名称为项目名称
add_library(${PROJECT_NAME} STATIC ${SOURCES})

# 设置静态库的输出路径为 project_root/lib
set_target_properties(${PROJECT_NAME} PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../lib
    # 设置库的前缀为空，这样生成的库名就不会以 lib 开头
    PREFIX ""
)