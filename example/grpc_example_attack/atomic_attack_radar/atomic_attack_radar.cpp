#include "atomic_attack_radar.h"

int getRaderMonitor(radar_info *request, radar_result *reply){
    reply->x = request ->x;
    reply->y = request ->y;
    reply->z = request ->z;
    reply->size = request->size * request->size;
    return ATOMIC_SERVICE_SUCCESS;
}
int getRaderState(radar_signal *request, radar_state *reply){
    reply->id = request->id;
    reply->state = 100;
    reply->result = "Normal status";
    return ATOMIC_SERVICE_SUCCESS;
}