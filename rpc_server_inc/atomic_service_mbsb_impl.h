#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_mbsb.grpc.pb.h"
#include "../atom_inc/atomic_service_mbsb.h"

void atomic_service_mbsb_interface_func(atomic_service_mbsb_Request_st* request, atomic_service_mbsb_Reply_st* reply);

class atomic_service_mbsb_Service_ServerImpl final : public ::atomic_service_mbsb_Package::atomic_service_mbsb_Service::Service {
public:
    atomic_service_mbsb_Service_ServerImpl() {} 
    
    
    
    
};