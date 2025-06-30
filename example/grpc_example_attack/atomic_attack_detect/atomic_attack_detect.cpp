#include "atomic_attack_detect.h"

int imageDetect(detect_request *request, detect_result *reply)
{
    // 随机生成一个检测结果
    reply->object_class = "plane";
    reply->confidence = 0.9;
    reply->x_min = request->x - 100;
    reply->y_min = request->y - 100;
    reply->x_max = request->x + 100;
    reply->y_max = request->y + 100;
    return ATOMIC_SERVICE_SUCCESS;
}