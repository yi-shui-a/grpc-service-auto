#include "atomic_show_ysdd.h"

int getYSDDData(ysdd_input *request, ysdd_output *reply){
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    reply->size = request->size;
    return ATOMIC_SERVICE_SUCCESS;
}