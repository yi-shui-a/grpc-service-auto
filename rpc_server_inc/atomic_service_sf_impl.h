#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpcpp/grpcpp.h>
#include "../protos/atomic_service_sf.grpc.pb.h"
#include "../atom_inc/atomic_service_sf.h"


void atomic_service_fun_task_C_func(atomic_service_sf_task_C_Request_st* request, atomic_service_sf_task_C_Reply_st* reply);


void atomic_service_fun_task_D_func(atomic_service_sf_task_D_Request_st* request, atomic_service_sf_task_D_Reply_st* reply);



class atomic_service_sf_Service_ServerImpl final : public ::atomic_service_sf_Package::atomic_service_sf_Service::Service {
public:
    atomic_service_sf_Service_ServerImpl() {} 
    

    ::grpc::Status atomic_service_fun_task_C(::grpc::ServerContext* context, 
            const ::atomic_service_sf_Package::atomic_service_sf_task_C_Request_st* request, 
                ::atomic_service_sf_Package::atomic_service_sf_task_C_Reply_st* reply) override {

        atomic_service_sf_task_C_Request_st atomic_service_sf_Request_t;
        atomic_service_sf_task_C_Reply_st atomic_service_sf_Reply_t;

        
        
        atomic_service_sf_Request_t.name = request->name();
        
        
        
        atomic_service_sf_Request_t.title = request->title();
        
        

        /******************************************************************/
        atomic_service_fun_task_C_func(&atomic_service_sf_Request_t, &atomic_service_sf_Reply_t);

        /******************************************************************/

        reply->Clear(); // clear reply message
        
        
        reply->set_result(atomic_service_sf_Reply_t.result);
        
        
        
        reply->set_return_type(atomic_service_sf_Reply_t.return_type);
        
        
        std::cout << "This is Method = atomic_service_fun_task_C,   ServiceName = atomic_service_sf_Service" << std::endl;
        return grpc::Status::OK;
    }

    

    ::grpc::Status atomic_service_fun_task_D(::grpc::ServerContext* context, 
            const ::atomic_service_sf_Package::atomic_service_sf_task_D_Request_st* request, 
                ::atomic_service_sf_Package::atomic_service_sf_task_D_Reply_st* reply) override {

        atomic_service_sf_task_D_Request_st atomic_service_sf_Request_t;
        atomic_service_sf_task_D_Reply_st atomic_service_sf_Reply_t;

        
        
        for(int i=0; i < request->int_array_size();++i){
            atomic_service_sf_Request_t.int_array.push_back(request->int_array(i));
        }
        
        

        /******************************************************************/
        atomic_service_fun_task_D_func(&atomic_service_sf_Request_t, &atomic_service_sf_Reply_t);

        /******************************************************************/

        reply->Clear(); // clear reply message
        
        
        for (const auto& item : atomic_service_sf_Reply_t.string_int_map_reply) {
            reply->mutable_string_int_map_reply()->insert({item.first, item.second});
        }
        
        
        
        reply->set_return_type(atomic_service_sf_Reply_t.return_type);
        
        
        std::cout << "This is Method = atomic_service_fun_task_D,   ServiceName = atomic_service_sf_Service" << std::endl;
        return grpc::Status::OK;
    }

    
};