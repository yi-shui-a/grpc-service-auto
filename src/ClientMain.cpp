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


#include "../rpc_client_inc/atomic_service_sfzt_client.h"
#include "../atom_inc/atomic_service_sfzt.h"

#include "../rpc_client_inc/atomic_service_skzt_client.h"
#include "../atom_inc/atomic_service_skzt.h"

#include "../rpc_client_inc/atomic_service_mbsb_client.h"
#include "../atom_inc/atomic_service_mbsb.h"

#include "../rpc_client_inc/atomic_service_sj_client.h"
#include "../atom_inc/atomic_service_sj.h"

#include "../rpc_client_inc/atomic_service_st_client.h"
#include "../atom_inc/atomic_service_st.h"



class atomic_service_sfzt_Client;

class atomic_service_skzt_Client;

class atomic_service_mbsb_Client;

class atomic_service_sj_Client;

class atomic_service_st_Client;


int main(int argc, char** argv) {

    std::string server_addr = "localhost:50051";
    auto channel = grpc::CreateChannel(server_addr, grpc::InsecureChannelCredentials());
    // TODO add *Client 
    // GreeterClient greeter(channel);
    // AtomServerSJClient atom_server_sj_client(channel);

    
    atomic_service_sfzt_Service_Client atomic_service_sfzt(channel);
    
    atomic_service_skzt_Service_Client atomic_service_skzt(channel);
    
    atomic_service_mbsb_Service_Client atomic_service_mbsb(channel);
    
    atomic_service_sj_Service_Client atomic_service_sj(channel);
    
    atomic_service_st_Service_Client atomic_service_st(channel);
    

    
    atomic_service_sfzt_Request_st atomic_service_sfzt_Request_st;
    atomic_service_sfzt_Reply_st atomic_service_sfzt_Reply_t;

    atomic_service_sfzt_Request_st.name ="atomic_service_sfzt";
    atomic_service_sfzt_Request_st.integer_field = 123;
    atomic_service_sfzt_Request_st.double_field = 123.123;
    atomic_service_sfzt_Request_st.float_field = 12.12;
    std::vector<int> atomic_service_sfzt_int_array_var;
    for(int i=0;i<20;i++) {
        atomic_service_sfzt_int_array_var.push_back(11);
    }
    atomic_service_sfzt_Request_st.int_array = atomic_service_sfzt_int_array_var;
    std::map<std::string, int32_t> atomic_service_sfzt_string_int_map_var;
    for(int i = 0; i < 10; i++) {
        atomic_service_sfzt_string_int_map_var["key_" + std::to_string(i)] = i+100;
    }
    atomic_service_sfzt_Request_st.string_int_map = atomic_service_sfzt_string_int_map_var;
    
    atomic_service_skzt_Request_st atomic_service_skzt_Request_st;
    atomic_service_skzt_Reply_st atomic_service_skzt_Reply_t;

    atomic_service_skzt_Request_st.name ="atomic_service_skzt";
    atomic_service_skzt_Request_st.integer_field = 123;
    atomic_service_skzt_Request_st.double_field = 123.123;
    atomic_service_skzt_Request_st.float_field = 12.12;
    std::vector<int> atomic_service_skzt_int_array_var;
    for(int i=0;i<20;i++) {
        atomic_service_skzt_int_array_var.push_back(11);
    }
    atomic_service_skzt_Request_st.int_array = atomic_service_skzt_int_array_var;
    std::map<std::string, int32_t> atomic_service_skzt_string_int_map_var;
    for(int i = 0; i < 10; i++) {
        atomic_service_skzt_string_int_map_var["key_" + std::to_string(i)] = i+100;
    }
    atomic_service_skzt_Request_st.string_int_map = atomic_service_skzt_string_int_map_var;
    
    atomic_service_mbsb_Request_st atomic_service_mbsb_Request_st;
    atomic_service_mbsb_Reply_st atomic_service_mbsb_Reply_t;

    atomic_service_mbsb_Request_st.name ="atomic_service_mbsb";
    atomic_service_mbsb_Request_st.integer_field = 123;
    atomic_service_mbsb_Request_st.double_field = 123.123;
    atomic_service_mbsb_Request_st.float_field = 12.12;
    std::vector<int> atomic_service_mbsb_int_array_var;
    for(int i=0;i<20;i++) {
        atomic_service_mbsb_int_array_var.push_back(11);
    }
    atomic_service_mbsb_Request_st.int_array = atomic_service_mbsb_int_array_var;
    std::map<std::string, int32_t> atomic_service_mbsb_string_int_map_var;
    for(int i = 0; i < 10; i++) {
        atomic_service_mbsb_string_int_map_var["key_" + std::to_string(i)] = i+100;
    }
    atomic_service_mbsb_Request_st.string_int_map = atomic_service_mbsb_string_int_map_var;
    
    atomic_service_sj_Request_st atomic_service_sj_Request_st;
    atomic_service_sj_Reply_st atomic_service_sj_Reply_t;

    atomic_service_sj_Request_st.name ="atomic_service_sj";
    atomic_service_sj_Request_st.integer_field = 123;
    atomic_service_sj_Request_st.double_field = 123.123;
    atomic_service_sj_Request_st.float_field = 12.12;
    std::vector<int> atomic_service_sj_int_array_var;
    for(int i=0;i<20;i++) {
        atomic_service_sj_int_array_var.push_back(11);
    }
    atomic_service_sj_Request_st.int_array = atomic_service_sj_int_array_var;
    std::map<std::string, int32_t> atomic_service_sj_string_int_map_var;
    for(int i = 0; i < 10; i++) {
        atomic_service_sj_string_int_map_var["key_" + std::to_string(i)] = i+100;
    }
    atomic_service_sj_Request_st.string_int_map = atomic_service_sj_string_int_map_var;
    
    atomic_service_st_Request_st atomic_service_st_Request_st;
    atomic_service_st_Reply_st atomic_service_st_Reply_t;

    atomic_service_st_Request_st.name ="atomic_service_st";
    atomic_service_st_Request_st.integer_field = 123;
    atomic_service_st_Request_st.double_field = 123.123;
    atomic_service_st_Request_st.float_field = 12.12;
    std::vector<int> atomic_service_st_int_array_var;
    for(int i=0;i<20;i++) {
        atomic_service_st_int_array_var.push_back(11);
    }
    atomic_service_st_Request_st.int_array = atomic_service_st_int_array_var;
    std::map<std::string, int32_t> atomic_service_st_string_int_map_var;
    for(int i = 0; i < 10; i++) {
        atomic_service_st_string_int_map_var["key_" + std::to_string(i)] = i+100;
    }
    atomic_service_st_Request_st.string_int_map = atomic_service_st_string_int_map_var;
    
    
    
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
    
    std::cout << "<<<<<<<<<<<<<<<<<< Call the RPC << atomic_service_skzt>> and wait for response >>>>>>>>>>>>>>>>>>>>>" << std::endl;
    atomic_service_skzt_Reply_st atomic_service_skzt_rpc_reply = atomic_service_skzt.UnitaryStream(atomic_service_skzt_Request_st);
    std::cout << "Greeter received: " << atomic_service_skzt_rpc_reply.message << std::endl;
    std::cout << "Greeter received: " << atomic_service_skzt_rpc_reply.integer_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_skzt_rpc_reply.double_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_skzt_rpc_reply.float_reply<< std::endl;
    for(int i = 0; i < atomic_service_skzt_rpc_reply.int_array_reply.size(); i++){
        std::cout << "atomic_service_skzt received: " << atomic_service_skzt_rpc_reply.int_array_reply[i] << std::endl;
    }
    for (const auto& pair : atomic_service_skzt_rpc_reply.string_int_map_reply) {
        std::cout<< "atomic_service_skzt map data:" << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }
    
    std::cout << "<<<<<<<<<<<<<<<<<< Call the RPC << atomic_service_mbsb>> and wait for response >>>>>>>>>>>>>>>>>>>>>" << std::endl;
    atomic_service_mbsb_Reply_st atomic_service_mbsb_rpc_reply = atomic_service_mbsb.UnitaryStream(atomic_service_mbsb_Request_st);
    std::cout << "Greeter received: " << atomic_service_mbsb_rpc_reply.message << std::endl;
    std::cout << "Greeter received: " << atomic_service_mbsb_rpc_reply.integer_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_mbsb_rpc_reply.double_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_mbsb_rpc_reply.float_reply<< std::endl;
    for(int i = 0; i < atomic_service_mbsb_rpc_reply.int_array_reply.size(); i++){
        std::cout << "atomic_service_mbsb received: " << atomic_service_mbsb_rpc_reply.int_array_reply[i] << std::endl;
    }
    for (const auto& pair : atomic_service_mbsb_rpc_reply.string_int_map_reply) {
        std::cout<< "atomic_service_mbsb map data:" << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }
    
    std::cout << "<<<<<<<<<<<<<<<<<< Call the RPC << atomic_service_sj>> and wait for response >>>>>>>>>>>>>>>>>>>>>" << std::endl;
    atomic_service_sj_Reply_st atomic_service_sj_rpc_reply = atomic_service_sj.UnitaryStream(atomic_service_sj_Request_st);
    std::cout << "Greeter received: " << atomic_service_sj_rpc_reply.message << std::endl;
    std::cout << "Greeter received: " << atomic_service_sj_rpc_reply.integer_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_sj_rpc_reply.double_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_sj_rpc_reply.float_reply<< std::endl;
    for(int i = 0; i < atomic_service_sj_rpc_reply.int_array_reply.size(); i++){
        std::cout << "atomic_service_sj received: " << atomic_service_sj_rpc_reply.int_array_reply[i] << std::endl;
    }
    for (const auto& pair : atomic_service_sj_rpc_reply.string_int_map_reply) {
        std::cout<< "atomic_service_sj map data:" << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }
    
    std::cout << "<<<<<<<<<<<<<<<<<< Call the RPC << atomic_service_st>> and wait for response >>>>>>>>>>>>>>>>>>>>>" << std::endl;
    atomic_service_st_Reply_st atomic_service_st_rpc_reply = atomic_service_st.UnitaryStream(atomic_service_st_Request_st);
    std::cout << "Greeter received: " << atomic_service_st_rpc_reply.message << std::endl;
    std::cout << "Greeter received: " << atomic_service_st_rpc_reply.integer_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_st_rpc_reply.double_reply << std::endl;
    std::cout << "Greeter received: " << atomic_service_st_rpc_reply.float_reply<< std::endl;
    for(int i = 0; i < atomic_service_st_rpc_reply.int_array_reply.size(); i++){
        std::cout << "atomic_service_st received: " << atomic_service_st_rpc_reply.int_array_reply[i] << std::endl;
    }
    for (const auto& pair : atomic_service_st_rpc_reply.string_int_map_reply) {
        std::cout<< "atomic_service_st map data:" << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }
    

#if 0
    // Call the RPC and wait for SayHello_reply response
    std::cout << "<<<<<<<<<<<<<<<<<< Call the RPC and wait for SayHello_reply response >>>>>>>>>>>>>>>>>>>>>" << std::endl;
    helloworld::HelloReply SayHello_reply = greeter.SayHello(user, int_field, double_field, float_field, int_array, string_int_map);
    std::cout << "Greeter received: " << SayHello_reply.message() << std::endl;
    std::cout << "Greeter received: " << SayHello_reply.integer_reply() << std::endl;
    std::cout << "Greeter received: " << SayHello_reply.double_reply() << std::endl;
    std::cout << "Greeter received: " << SayHello_reply.float_reply() << std::endl;
    for(int i = 0; i < SayHello_reply.int_array_reply_size(); i++){
        std::cout << "Greeter received: " << SayHello_reply.int_array_reply(i) << std::endl;
    }
    for (const auto& pair : SayHello_reply.string_int_map_reply()) {
        std::cout << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }
    // Call the RPC and wait for ServerStream_reply response
    std::cout << "<<<<<<<<<<<<<<<<< Call the RPC and wait for ServerStream_reply response >>>>>>>>>>>>>>>>>>" << std::endl;
    std::vector<helloworld::HelloReply> ServerStream_reply = greeter.ServerStream(user, int_field, double_field, float_field, int_array, string_int_map);
    for (const auto& reply : ServerStream_reply) {
        std::cout << "Greeter received: " << reply.message() << std::endl;
        std::cout << "Greeter received: " << reply.integer_reply() << std::endl;
        std::cout << "Greeter received: " << reply.double_reply() << std::endl;
        std::cout << "Greeter received: " << reply.float_reply() << std::endl;
        for(int i = 0; i < reply.int_array_reply_size(); i++){
            std::cout << "Greeter received: " << reply.int_array_reply(i) << std::endl;
        }
        for (const auto& pair : reply.string_int_map_reply()) {
            std::cout << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
        }
    }

    // Call the RPC and wait for ClientStream_reply response
    std::cout << "<<<<<<<<<<<<<<<<< Call the RPC and wait for ClientStream_reply response >>>>>>>>>>>>>>>>>>" << std::endl;
    helloworld::HelloReply ClientStream_reply = greeter.ClientStream(user, int_field, double_field, float_field, int_array, string_int_map);
    std::cout << "Greeter received: " << SayHello_reply.message() << std::endl;
    std::cout << "Greeter received: " << SayHello_reply.integer_reply() << std::endl;
    std::cout << "Greeter received: " << SayHello_reply.double_reply() << std::endl;
    std::cout << "Greeter received: " << SayHello_reply.float_reply() << std::endl;
    for(int i = 0; i < SayHello_reply.int_array_reply_size(); i++){
        std::cout << "Greeter received: " << SayHello_reply.int_array_reply(i) << std::endl;
    }
    for (const auto& pair : SayHello_reply.string_int_map_reply()) {
        std::cout << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
    }

    // Call the RPC and wait for Chat_reply response
    std::cout << "<<<<<<<<<<<<<<<<< Call the RPC and wait for Chat_reply response >>>>>>>>>>>>>>>>>>>>>>" << std::endl;
    std::vector<helloworld::HelloReply> Chat_reply = greeter.Chat(user, int_field, double_field, float_field, int_array, string_int_map);
    for (const auto& reply : Chat_reply) {
        std::cout << "Greeter received: " << reply.message() << std::endl;
        std::cout << "Greeter received: " << reply.integer_reply() << std::endl;
        std::cout << "Greeter received: " << reply.double_reply() << std::endl;
        std::cout << "Greeter received: " << reply.float_reply() << std::endl;
        for(int i = 0; i < reply.int_array_reply_size(); i++){
            std::cout << "Greeter received: " << reply.int_array_reply(i) << std::endl;
        }
        for (const auto& pair : reply.string_int_map_reply()) {
            std::cout << "Key: " << pair.first << ", Value: " << pair.second << std::endl;
        }
    }
#endif

    return 0;
}