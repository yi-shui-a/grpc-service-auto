#include "atomic_show_sjrh.h"

int getSJRHData(sjrh_input *request, sjrh_output *reply){
    reply->x = request->x;
    reply->y = request->y;
    reply->z = request->z;
    reply->size = request->size;
    return ATOMIC_SERVICE_SUCCESS;
}