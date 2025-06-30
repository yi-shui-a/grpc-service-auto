#include "atomic_attack_infrared.h"

int getInfraredMonitor(infrared_info *request, infrared_result *reply){
    reply->x = request ->x;
    reply->y = request ->y;
    reply->z = request ->z;
    reply->size = request->size * request->size;
    return ATOMIC_SERVICE_SUCCESS;
}
int getInfraredState(infrared_signal *request, infrared_state *reply){
    reply->id = request->id;
    reply->state = 100;
    reply->result = "Normal status";
    return ATOMIC_SERVICE_SUCCESS;
}