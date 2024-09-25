#include "../atom_inc/atomic_service_mbsb.h"

int atomic_service_fun_task_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply){
	// TODO: add your code here
    request->number1 = 123;
    request->number2 = 456;
    reply->sum_result = request->number1 + request->number2;
    
    return ATOMIC_SERVICE_SUCCESS;
}

int atomic_service_fun_task_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply){
	// TODO: add your code here
    request->number1 = 123;
    request->number2 = 456;
    reply->sum_result = request->number1 - request->number2;
    return ATOMIC_SERVICE_SUCCESS;
}


int atomic_service_fun_task_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply){
	// TODO: add your code here
    request->number1 = 123;
    request->number2 = 456;
    reply->sum_result = (request->number1) * (request->number2);
    return ATOMIC_SERVICE_SUCCESS;
}


int atomic_service_fun_task_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply){
	// TODO: add your code here
    request->number1 = 123;
    request->number2 = 0;

    if(request->number2 == 0){
        return DATA_ERROR;
    }
    else 
        reply->sum_result = (request->number1) / (request->number2);
    return ATOMIC_SERVICE_SUCCESS;
}


void atomic_service_mbsb_func_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply){
	// Function implementation TODO 
    int ret_type = atomic_service_fun_task_A(request, reply);
    reply->return_type = ret_type;
}
void atomic_service_mbsb_func_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply){
	// Function implementation TODO 
    int ret_type = atomic_service_fun_task_B(request, reply);
    reply->return_type = ret_type;
}
void atomic_service_mbsb_func_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply){
	// Function implementation TODO 
    int ret_type = atomic_service_fun_task_C(request, reply);
    reply->return_type = ret_type;
}
void atomic_service_mbsb_func_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply){
	// Function implementation TODO 
    int ret_type = atomic_service_fun_task_D(request, reply);
    reply->return_type = ret_type;
}


