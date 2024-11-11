#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include <netdb.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <nlohmann/json.hpp>


#include "../rpc_client_inc/atomic_service_mbsb_client.h"
#include "../atom_inc/atomic_service_mbsb.h"

#include "../rpc_client_inc/atomic_service_sf_client.h"
#include "../atom_inc/atomic_service_sf.h"

class atomic_service_mbsb_Client;

class atomic_service_sf_Client;




int main(int argc, char** argv) {

    std::string server_addr = "localhost:50051";
    auto channel = grpc::CreateChannel(server_addr, grpc::InsecureChannelCredentials());
    // TODO add *Client 
    // GreeterClient greeter(channel);
    // AtomServerSJClient atom_server_sj_client(channel);

    

    
    atomic_service_mbsb_Service_Client atomic_service_mbsb(channel);
    
    atomic_service_sf_Service_Client atomic_service_sf(channel);
    
    
    std::cout << "<<<<<<<<<<<<<<<<<< Call the RPC << atomic_service_sfzt>> and wait for response >>>>>>>>>>>>>>>>>>>>>" << std::endl;
    atomic_service_sfzt_Reply_st atomic_service_sfzt_rpc_reply = atomic_service_sfzt.UnitaryStream(atomic_service_sfzt_Request_st);
    std::cout << "Greeter received: " << atomic_service_sfzt_rpc_reply.message << std::endl;
    std::cout << "Greeter received: " << atomic_service_sfzt_rpc_reply.integer_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_sfzt_rpc_reply.double_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_sfzt_rpc_reply.float_reply<< std::endl;
    for(int i = 0; i < atomic_service_sfzt_rpc_reply.int_array_reply.size(); i++){
        std::cout << "atomic_service_sfzt received: " << atomic_service_sfzt_rpc_reply.int_array_reply[i] << std::endl;
    }
    for (const auto& pair : atomic_service_sfzt_rpc_reply.string_int_map_reply) {
        std::cout<< "atomic_service_sfzt map data:" << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }

    return 0;
}