#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_mbsb.grpc.pb.h"
#include "../protos/atomic_service_mbsb.pb.h"
#include "../atom_inc/atomic_service_mbsb.h"
class atomic_service_mbsb_Service_Client {
public:
    atomic_service_mbsb_Service_Client(std::shared_ptr<::grpc::Channel> channel)
        : stub_(::atomic_service_mbsb_Package::atomic_service_mbsb_Service::NewStub(channel)){}
    
    
    
    
private:
    std::unique_ptr<::atomic_service_mbsb_Package::atomic_service_mbsb_Service::Stub> stub_;
};