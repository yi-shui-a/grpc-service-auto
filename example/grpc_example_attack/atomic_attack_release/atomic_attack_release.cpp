#include "atomic_attack_release.h"

int getTargetInfo(release_request *request, release_result *reply)
{
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    return ATOMIC_SERVICE_SUCCESS;
}