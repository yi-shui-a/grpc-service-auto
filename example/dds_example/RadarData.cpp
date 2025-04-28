#include "RadarData.h"

// 实现获取单例实例的静态方法
RadarList& RadarList::getInstance() {
    static RadarList instance;
    return instance;
}

// 添加新的雷达
void RadarList::addRadar(int id) {
    for (const auto& radar : radars) {
        if (radar.radar_id == id) {
            return; // 雷达已存在，无需重复添加
        }
    }
    radars.emplace_back(id);
}
 
// 删除指定的雷达
void RadarList::deleteRadar(int id){
    for (auto it = radars.begin(); it != radars.end(); ++it) {
        if (it->radar_id == id) {
            radars.erase(it);
            return; // 成功删除雷达
        }
    }
    // 如果未找到指定的雷达，打印错误信息
    std::cerr << "Radar with ID " << id << " not found." << std::endl;
}


// 设置指定雷达的距离
void RadarList::setDistance(int radar_id, double distance) {
    for (auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            radar.distance = distance;
            return;
        }
    }
}

// 获取指定雷达的距离
double RadarList::getDistance(int radar_id) {
    for (const auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            return radar.distance;
        }
    }
    return 0.0; // 未找到雷达，返回默认值
}

// 设置指定雷达的角度
void RadarList::setAngle(int radar_id, double angle) {
    for (auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            radar.angle = angle;
            return;
        }
    }
}

// 获取指定雷达的角度
double RadarList::getAngle(int radar_id) {
    for (const auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            return radar.angle;
        }
    }
    return 0.0; // 未找到雷达，返回默认值
}

// 设置指定雷达的速度
void RadarList::setVelocity(int radar_id, double velocity) {
    for (auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            radar.velocity = velocity;
            return;
        }
    }
}

// 获取指定雷达的速度
double RadarList::getVelocity(int radar_id) {
    for (const auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            return radar.velocity;
        }
    }
    return 0.0; // 未找到雷达，返回默认值
}

// 设置指定雷达的目标类型
void RadarList::setTargetType(int radar_id, const std::string& target_type) {
    for (auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            radar.target_type = target_type;
            return;
        }
    }
}

// 获取指定雷达的目标类型
std::string RadarList::getTargetType(int radar_id) {
    for (const auto& radar : radars) {
        if (radar.radar_id == radar_id) {
            return radar.target_type;
        }
    }
    return ""; // 未找到雷达，返回空字符串
}

// 获取指定索引的雷达 ID
int RadarList::getRadarID(int index) {
    if (index >= 0 && index < static_cast<int>(radars.size())) {
        return radars[index].radar_id;
    }
    return -1; // 索引越界，返回 -1
}


//启动雷达
int StartRadar(RequestSignal *requestSignal, OperationResult *operationResult){
    // 随机生成一个检测结果
    RadarList& radarList = RadarList::getInstance();
    int radar_id = requestSignal -> radar_id;
    radarList.addRadar(radar_id); // 若雷达不存在则添加
    operationResult->status_code = 1;
    operationResult->description = "Radar is ready";
    return ATOMIC_SERVICE_SUCCESS;
}

//停止雷达
int StopRadar(RequestSignal *requestSignal, OperationResult *operationResult){
    // 随机生成一个检测结果
    RadarList& radarList = RadarList::getInstance();
    int radar_id = requestSignal -> radar_id;
    radarList.deleteRadar(radar_id); // 若雷达不存在则添加
    operationResult->status_code = 1;
    operationResult->description = "Radar is stop";
    return ATOMIC_SERVICE_SUCCESS;
}

//获取雷达状态
int statusDetect(RequestSignal *requestSignal, RadarResult *radarResult){
    // 随机生成一个状态
    RadarList& radarList = RadarList::getInstance();
    int radar_id = requestSignal -> radar_id;
    // 先随机数为雷达生成数据
    radarList.setAngle(radar_id, 100.0);
    radarList.setDistance(radar_id, 100.0);
    radarList.setVelocity(radar_id, 100.0);
    radarList.setTargetType(radar_id, "person");

    //再为radarStatus返回数据
    radarResult -> distance = radarList.getDistance(radar_id);
    radarResult -> angle = radarList.getAngle(radar_id);
    radarResult -> velocity = radarList.getVelocity(radar_id);
    radarResult -> target_type = radarList.getTargetType(radar_id);
    return ATOMIC_SERVICE_SUCCESS;
}