# 设置 CMake 最低版本要求
cmake_minimum_required(VERSION 3.10)

# 设置项目名称
project(FusionDataDemo)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置 CycloneDDS 的路径
set(CYCLONEDDS_HOME "/usr/local/lib/cmake/CycloneDDS/")

# 查找必要的库
find_package(Threads REQUIRED)
# 查找nlohmann_json库
find_package(nlohmann_json REQUIRED)
# 查找 CycloneDDS 库
find_package(CycloneDDS REQUIRED)

# 添加头文件搜索路径
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RobotPose/idl
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RobotPose/atomic_include
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RadarData/idl
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RadarData/atomic_include
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/MotorData/idl
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/MotorData/atomic_include
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/ImageDetection/idl
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/ImageDetection/atomic_include
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/FusionData/idl
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/FusionData/atomic_include
    ${CycloneDDS_INCLUDE_DIRS}
)

# 定义主源文件列表，不包含公共的 .c 文件
set(MAIN_SOURCE_FILES
    ImageDetectionNode_1.cpp
    MotorDataNode_1.cpp
    RadarDataNode_1.cpp
    RobotPoseNode_1.cpp
    StartPublisher_1.cpp
    FusionData_1.cpp
)

# 定义公共的 .c 文件列表
set(COMMON_SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RobotPose/idl/RobotPose.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RadarData/idl/RadarData.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/MotorData/idl/MotorData.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/ImageDetection/idl/ImageDetection.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/FusionData/idl/FusionData.c
)

# 定义静态库列表
set(STATIC_LIBS
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RobotPose/lib/RobotPose.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/RadarData/lib/RadarData.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/MotorData/lib/MotorData.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/ImageDetection/lib/ImageDetection.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../../atomic_service/FusionData/lib/FusionData.a
)

# 遍历主源文件列表，为每个文件创建可执行文件
foreach(MAIN_SOURCE ${MAIN_SOURCE_FILES})
    # 获取文件名（不包含扩展名）
    get_filename_component(EXECUTABLE_NAME ${MAIN_SOURCE} NAME_WE)
    
    # 添加可执行文件，同时包含公共的 .c 文件
    add_executable(${EXECUTABLE_NAME} ${MAIN_SOURCE} ${COMMON_SOURCE_FILES})
    
    # 链接 DDS 库和静态库
    target_link_libraries(${EXECUTABLE_NAME} CycloneDDS::ddsc ${STATIC_LIBS} Threads::Threads nlohmann_json::nlohmann_json)

    # 设置可执行文件的输出目录
    set_target_properties(${EXECUTABLE_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
    )
endforeach()