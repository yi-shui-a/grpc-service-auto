#include "atomic_test_light.h"

int getLightMonitor(light_info *request, light_result *reply){
    reply->x = request ->x;
    reply->y = request ->y;
    reply->z = request ->z;
    reply->size = request->size * request->size;
    return ATOMIC_SERVICE_SUCCESS;
}
int getLightState(light_signal *request, light_state *reply){
    reply->id = request->id;
    reply->state = 100;
    reply->result = "Normal status";
    return ATOMIC_SERVICE_SUCCESS;
}