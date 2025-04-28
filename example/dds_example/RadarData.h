#ifndef _RADAR_DATA_H_
#define _RADAR_DATA_H_

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
 * @name:     RadarData
 * @chinese_name: 雷达数据
 * @description: information RadarData
 * @version: V1.0.0
 * @build_time: 2024-05-23 16:00:00
 * @license: MIT
 * @service_path: RadarData
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

// 定义 Radar 结构体
struct Radar {
    int radar_id;      // 雷达 ID
    double distance;    // 距离
    double angle;       // 角度
    double velocity;    // 速度
    std::string target_type; // 目标类型

    // 构造函数
    Radar(int id) : radar_id(id), distance(0.0), angle(0.0), velocity(0.0), target_type("") {}
};

// 单例模式的 RadarList 类
class RadarList {
private:
    std::vector<Radar> radars;

    // 私有构造函数，防止外部实例化
    RadarList() = default;
    // 私有析构函数，防止外部删除实例
    ~RadarList() = default;
    // 禁用拷贝构造函数
    RadarList(const RadarList&) = delete;
    // 禁用赋值运算符
    RadarList& operator=(const RadarList&) = delete;

public:
    // 获取单例实例的静态方法
    static RadarList& getInstance();

    // 添加新的雷达
    void addRadar(int id);
	// 删除指定的雷达
    void deleteRadar(int id);
    // 设置指定雷达的距离
    void setDistance(int radar_id, double distance);
    // 获取指定雷达的距离
    double getDistance(int radar_id);
    // 设置指定雷达的角度
    void setAngle(int radar_id, double angle);
    // 获取指定雷达的角度
    double getAngle(int radar_id);
    // 设置指定雷达的速度
    void setVelocity(int radar_id, double velocity);
    // 获取指定雷达的速度
    double getVelocity(int radar_id);
    // 设置指定雷达的目标类型
    void setTargetType(int radar_id, const std::string& target_type);
    // 获取指定雷达的目标类型
    std::string getTargetType(int radar_id);
    // 获取指定雷达的 ID
    int getRadarID(int index);
};


/*------------------------  Message Info Begin  --------------------------*/
typedef struct
{
	int signal;
	int radar_id;
} RequestSignal;

typedef struct
{
	int radar_id;
	double speed;
} RequestSpeed;

typedef struct
{
	int radar_id;			 // 雷达 ID
	double distance;		 // 距离
	double angle;			 // 角度
	double velocity;		 // 速度
	std::string target_type; // 目标类型
	int return_type;
} RadarResult;

typedef struct
{
	int status_code;
	std::string description;
	int return_type;
} OperationResult;

/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

int StartRadar(RequestSignal *requestSignal, OperationResult *operationResult);
int StopRadar(RequestSignal *requestSignal, OperationResult *operationResult);
int statusDetect(RequestSignal *requestSignal, RadarResult *radarResult);


/*------------------------  Interface Declaration End  --------------------------*/

#endif // _RADAR_DATA_H_
