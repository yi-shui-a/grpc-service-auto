#include "atomic_show_ztjs.h"

int getZTJSData(ztjs_input *request, ztjs_output *reply){
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    reply->size = request->size;
    return ATOMIC_SERVICE_SUCCESS;
}