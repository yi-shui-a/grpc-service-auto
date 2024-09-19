#include "../atom_inc/atomic_service_mbsb.h"



int atomic_service_fun_task_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply){
	// TODO: add your code here
    /* logic code */
    /*
	伪代码
    if ( codition ){
        return OperationNotPermitted;
    }
    else if (codition){
        return NoSuchFile;
    }
    else if (codition){
        return NoSuchDir;
    }
    */
    return 0;
}

int atomic_service_fun_task_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply){
	// TODO: add your code here
    /* logic code */
    /*
	伪代码
    if ( codition ){
        return OperationNotPermitted;
    }
    else if (codition){
        return NoSuchFile;
    }
    else if (codition){
        return NoSuchDir;
    }
    */
    return 0;
	
}


int atomic_service_fun_task_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply){
	// TODO: add your code here
    /* logic code */
    /*
	伪代码
    if ( codition ){
        return OperationNotPermitted;
    }
    else if (codition){
        return NoSuchFile;
    }
    else if (codition){
        return NoSuchDir;
    }
    */
    return 0;
}


int atomic_service_fun_task_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply){
	// TODO: add your code here
    /* logic code */
    /*
	伪代码
    if ( codition ){
        return OperationNotPermitted;
    }
    else if (codition){
        return NoSuchFile;
    }
    else if (codition){
        return NoSuchDir;
    }
    */
    return 0;
	
}


void atomic_service_mbsb_func_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply){
	// Function implementation TODO 
    int ret = atomic_service_fun_task_A(request, reply);
    reply->error_type = ret;
}
void atomic_service_mbsb_func_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply){
	// Function implementation TODO 
    int ret = atomic_service_fun_task_B(request, reply);
    reply->error_type = ret;
}
void atomic_service_mbsb_func_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply){
	// Function implementation TODO 
    int ret = atomic_service_fun_task_C(request, reply);
    reply->error_type = ret;
}
void atomic_service_mbsb_func_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply){
	// Function implementation TODO 
    int ret = atomic_service_fun_task_D(request, reply);
    reply->error_type = ret;
}


