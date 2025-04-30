#ifndef _IMAGE_DETECTION_H_
#define _IMAGE_DETECTION_H_

/*------------------------ Include Begin --------------------------*/

#include <iostream>
#include <fstream>
#include <chrono>
#include <string>

#include <cmath>
#include <vector>
#include <map>
#include <set>

/*------------------------  Include End  -------------------------*/

/*------------------------  Service Info Begin  --------------------------*/
/**
 *
 * @name:     FusionData
 * @chinese_name: 数据融合
 * @description: information FusionData
 * @version: V1.0.0
 * @build_time: 2024-05-23 16:00:00
 * @license: MIT
 * @service_path: FusionData
 *
 * @resource_requirement:
 *         + cpu_architecture: x86_64
 *         + memory: 4GB
 *         + hard_disk: 50GB
 *
 * @developer:
 *      +name: Spiderman
 *      +email: Spidermsan@atomic_service_fwgz.com
 * @maintainer:
 *      +name: yishui
 *      +email:yishui@atomic_service_fwgz.com
 * @operating_system:
 *      +name:Linux
 *      +v1:5.13.0-117-generic
 *      +v2:5.14.0-117-generic
 *      +name:SylixOS
 *      +v1:1.0.0
 *      +v2:1.0.2
 *
 *
 *
 */
/*------------------------  Service Info End  --------------------------*/

/*------------------------  Return Type Begin  --------------------------*/

#define ATOMIC_SERVICE_SUCCESS 0
#define ATOMIC_SERVICE_FAIL -1
#define ATOMIC_SERVICE_TIMEOUT -2
#define ATOMIC_SERVICE_ERROR -3
#define ATOMIC_SERVICE_NOT_SUPPORT -4
#define ATOMIC_SERVICE_NOT_READY -5
#define ATOMIC_SERVICE_NOT_INIT -6
#define ATOMIC_SERVICE_NOT_START -7
#define ATOMIC_SERVICE_NOT_STOP -8
#define ATOMIC_SERVICE_NOT_RELEASE -9
#define ATOMIC_SERVICE_NOT_DESTROY -10
#define ATOMIC_SERVICE_NOT_CREATE -11
#define ATOMIC_SERVICE_NOT_OPEN -12
#define ATOMIC_SERVICE_NOT_CLOSE -13
#define ATOMIC_SERVICE_NOT_READ -14
#define ATOMIC_SERVICE_NOT_WRITE -15
#define ATOMIC_SERVICE_NOT_SEEK -16
#define ATOMIC_SERVICE_NOT_TELL -17
#define ATOMIC_SERVICE_NOT_SIZE -18
#define ATOMIC_SERVICE_NOT_SEEK_END -19
#define ATOMIC_SERVICE_NOT_SEEK_SET -20
#define ATOMIC_SERVICE_NOT_SEEK_CUR -21
#define ATOMIC_SERVICE_NOT_SEEK_ABS -22

/*------------------------  Return Type End  --------------------------*/

/*------------------------  Message Info Begin  --------------------------*/
typedef struct
{
    int signal;
} RequestSignal;

typedef struct
{
    int camera_id;            // 相机 ID
    std::string object_class; // 检测到的对象类别
    double confidence;        // 置信度
    double x_min;             // 边界框左上角 X
    double y_min;             // 边界框左上角 Y
    double x_max;             // 边界框右下角 X
    double y_max;             // 边界框右下角 Y
    int return_type;
} DetectionResult;

typedef struct
{
    int motor_id;       // 电机 ID
    double speed;       // 当前速度
    double temperature; // 温度
    std::string status; // 状态信息
    int return_type;
} MotorResult;

typedef struct
{
    int radar_id;            // 雷达 ID
    double distance;         // 距离
    double angle;            // 角度
    double velocity;         // 速度
    std::string target_type; // 目标类型
    int return_type;
} RadarResult;

typedef struct
{
    int robot_id; //  ID
    double x;     // X 坐标
    double y;     // Y 坐标
    double z;     // Z 坐标
    double roll;  // 横滚角
    double pitch; // 俯仰角
    double yaw;   // 偏航角
    int return_type;
} RobotResult;

typedef struct
{
    DetectionResult detection_result; // 检测结果
    RadarResult radar_result;         // 雷达结果
    RobotResult robot_result;         // 机器人结果
    MotorResult motor_result;         // 电机结果
} FusionInput;

typedef struct
{
    DetectionResult detection_result; // 检测结果
    RadarResult radar_result;         // 雷达结果
    RobotResult robot_result;         // 机器人结果
    MotorResult motor_result;         // 电机结果
    int return_type;
} FusionOutput;

typedef struct
{
    int code;           // 状态码
    std::string status; // 状态信息
    int return_type;
} FusionStatus;

/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

int getFusionData(FusionInput *fusionInput, FusionOutput *fusionOutput);

// int getFusionData(DetectionResult *detectionResult, FusionStatus *fusionStatus);
// int imageDetect(RequestSignal *requestSignal, DetectionResult *detectionResult);
// int statusDetect(RequestSignal *requestSignal, CameraStatus *cameraStatus);

/*------------------------  Interface Declaration End  --------------------------*/

#endif // _IMAGE_DETECTION_H_
