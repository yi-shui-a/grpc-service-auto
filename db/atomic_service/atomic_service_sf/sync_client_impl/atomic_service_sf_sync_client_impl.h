#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_sf.grpc.pb.h"
#include "../protos/atomic_service_sf.pb.h"
#include "../atomic_include/atomic_service_sf.h"
class atomic_service_sf_Service_Client {
public:
    atomic_service_sf_Service_Client(std::shared_ptr<::grpc::Channel> channel)
        : stub_(::atomic_service_sf_Package::atomic_service_sf_Service::NewStub(channel)){}
    

    atomic_service_sf_task_C_Reply_st atomic_service_fun_task_C(const atomic_service_sf_task_C_Request_st& atomic_service_sf_Request_t){
        atomic_service_sf_Package::atomic_service_sf_task_C_Request_st request;
        
        
        request.set_name(atomic_service_sf_Request_t.name);
        
        
        
        request.set_title(atomic_service_sf_Request_t.title);
        
        
        //Received reply data translate to atomic_service_sf_Reply_t; 
        atomic_service_sf_task_C_Reply_st atomic_service_sf_Reply_t;
        atomic_service_sf_Package::atomic_service_sf_task_C_Reply_st reply;
        ::grpc::ClientContext context;
        ::grpc::Status status = stub_->atomic_service_fun_task_C(&context, request, &reply);
        
        
        atomic_service_sf_Reply_t.result = reply.result();
        
        
        
        atomic_service_sf_Reply_t.return_type = reply.return_type();
        
        
        if (status.ok()) {
            std::cout << "atomic_service_sf--> atomic_service_fun_task_C : Received server data success " << std::endl;
        } else {
            std::cout << "atomic_service_sf--> atomic_service_fun_task_C :" << status.error_code() << ": " << status.error_message() << std::endl;
        }
        return atomic_service_sf_Reply_t;
    }

    

    atomic_service_sf_task_D_Reply_st atomic_service_fun_task_D(const atomic_service_sf_task_D_Request_st& atomic_service_sf_Request_t){
        atomic_service_sf_Package::atomic_service_sf_task_D_Request_st request;
        
        
        for(int i=0;i < atomic_service_sf_Request_t.int_array.size();i++){
            request.add_int_array(atomic_service_sf_Request_t.int_array[i]);
        }
        
        
        //Received reply data translate to atomic_service_sf_Reply_t; 
        atomic_service_sf_task_D_Reply_st atomic_service_sf_Reply_t;
        atomic_service_sf_Package::atomic_service_sf_task_D_Reply_st reply;
        ::grpc::ClientContext context;
        ::grpc::Status status = stub_->atomic_service_fun_task_D(&context, request, &reply);
        
        
        for (const auto& item : reply.string_int_map_reply()) {
            (atomic_service_sf_Reply_t.string_int_map_reply)[item.first] = item.second;
        }
        
        
        
        atomic_service_sf_Reply_t.return_type = reply.return_type();
        
        
        if (status.ok()) {
            std::cout << "atomic_service_sf--> atomic_service_fun_task_D : Received server data success " << std::endl;
        } else {
            std::cout << "atomic_service_sf--> atomic_service_fun_task_D :" << status.error_code() << ": " << status.error_message() << std::endl;
        }
        return atomic_service_sf_Reply_t;
    }

    
private:
    std::unique_ptr<::atomic_service_sf_Package::atomic_service_sf_Service::Stub> stub_;
};