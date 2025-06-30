#include "atomic_service_ycl.h"

int atomic_service_fun_task_E(input_info *request, process_result *reply){
	// TODO: add your code here
    reply->x = 1312;
    reply->y = 124;
    reply->z = 23;
    return ATOMIC_SERVICE_SUCCESS;
}
