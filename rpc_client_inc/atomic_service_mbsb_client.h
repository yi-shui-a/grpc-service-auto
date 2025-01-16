#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_mbsb.grpc.pb.h"
#include "../protos/atomic_service_mbsb.pb.h"
#include "../atom_service/atomic_service_mbsb/atomic_service_mbsb.h"
class atomic_service_mbsb_Service_Client {
public:
    atomic_service_mbsb_Service_Client(std::shared_ptr<::grpc::Channel> channel)
        : stub_(::atomic_service_mbsb_Package::atomic_service_mbsb_Service::NewStub(channel)){}
    

    atomic_service_mbsb_task_A_Reply_st atomic_service_fun_task_A(const atomic_service_mbsb_task_A_Request_st& atomic_service_mbsb_Request_t){
        atomic_service_mbsb_Package::atomic_service_mbsb_task_A_Request_st request;
        
        
        request.set_number1(atomic_service_mbsb_Request_t.number1);
        
        
        
        request.set_number2(atomic_service_mbsb_Request_t.number2);
        
        
        //Received reply data translate to atomic_service_mbsb_Reply_t; 
        atomic_service_mbsb_task_A_Reply_st atomic_service_mbsb_Reply_t;
        atomic_service_mbsb_Package::atomic_service_mbsb_task_A_Reply_st reply;
        ::grpc::ClientContext context;
        ::grpc::Status status = stub_->atomic_service_fun_task_A(&context, request, &reply);
        
        
        atomic_service_mbsb_Reply_t.sum_result = reply.sum_result();
        
        
        
        atomic_service_mbsb_Reply_t.return_type = reply.return_type();
        
        
        if (status.ok()) {
            std::cout << "atomic_service_mbsb--> atomic_service_fun_task_A : Received server data success " << std::endl;
        } else {
            std::cout << "atomic_service_mbsb--> atomic_service_fun_task_A :" << status.error_code() << ": " << status.error_message() << std::endl;
        }
        return atomic_service_mbsb_Reply_t;
    }

    

    atomic_service_mbsb_task_B_Reply_st atomic_service_fun_task_B(const atomic_service_mbsb_task_B_Request_st& atomic_service_mbsb_Request_t){
        atomic_service_mbsb_Package::atomic_service_mbsb_task_B_Request_st request;
        
        
        request.set_number1(atomic_service_mbsb_Request_t.number1);
        
        
        
        request.set_number2(atomic_service_mbsb_Request_t.number2);
        
        
        //Received reply data translate to atomic_service_mbsb_Reply_t; 
        atomic_service_mbsb_task_B_Reply_st atomic_service_mbsb_Reply_t;
        atomic_service_mbsb_Package::atomic_service_mbsb_task_B_Reply_st reply;
        ::grpc::ClientContext context;
        ::grpc::Status status = stub_->atomic_service_fun_task_B(&context, request, &reply);
        
        
        atomic_service_mbsb_Reply_t.sub_result = reply.sub_result();
        
        
        
        atomic_service_mbsb_Reply_t.return_type = reply.return_type();
        
        
        if (status.ok()) {
            std::cout << "atomic_service_mbsb--> atomic_service_fun_task_B : Received server data success " << std::endl;
        } else {
            std::cout << "atomic_service_mbsb--> atomic_service_fun_task_B :" << status.error_code() << ": " << status.error_message() << std::endl;
        }
        return atomic_service_mbsb_Reply_t;
    }

    
private:
    std::unique_ptr<::atomic_service_mbsb_Package::atomic_service_mbsb_Service::Stub> stub_;
};