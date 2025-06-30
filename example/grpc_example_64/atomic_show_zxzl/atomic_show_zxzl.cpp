#include "atomic_show_zxzl.h"

int getZXZLresult(zxzl_input *request, zxzl_output *reply)
{
    // TODO: add your code here
    reply->signal = request->x + request->y - request->z;

    return ATOMIC_SERVICE_SUCCESS;
}
