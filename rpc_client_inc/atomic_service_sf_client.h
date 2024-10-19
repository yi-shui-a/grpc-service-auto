#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_sf.grpc.pb.h"
#include "../protos/atomic_service_sf.pb.h"
#include "../atom_inc/atomic_service_sf.h"
class atomic_service_sf_Service_Client {
public:
    atomic_service_sf_Service_Client(std::shared_ptr<::grpc::Channel> channel)
        : stub_(::atomic_service_sf_Package::atomic_service_sf_Service::NewStub(channel)){}
    
    
    
    
private:
    std::unique_ptr<::atomic_service_sf_Package::atomic_service_sf_Service::Stub> stub_;
};