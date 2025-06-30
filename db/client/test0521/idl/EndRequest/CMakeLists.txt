cmake_minimum_required(VERSION 3.10)
project(EndRequest)

# 设置 CycloneDDS 的路径
set(CYCLONEDDS_HOME "/usr/local/lib/cmake/CycloneDDS/")

# 查找 idlc 编译器
find_program(IDLC_EXECUTABLE idlc PATHS "${CYCLONEDDS_HOME}/bin" REQUIRED)

# 设置 IDL 文件路径
set(IDL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/EndRequest.idl")

# 设置生成的 C 和 H 文件路径
set(GENERATED_C_FILE "${CMAKE_CURRENT_SOURCE_DIR}/EndRequest.c")
set(GENERATED_H_FILE "${CMAKE_CURRENT_SOURCE_DIR}/EndRequest.h")

# 添加自定义命令来生成 C 和 H 文件
add_custom_command(
    OUTPUT ${GENERATED_C_FILE} ${GENERATED_H_FILE}
    COMMAND ${IDLC_EXECUTABLE} -o ${CMAKE_CURRENT_SOURCE_DIR} ${IDL_FILE}
    DEPENDS ${IDL_FILE}
    COMMENT "Generating C and H files from EndRequest IDL"
)

# 添加一个自定义目标，用于生成文件
add_custom_target(generate_idl_files ALL DEPENDS ${GENERATED_C_FILE} ${GENERATED_H_FILE})