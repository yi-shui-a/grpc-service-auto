#include "../atom_inc/atomic_service_mbsb.h"

if 0
int atomic_service_mbsb(atomic_service_mbsb_Request_st *request, atomic_service_mbsb_Reply_st *reply){
    // TODO: add your code here
    /* logic code */
    /*
    if (ptr == NULL){
        return -1;
    }
    else if (ptr->id != 666){
        return -2;
    }
    else if (ptr->np == 0){
        return -3;
    }
    */
    return 0;
}
#endif

void atomic_service_mbsb_interface(atomic_service_mbsb_Request_st *request, atomic_service_mbsb_Reply_st *reply) {
    // Function implementation TODO 
    int ret = atomic_service_mbsb(request, reply);
    reply->error_type = ret;
}