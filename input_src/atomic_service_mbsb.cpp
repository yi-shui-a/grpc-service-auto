#include "../atom_inc/atomic_service_mbsb.h"

void atomic_service_mbsb_interface(atomic_service_mbsb_Request_st *request, atomic_service_mbsb_Reply_st *reply) {
    // Function implementation TODO 

    reply->message = " from atom_service_mbsb_interface";
    reply->integer_reply = 33333;
    reply->double_reply = 111111;
    reply->float_reply = 22.22;

    std::cout << " >>>>>>>  atomic_service_mbsb_interface called" << std::endl;
}
