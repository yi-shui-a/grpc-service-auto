#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_mbsb.grpc.pb.h"
#include "../atom_service/atomic_service_mbsb/atomic_service_mbsb.h"


void atomic_service_fun_task_A_func(atomic_service_mbsb_task_A_Request_st* request, atomic_service_mbsb_task_A_Reply_st* reply);


void atomic_service_fun_task_B_func(atomic_service_mbsb_task_B_Request_st* request, atomic_service_mbsb_task_B_Reply_st* reply);



class atomic_service_mbsb_Service_ServerImpl final : public ::atomic_service_mbsb_Package::atomic_service_mbsb_Service::Service {
public:
    atomic_service_mbsb_Service_ServerImpl() {} 
    

    ::grpc::Status atomic_service_fun_task_A(::grpc::ServerContext* context, 
            const ::atomic_service_mbsb_Package::atomic_service_mbsb_task_A_Request_st* request, 
                ::atomic_service_mbsb_Package::atomic_service_mbsb_task_A_Reply_st* reply) override {

        atomic_service_mbsb_task_A_Request_st atomic_service_mbsb_Request_t;
        atomic_service_mbsb_task_A_Reply_st atomic_service_mbsb_Reply_t;

        
        
        atomic_service_mbsb_Request_t.number1 = request->number1();
        
        
        
        atomic_service_mbsb_Request_t.number2 = request->number2();
        
        

        /******************************************************************/
        atomic_service_fun_task_A_func(&atomic_service_mbsb_Request_t, &atomic_service_mbsb_Reply_t);

        /******************************************************************/

        reply->Clear(); // clear reply message
        
        
        reply->set_sum_result(atomic_service_mbsb_Reply_t.sum_result);
        
        
        
        reply->set_return_type(atomic_service_mbsb_Reply_t.return_type);
        
        
        std::cout << "This is Method = atomic_service_fun_task_A,   ServiceName = atomic_service_mbsb_Service" << std::endl;
        return grpc::Status::OK;
    }

    

    ::grpc::Status atomic_service_fun_task_B(::grpc::ServerContext* context, 
            const ::atomic_service_mbsb_Package::atomic_service_mbsb_task_B_Request_st* request, 
                ::atomic_service_mbsb_Package::atomic_service_mbsb_task_B_Reply_st* reply) override {

        atomic_service_mbsb_task_B_Request_st atomic_service_mbsb_Request_t;
        atomic_service_mbsb_task_B_Reply_st atomic_service_mbsb_Reply_t;

        
        
        atomic_service_mbsb_Request_t.number1 = request->number1();
        
        
        
        atomic_service_mbsb_Request_t.number2 = request->number2();
        
        

        /******************************************************************/
        atomic_service_fun_task_B_func(&atomic_service_mbsb_Request_t, &atomic_service_mbsb_Reply_t);

        /******************************************************************/

        reply->Clear(); // clear reply message
        
        
        reply->set_sub_result(atomic_service_mbsb_Reply_t.sub_result);
        
        
        
        reply->set_return_type(atomic_service_mbsb_Reply_t.return_type);
        
        
        std::cout << "This is Method = atomic_service_fun_task_B,   ServiceName = atomic_service_mbsb_Service" << std::endl;
        return grpc::Status::OK;
    }

    
};