#include "atomic_show_zlsc.h"

int atomic_service_fun_task_A(state_info *request, command *reply){
	// TODO: add your code here
    std::random_device rd;  // 用于获取随机种子
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 100); 
    reply->signal = dis(gen);
    
    return ATOMIC_SERVICE_SUCCESS;
}
