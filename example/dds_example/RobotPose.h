#ifndef _ROBOT_POSE_H_
#define _ROBOT_POSE_H_

/*------------------------ Include Begin --------------------------*/

#include <iostream>
#include <fstream>
#include <chrono>
#include <string>

#include <cmath>
#include <vector>
#include <map>
#include <set>

#include <random>

/*------------------------  Include End  -------------------------*/

/*------------------------  Service Info Begin  --------------------------*/
/**
 *
 * @name:        RobotPose
 * @chinese_name: 机器人位姿
 * @description: information RobotPose
 * @version: V1.0.0
 * @build_time: 2024-05-23 16:00:00
 * @license: MIT
 * @service_path: RobotPose
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

class Robot
{
private:
	// 随机数引擎
	std::mt19937 gen;

	// 私有构造函数，防止外部实例化
	Robot();
	// 禁用拷贝构造函数
	Robot(const Robot &) = delete;
	// 禁用赋值运算符
	Robot &operator=(const Robot &) = delete;

	// 生成指定范围的随机 double 数
	double randomDouble(double min, double max);
	// 生成指定范围的随机整数
	int randomInt(int min, int max);

public:
	// 获取单例实例的静态方法
	static Robot &getInstance();

	// 获取机器人 ID
	int getRobotId();
	// 获取 X 坐标
	double getX();
	// 获取 Y 坐标
	double getY();
	// 获取 Z 坐标
	double getZ();
	// 获取横滚角
	double getRoll();
	// 获取俯仰角
	double getPitch();
	// 获取偏航角
	double getYaw();
};

/*------------------------  Message Info Begin  --------------------------*/
typedef struct
{
	int signal;
} RequestSignal;

typedef struct
{
	double speed;
} RequestSpeed;

typedef struct
{
	int robot_id; //  ID
	double x;	   // X 坐标
	double y;	   // Y 坐标
	double z;	   // Z 坐标
	double roll;   // 横滚角
	double pitch;  // 俯仰角
	double yaw;	   // 偏航角
	int return_type;
} RobotResult;

typedef struct
{
	int status_code;
	std::string description;
	int return_type;
} OperationResult;

/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

int getRobotPose(RequestSignal *requestSignal, RobotResult *robotResult);

/*------------------------  Interface Declaration End  --------------------------*/

#endif // _ROBOT_POSE_H_
