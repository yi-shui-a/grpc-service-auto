#include "atomic_show_ddpc.h"

int getDDPCData(ddpc_input *request, ddpc_output *reply){
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    reply->size = request->size;
    return ATOMIC_SERVICE_SUCCESS;
}