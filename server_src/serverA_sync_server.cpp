#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <string>
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include <netdb.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <ctime>

#include <nlohmann/json.hpp>

#include "../rpc_server_inc/atomic_service_mbsb_impl.h"

#include "../rpc_server_inc/atomic_service_sf_impl.h"

using json = nlohmann::json;


class atomic_service_mbsb_Service_ServerImpl ;

class atomic_service_sf_Service_ServerImpl ;


//统计数字位数
int getDigit(int number)
{
    int count = 0;
    while (number != 0)
    {
        number /= 10;
        count++;
    }
    return count;
}

//更新字符数
int updateNumber(int number)
{
    int i = number;
    i = i + getDigit(i);
    i -= 1;
    return i;
}


void monitorComm(const std::string& broadcastAddress, const int port){
    int sock;
    struct sockaddr_in sockertaddr;  
    // 创建UDP socket  
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {  
        perror("socket creation failed");  
        exit(EXIT_FAILURE);  
    }  
  
    // 设置socket选项以允许广播  
    int opt = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &opt, sizeof(opt)) < 0) {  
        perror("setsockopt(SO_BROADCAST) failed");  
        exit(EXIT_FAILURE);  
    }  
  
    // 初始化广播地址结构  
    memset(&sockertaddr, 0, sizeof(sockertaddr));  
    sockertaddr.sin_family = AF_INET;  
    sockertaddr.sin_addr.s_addr = inet_addr(broadcastAddress.c_str());  
    sockertaddr.sin_port = htons(port);  

    // 构造注册信息
    json registry_json;
    json header;
    header["protocol_identifier"] =22;
    header["send_time"] = time(NULL);
    header["message_length"] = 1;
    header["message_serial_number"] = 1;
    header["check_bit"] = 4;
    header["type"] = 1;
    registry_json["header"] = header;
    registry_json["server_name"] = "serverA";
    registry_json["address"] = "localhost";
    registry_json["port"] = 50051;

    json registry_services_list = json::array();
    
    
    registry_services_list.push_back({ {"service_name","atomic_service_mbsb"},{"role", 1} });
    
    registry_services_list.push_back({ {"service_name","atomic_service_sf"},{"role", 1} });
    
    registry_json["services_list"] = registry_services_list;
    std::string registry_str = registry_json.dump();
    header["message_length"] = updateNumber(registry_str.size());
    registry_str = registry_json.dump();
    // 发送注册报文到广播地址
    if (sendto(sock, registry_str.c_str(), registry_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0) {
        close(sock);
        exit(EXIT_FAILURE);
    }

    // 构造元数据信息
    json metadata_registry_json;
    header["protocol_identifier"] =22;
    header["send_time"] = time(NULL);
    header["message_length"] = 1;
    header["message_serial_number"] = 1;
    header["check_bit"] = 4;
    header["type"] = 3;
    metadata_registry_json["header"] = header;
    metadata_registry_json["server_name"] = "serverA";
    metadata_registry_json["address"] = "localhost";
    metadata_registry_json["port"] = 50051;
    json metadata_registry_services_list = json::array();
    
    metadata_registry_services_list.push_back({ {"metadata",{ { "version", "V1.0.0" },{"decription",""},{"developer","Spiderman"},{"build_time","2024-09-21T09-21-21"} } },{"service_name", "atomic_service_mbsb" },{"card","atlas"},{"os","openeuler"} });
    
    metadata_registry_services_list.push_back({ {"metadata",{ { "version", "V1.0.2" },{"decription",""},{"developer","yishui"},{"build_time","2024-09-30T09-21-21"} } },{"service_name", "atomic_service_sf" },{"card","atlas"},{"os","openeuler"} });
    
    metadata_registry_json["services_list"] = metadata_registry_services_list;
    std::string metadata_registry_str = metadata_registry_json.dump();
    header["message_length"] = updateNumber(metadata_registry_str.size());
    metadata_registry_str = metadata_registry_json.dump();
    // 发送注册报文到广播地址
    if (sendto(sock, metadata_registry_str.c_str(), metadata_registry_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0) {
        close(sock);
        exit(EXIT_FAILURE);
    }


    //构造心跳信息
    json heartbeat_json;
    json heartbeat_services_list;
    while (1) { 
        // 无限循环，每30秒发送一次  
        header["protocol_identifier"] =22;
        header["send_time"] = time(NULL);
        header["message_length"] = 1;
        header["message_serial_number"] = 1;
        header["check_bit"] = 4;
        header["type"] = 7;
        heartbeat_json["header"] = header;
        heartbeat_json["server_name"] = "serverA";
        heartbeat_json["address"] = "localhost";
        heartbeat_json["port"] = 50051;
        heartbeat_services_list = json::array();
        
        heartbeat_services_list.push_back({ {"service_name","atomic_service_mbsb"},{"role", 1} });
        
        heartbeat_services_list.push_back({ {"service_name","atomic_service_sf"},{"role", 1} });
        
        registry_json["services_list"] = metadata_registry_services_list;
        std::string heartbeat_str = heartbeat_json.dump();
        header["message_length"] = updateNumber(heartbeat_str.size());
        heartbeat_str = heartbeat_json.dump();
        // 发送注册报文到广播地址
        if (sendto(sock, heartbeat_str.c_str(), heartbeat_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0) {
            close(sock);
            exit(EXIT_FAILURE);
        }

        sleep(30);  
    }  

    // 关闭socket
    close(sock);  
}


void RunServer(const std::string& ip, const std::string& port) {
    std::string server_address(ip+":"+port);
    ::grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address, ::grpc::InsecureServerCredentials());
    // TODO add service
    
    atomic_service_mbsb_Service_ServerImpl atomic_service_mbsb_instance;
    builder.RegisterService(&atomic_service_mbsb_instance);
    
    atomic_service_sf_Service_ServerImpl atomic_service_sf_instance;
    builder.RegisterService(&atomic_service_sf_instance);
    
    std::unique_ptr<::grpc::Server> server(builder.BuildAndStart());
    std::cout << ">>>> Server listening on " << server_address << std::endl;
    server->Wait();
}

int main(int argc, char** argv) {

    std::string ip = "localhost";
    std::string port = "50051";
    std::string broadcastAddress = "255.255.255.255";  // Default broadcast addressIP "192.168.0.255"
    std::string broadcastPort = "8888";     // Default broadcast port

    std::cout << ">>>>[INFO] Server IP: " << ip << std::endl;
    std::cout << ">>>>[INFO] Server Port: " << port << std::endl;
    std::cout << ">>>>[INFO] Broadcast Address: " << broadcastAddress << std::endl;
    std::cout << ">>>>[INFO] Broadcast Port: " << broadcastPort << std::endl;

    std::thread senderThread(monitorComm, broadcastAddress, std::stoi(broadcastPort));
    // TODO: Add other threads here
    
    RunServer(ip,port);
    
    senderThread.join();

    return 0;
}