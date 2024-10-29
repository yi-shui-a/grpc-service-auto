#include "../atom_inc/atomic_service_sf.h"

int atomic_service_fun_task_C(atomic_service_sf_task_C_Request_st *request, atomic_service_sf_task_C_Reply_st *reply)
{

    request->name = "bob";
    request->title = "doctor";
    reply->result = request->name + "--" + request->title;

    return ATOMIC_SERVICE_SUCCESS;
}

int atomic_service_fun_task_D(atomic_service_sf_task_D_Request_st *request, atomic_service_sf_task_D_Reply_st *reply)
{
    request->int_array = {1, 3, 5, 7, 9};
    std::vector<std::string> sss = {"11", "33", "55", "77", "99"};
    for (int i = 0; i < request->int_array.size(); ++i)
    {
        reply->string_int_map_reply[sss[i]] = request->int_array[i];
    }
    return ATOMIC_SERVICE_SUCCESS;
}

 void atomic_service_fun_task_C_func(atomic_service_sf_task_C_Request_st *request, atomic_service_sf_task_C_Reply_st *reply){
 	// Function implementation TODO
     int ret_type = atomic_service_fun_task_C(request, reply);
     reply->return_type = ret_type;
 }

 void atomic_service_fun_task_D_func(atomic_service_sf_task_D_Request_st *request, atomic_service_sf_task_D_Reply_st *reply){
 	// Function implementation TODO
     int ret_type = atomic_service_fun_task_D(request, reply);
     reply->return_type = ret_type;
 }

