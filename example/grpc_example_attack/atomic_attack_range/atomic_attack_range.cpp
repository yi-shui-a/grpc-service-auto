#include "atomic_attack_range.h"

int imageRange(range_request *request, range_result *reply)
{
    // 随机生成一个检测结果
    reply->z = request->z;
    return ATOMIC_SERVICE_SUCCESS;
}