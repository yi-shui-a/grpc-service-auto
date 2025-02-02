


/* 服务框架调用接口 */
void atomic_service_mbsb_func_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply);
void atomic_service_mbsb_func_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply);
void atomic_service_mbsb_func_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply);
void atomic_service_mbsb_func_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply);

// eg:
/*
int atomic_service_mbsb_funcE(atomic_service_mbsb_task_E_Request_st *request, atomic_service_mbsb_task_E_Reply_st *reply);
int atomic_service_mbsb_funcF(atomic_service_mbsb_task_F_Request_st *request, atomic_service_mbsb_task_F_Reply_st *reply);
int atomic_service_mbsb_funcG(atomic_service_mbsb_task_G_Request_st *request, atomic_service_mbsb_task_G_Reply_st *reply);
int atomic_service_mbsb_funcH(atomic_service_mbsb_task_H_Request_st *request, atomic_service_mbsb_task_H_Reply_st *reply);
*/

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

