#include "atomic_show_cgsj.h"

int getCGSJData(cgsj_input *request, cgsj_output *reply){
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    reply->size = request->size;
    return ATOMIC_SERVICE_SUCCESS;
}