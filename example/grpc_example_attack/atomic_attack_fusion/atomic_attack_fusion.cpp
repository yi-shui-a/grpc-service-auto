#include "atomic_attack_fusion.h"

int getFusionData(fusion_input *request, fusion_output *reply){
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    reply->size = request->size;
    return ATOMIC_SERVICE_SUCCESS;
}