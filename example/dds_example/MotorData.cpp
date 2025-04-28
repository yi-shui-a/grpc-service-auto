#include "MotorData.h"

/**
 * 单例模式生成一个Motor类，包含基本的函数和变量
 */
// 实现获取单例实例的静态方法
// 实现获取单例实例的静态方法
MotorList& MotorList::getInstance() {
    static MotorList instance;
    return instance;
}

// 添加新的电机
void MotorList::addMotor(int id) {
    // 如果存在相同 ID 的电机，则不添加
    for (const auto& motor : motors) {
        if (motor.motor_id == id) {
            return;
        }
    }
    motors.emplace_back(id);
}

// 设置指定电机的速度
void MotorList::setSpeed(int motor_id, double speed) {
    for (auto& motor : motors) {
        if (motor.motor_id == motor_id) {
            motor.speed_ = speed;
            return;
        }
    }
}

// 获取指定电机的速度
double MotorList::getSpeed(int motor_id) {
    for (const auto& motor : motors) {
        if (motor.motor_id == motor_id) {
            return motor.speed_;
        }
    }
    return -9999.0; // 未找到电机，返回默认值
}

// 设置指定电机的温度
void MotorList::setTemperature(int motor_id, double temperature) {
    for (auto& motor : motors) {
        if (motor.motor_id == motor_id) {
            motor.temperature = temperature;
            return;
        }
    }
}

// 获取指定电机的温度
double MotorList::getTemperature(int motor_id) {
    for (const auto& motor : motors) {
        if (motor.motor_id == motor_id) {
            return motor.temperature;
        }
    }
    return -9999.0;  // 未找到电机，返回默认值
}

// 设置指定电机的状态
void MotorList::setStatus(int motor_id, const std::string& status) {
    for (auto& motor : motors) {
        if (motor.motor_id == motor_id) {
            motor.status = status;
            return;
        }
    }
}

// 获取指定电机的状态
std::string MotorList::getStatus(int motor_id) {
    for (const auto& motor : motors) {
        if (motor.motor_id == motor_id) {
            return motor.status;
        }
    }
    return ""; // 未找到电机，返回空字符串
}

// 获取指定索引的电机 ID
int MotorList::getMotorID(int index) {
    if (index >= 0 && index < static_cast<int>(motors.size())) {
        return motors[index].motor_id;
    }
    return -1; // 索引越界，返回 -1
}


int StartMotor(RequestSignal *requestSignal, OperationResult *operationResult){
    // 启动 motor signal
    MotorList& motorList = MotorList::getInstance();
    int motor_id = requestSignal -> motor_id;
    motorList.addMotor(motor_id); // 若电机不存在则添加
    motorList.setSpeed(motor_id, 10.0);
    motorList.setTemperature(motor_id, 25.0);
    motorList.setStatus(motor_id, "started");
    operationResult->status_code = 1;
    operationResult->description = "Motor is started";
    return ATOMIC_SERVICE_SUCCESS;
}

int StopMotor(RequestSignal *requestSignal, OperationResult *operationResult){
    // 停止 motor signal
    MotorList& motorList = MotorList::getInstance();
    int motor_id = requestSignal -> motor_id;
    motorList.setSpeed(motor_id, 0.0);
    motorList.setTemperature(motor_id, 0.0);
    motorList.setStatus(motor_id, "stopped");
    operationResult->status_code = 1;
    operationResult->description = "Motor is stopped";
    return ATOMIC_SERVICE_SUCCESS;
}

int statusDetect(RequestSignal *requestSignal, MotorResult *motorResult){
    // 获取 motor status
    MotorList& motorList = MotorList::getInstance();
    int motor_id = requestSignal -> motor_id;
    motorResult->motor_id = motor_id;
    motorResult->temperature = motorList.getTemperature(motor_id);
    motorResult->speed = motorList.getSpeed(motor_id);
    motorResult->status = motorList.getStatus(motor_id);
    return ATOMIC_SERVICE_SUCCESS;
}

int SetMotorSpeed(RequestSpeed *requestSpeed, OperationResult *operationResult){
    // 设置 motor speed
    MotorList& motorList = MotorList::getInstance();
    int motor_id = requestSpeed->motor_id;
    motorList.setSpeed(motor_id, requestSpeed->speed);
    operationResult->status_code = 1;
    operationResult->description = "Motor speed is set to " + std::to_string(requestSpeed->speed);
    return ATOMIC_SERVICE_SUCCESS;
}