syntax = "proto3";

package atomic_service_sf_Package;



message atomic_service_sf_task_C_Request_st {
    
    string name = 1;
    
    string title = 2;
    
}


message atomic_service_sf_task_C_Reply_st {
    
    string result = 1;
    
    int32 return_type = 2;
    
}


message atomic_service_sf_task_D_Request_st {
    
    repeated int32 int_array = 1;
    
}


message atomic_service_sf_task_D_Reply_st {
    
    map<string, int32> string_int_map_reply = 1;
    
    int32 return_type = 2;
    
}




service atomic_service_sf_Service {
    
    rpc atomic_service_fun_task_C (atomic_service_sf_task_C_Request_st) returns (atomic_service_sf_task_C_Reply_st) {}
    
    rpc atomic_service_fun_task_D (atomic_service_sf_task_D_Request_st) returns (atomic_service_sf_task_D_Reply_st) {}
    
}
