#include "atomic_show_ddzt.h"

int getDDZTData(ddzt_input *request, ddzt_output *reply){
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    reply->size = request->size;
    return ATOMIC_SERVICE_SUCCESS;
}