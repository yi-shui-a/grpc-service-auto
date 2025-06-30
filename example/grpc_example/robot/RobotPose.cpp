#include "RobotPose.h"

// 实现私有构造函数
Robot::Robot() : gen(std::chrono::system_clock::now().time_since_epoch().count()) {}

// 实现获取单例实例的静态方法
Robot& Robot::getInstance() {
    static Robot instance;
    return instance;
}

double Robot::randomDouble(double min, double max) {
    std::uniform_real_distribution<double> dis(min, max);
    return dis(gen);
}

int Robot::randomInt(int min, int max) {
    std::uniform_int_distribution<int> dis(min, max);
    return dis(gen);
}

int Robot::getRobotId() {
    return randomInt(1, 1000);
}

double Robot::getX() {
    return randomDouble(-100.0, 100.0);
}

double Robot::getY() {
    return randomDouble(-100.0, 100.0);
}

double Robot::getZ() {
    return randomDouble(0.0, 10.0);
}

double Robot::getRoll() {
    return randomDouble(-M_PI, M_PI);
}

double Robot::getPitch() {
    return randomDouble(-M_PI / 2, M_PI / 2);
}

double Robot::getYaw() {
    return randomDouble(-M_PI, M_PI);
}


int getRobotPose(RequestSignal_2 *requestSignal, RobotResult *robotResult){
    Robot& robot = Robot::getInstance();
    robotResult->robot_id = robot.getRobotId();
    robotResult->x = robot.getX();
    robotResult->y = robot.getY();
    robotResult->z = robot.getZ();
    robotResult->roll = robot.getRoll();
    robotResult->pitch = robot.getPitch();
    robotResult->yaw = robot.getYaw();
    return ATOMIC_SERVICE_SUCCESS;
}