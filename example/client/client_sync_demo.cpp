#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>

#include "../rpc_client_inc/atomic_service_mbsb_client.h"
#include "../rpc_client_inc/atomic_service_sf_client.h"

#include "../atom_inc/atomic_service_mbsb.h"
#include "../atom_inc/atomic_service_sf.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

int main(int argc, char **argv)
{
    std::string server_addr = "localhost:50051";
    auto channel = grpc::CreateChannel(server_addr, grpc::InsecureChannelCredentials());
    atomic_service_mbsb_Service_Client mbsb(channel);
    atomic_service_sf_Service_Client sf(channel);

    atomic_service_mbsb_task_A_Request_st request_a;
    atomic_service_mbsb_task_B_Request_st request_b;


    atomic_service_mbsb_task_A_Reply_st reply_a = mbsb.atomic_service_fun_task_A(request_a);
    atomic_service_mbsb_task_B_Reply_st reply_b = mbsb.atomic_service_fun_task_B(request_b);


    atomic_service_sf_task_C_Request_st request_c;
    atomic_service_sf_task_D_Request_st request_d;
    atomic_service_sf_task_C_Reply_st reply_c = sf.atomic_service_fun_task_C(request_c);
    atomic_service_sf_task_D_Reply_st reply_d = sf.atomic_service_fun_task_D(request_d);


    std::cout << "Greeter received: " << reply_a.sum_result << "     return_type: " << reply_a.return_type << std::endl;
    std::cout << "Greeter received: " << reply_b.sub_result << "     return_type: " << reply_b.return_type << std::endl;
    std::cout << "Greeter received: " << reply_c.result << "     return_type: " << reply_c.return_type << std::endl;
    // std::cout << "Greeter received: " << reply_d.string_int_map_reply << "     return_type: " << reply_d.return_type << std::endl;

    return 0;
}