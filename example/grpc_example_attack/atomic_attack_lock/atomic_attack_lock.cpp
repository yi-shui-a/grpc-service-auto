#include "atomic_attack_lock.h"

int targetLock(lock_request *request, lock_result *reply)
{
    std::random_device rd;                         // 用于获取随机种子
    std::mt19937 gen(rd());                        // 以随机设备作为种子初始化Mersenne Twister生成器
    std::uniform_int_distribution<> dis(100, 800); // 生成1到100之间的整数
    // 随机生成一个检测结果
    reply->object_class = "plane";
    reply->confidence = request->confidence;
    reply->x = dis(gen);
    reply->y = dis(gen);
    reply->z = request->z;
    return ATOMIC_SERVICE_SUCCESS;
}