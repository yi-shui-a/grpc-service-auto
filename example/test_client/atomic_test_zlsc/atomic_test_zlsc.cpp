#include "atomic_test_zlsc.h"

int atomic_service_fun_task_A(state_info *request, command *reply){
	// TODO: add your code here
    reply->signal = 40;
    
    return ATOMIC_SERVICE_SUCCESS;
}
