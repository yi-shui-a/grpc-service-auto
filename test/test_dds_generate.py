import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

# from src.scripts.util.AtomServiceUtil import AtomServiceUtil
# from src.scripts.util.GrpcMethodUtil import GrpcMethodUtil
# from src.scripts.util.ServerUtil import ServerUtil
# from scripts.entity.Server import Server
# from src.scripts.util.Util import Util
# from src.scripts.util.DDSUtil import DDSUtil

from src.scripts.util import *
from src.scripts.entity import *

if __name__ == "__main__":

    # """
    # atomic_service相关的函数
    # """
    # # 解析h文件，生成service对象
    # service_image_detection = AtomServiceUtil.parseHpp(
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/ImageDetection.h"
    # )
    # service_motor_data = AtomServiceUtil.parseHpp(
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/MotorData.h"
    # )
    # service_radar_data = AtomServiceUtil.parseHpp(
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/RadarData.h"
    # )
    # service_robot_pose = AtomServiceUtil.parseHpp(
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/RobotPose.h"
    # )
    # service_fusion_data = AtomServiceUtil.parseHpp(
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/FusionData.h"
    # )

    # # 解析 cpp 文件
    # AtomServiceUtil.parseCpp(
    #     service_image_detection,
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/ImageDetection.cpp",
    # )
    # AtomServiceUtil.parseCpp(
    #     service_motor_data,
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/MotorData.cpp",
    # )
    # AtomServiceUtil.parseCpp(
    #     service_radar_data,
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/RadarData.cpp",
    # )
    # AtomServiceUtil.parseCpp(
    #     service_robot_pose,
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/RobotPose.cpp",
    # )
    # AtomServiceUtil.parseCpp(
    #     service_fusion_data,
    #     f"{os.path.dirname(os.path.abspath(__file__))}/../example/dds_example/FusionData.cpp",
    # )

    # # 生成微服务编译的cmake
    # AtomServiceUtil.generateAtomServiceCMakeLists(service_image_detection)
    # AtomServiceUtil.generateAtomServiceCMakeLists(service_motor_data)
    # AtomServiceUtil.generateAtomServiceCMakeLists(service_radar_data)
    # AtomServiceUtil.generateAtomServiceCMakeLists(service_robot_pose)
    # AtomServiceUtil.generateAtomServiceCMakeLists(service_fusion_data)

    # AtomServiceUtil.compileAtomService(service_image_detection)
    # AtomServiceUtil.compileAtomService(service_motor_data)
    # AtomServiceUtil.compileAtomService(service_radar_data)
    # AtomServiceUtil.compileAtomService(service_robot_pose)
    # AtomServiceUtil.compileAtomService(service_fusion_data)

    # # 生成idl并编译
    # DDSUtil.generateIdl(service_image_detection)
    # DDSUtil.generateIdl(service_motor_data)
    # DDSUtil.generateIdl(service_radar_data)
    # DDSUtil.generateIdl(service_robot_pose)
    # DDSUtil.generateIdl(service_fusion_data)

    # DDSUtil.generateIdlCMakeLists(service_image_detection)
    # DDSUtil.generateIdlCMakeLists(service_motor_data)
    # DDSUtil.generateIdlCMakeLists(service_radar_data)
    # DDSUtil.generateIdlCMakeLists(service_robot_pose)
    # DDSUtil.generateIdlCMakeLists(service_fusion_data)

    # DDSUtil.compileIdl(service_image_detection)
    # DDSUtil.compileIdl(service_motor_data)
    # DDSUtil.compileIdl(service_radar_data)
    # DDSUtil.compileIdl(service_robot_pose)
    # DDSUtil.compileIdl(service_fusion_data)

    """
    编译节点文件
    """
    Util.compileCmakeProject(
        cmake_dir="/root/micro_service/server_compiling/db/dds_app/FusionDataDemo",
        file_name="StartPublisher_1.cpp",
        file_type="cpp",
    )
