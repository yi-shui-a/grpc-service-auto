#include "atomic_service_mbsb.h"

int atomic_service_fun_task_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply){
	
    
    
    reply->sum_result = request->number1 + request->number2;
    
    return ATOMIC_SERVICE_SUCCESS;
}

int atomic_service_fun_task_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply){
	
    request->number1 = 123;
    request->number2 = 456;
    reply->sub_result = request->number1 - request->number2;
    return ATOMIC_SERVICE_SUCCESS;
}

 void atomic_service_fun_task_A_func(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply){
 	// Function implementation TODO
     int ret_type = atomic_service_fun_task_A(request, reply);
     reply->return_type = ret_type;
 }

 void atomic_service_fun_task_B_func(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply){
 	// Function implementation TODO
     int ret_type = atomic_service_fun_task_B(request, reply);
     reply->return_type = ret_type;
 }

