#include "atomic_attack_decode.h"

int decodeImage(iamge_input *request, iamge_output *reply)
{
    reply->x = request->x + 5;
    reply->y = request->y + 5;
    reply->z = request->z + 5;
    reply->size = request->size + 5;
    return ATOMIC_SERVICE_SUCCESS;
}