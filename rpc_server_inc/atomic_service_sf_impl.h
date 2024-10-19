#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_sf.grpc.pb.h"
#include "../atom_inc/atomic_service_sf.h"

void atomic_service_fun_task_C_func(atomic_service_sf_Request_st* request, atomic_service_sf_Reply_st* reply);

class atomic_service_sf_Service_ServerImpl final : public ::atomic_service_sf_Package::atomic_service_sf_Service::Service {
public:
    atomic_service_sf_Service_ServerImpl() {} 
    
    
    
    
};