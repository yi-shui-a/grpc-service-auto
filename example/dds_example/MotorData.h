#ifndef _MOTOR_DATA_H_
#define _MOTOR_DATA_H_

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
 * @name:     MotorData
 * @chinese_name: 电机数据
 * @description: information MotorData
 * @version: V1.0.0
 * @build_time: 2024-05-23 16:00:00
 * @license: MIT
 * @service_path: MotorData
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

// 定义 Motor 结构体
struct Motor {
    int motor_id;
    double speed_;
    double temperature;
    std::string status;

    Motor(int id) : motor_id(id), speed_(0.0), temperature(0.0), status("") {}
};

// 单例模式的 MotorList 类
class MotorList {
private:
    std::vector<Motor> motors;

    // 私有构造函数，防止外部实例化
    MotorList() = default;
    // 私有析构函数，防止外部删除实例
    ~MotorList() = default;
    // 禁用拷贝构造函数
    MotorList(const MotorList&) = delete;
    // 禁用赋值运算符
    MotorList& operator=(const MotorList&) = delete;

public:
    // 获取单例实例的静态方法
    static MotorList& getInstance();

    // 添加新的电机
    void addMotor(int id);
    // 设置指定电机的速度
    void setSpeed(int motor_id, double speed);
    // 获取指定电机的速度
    double getSpeed(int motor_id);
    // 设置指定电机的温度
    void setTemperature(int motor_id, double temperature);
    // 获取指定电机的温度
    double getTemperature(int motor_id);
    // 设置指定电机的状态
    void setStatus(int motor_id, const std::string& status);
    // 获取指定电机的状态
    std::string getStatus(int motor_id);
    // 获取指定电机的 ID
    int getMotorID(int index);
};

/*------------------------  Message Info Begin  --------------------------*/
typedef struct
{
	int signal;
	int motor_id;
} RequestSignal;

typedef struct
{
	double speed;
	int motor_id;
} RequestSpeed;

typedef struct
{
	int motor_id;		// 电机 ID
	double speed;		// 当前速度
	double temperature; // 温度
	std::string status; // 状态信息
	int return_type;
} MotorResult;

typedef struct
{
	int status_code;
	std::string description;
	int return_type;
} OperationResult;

// extern int status;

/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

int StartMotor(RequestSignal *requestSignal, OperationResult *operationResult);
int StopMotor(RequestSignal *requestSignal, OperationResult *operationResult);
int statusDetect(RequestSignal *requestSignal, MotorResult *motorResult);
int SetMotorSpeed(RequestSpeed *requestSpeed, OperationResult *operationResult);

/*------------------------  Interface Declaration End  --------------------------*/

#endif // _MOTOR_DATA_H_
