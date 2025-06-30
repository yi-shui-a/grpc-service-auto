#include <iostream>
#include <fstream>
#include <memory>
#include <string>
#include <chrono>
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include <netdb.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <ctime>
#include <memory>

#include <vector>
#include <map>

#include <grpcpp/grpcpp.h>

#include "Header.h"

#include "../../atomic_service/atomic_test_fusion/sync_client_impl/atomic_test_fusion_sync_client_impl.cpp"

#include "dds/dds.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

#include <nlohmann/json.hpp>
using json = nlohmann::json;

typedef struct
{
    std::string ip;
    int port;
    std::string server_name;
    int role;
} QueryInfo;

// 定义包含 channel 和 IP 地址的结构体
typedef struct
{
    std::shared_ptr<grpc::Channel> channel;
    std::string ip;
} ChannelInfo;

void queryServiceInfo(std::string serviceName[], int num[], int size, QueryInfo info[], const std::string broadcastAddress, const int port);

std::string formatResponse(std::string contentStr, int32_t type, int32_t identifier);

long long getCurrentTimeMillis();
uint64_t getSystemMicroseconds();

int main(int argc, char **argv)
{
    //===============================================================================
    //                             init :初始化程序
    //===============================================================================
    std::cout << "INFO: client start" << std::endl;

    // 获取运行次数
    int count = 1000;
    if (argc == 2)
    {
        count = std::atoi(argv[1]);
    }

    // 创建ip和端口，此处为注册中心的的ip和端口号
    std::string broadcastAddress = "255.255.255.255"; // Default broadcast addressIP "192.168.0.255"
    int broadcastPort = 10450;                        // Default broadcast port
    // 定义服务名，此处为代码生成
    std::string serviceName[1] = {

        "atomic_test_fusion",

    };
    // 定义服务数量
    int num[1];
    for (int i = 0; i < 1; i++)
    {
        num[i] = 1; // 假设只有一个该服务
    }
    // 定义返回值列表，依次查询服务信息
    QueryInfo queryInfo[1];
    // 查询服务信息
    queryServiceInfo(serviceName, num, 1, queryInfo, broadcastAddress, broadcastPort);

    // 创建grpc channel
    // 创建一个 ChannelInfo 结构体的 vector
    std::vector<ChannelInfo> channel_list;
    for (int i = 0; i < 1; i++)
    {
        std::string temp_str = queryInfo[i].ip + ":" + std::to_string(queryInfo[i].port);
        int unequal_num = 0;
        // 遍历 channel_list 中的每个元素，比较 temp_str 与 channel_list 中元素的 ip 字段。如果不相等，则 unequal_num 加 1。
        for (int size_v = 0; size_v < channel_list.size(); size_v++)
        {
            if (temp_str != channel_list[size_v].ip)
            {
                unequal_num++;
            }
        }
        // 如果 unequal_num 等于 channel_list 的大小，说明 temp_str 对应的地址在 channel_list 中不存在.
        // 此时使用 grpc::CreateChannel 函数创建一个新的 gRPC 通道，并使用不安全的通道凭证
        if (unequal_num == channel_list.size())
        {
            auto channel = grpc::CreateChannel(temp_str, grpc::InsecureChannelCredentials());
            std::string ip = temp_str;
            ChannelInfo info = {channel, ip};
            channel_list.push_back(info);
        }
    }

    // 声明对象
    atomic_test_fusion_Service_Client *atomic_test_fusion = nullptr;

    for (int i = 0; i < channel_list.size(); i++)
    {
        if (channel_list[i].ip == queryInfo[0].ip + ":" + std::to_string(queryInfo[0].port))
        {
            atomic_test_fusion = new atomic_test_fusion_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[0].ip << "   " << queryInfo[0].port << std::endl;
        }
    }

    std::cout << "INFO: grpc connect finish." << std::endl;

    //===============================================================================
    //                             receiveData :接收输入数据
    //===============================================================================
    // 声明变量并赋值
    fusion_input request;

    // 为开始的服务赋值
    request.x = 1000;
    request.y = 1000;
    request.z = 1000;
    request.size = 5;
    for (int i = 1; i <= count; i++)
    {

        //===============================================================================
        //                                 调用服务流程
        //===============================================================================
        // 运行服务
        std::cout << "=====run_number:" << i << std::endl;
        std::cout << "=====start_time:" << getSystemMicroseconds() << std::endl;
        fusion_output reply = atomic_test_fusion->getFusionData(request);

        std::cout << "reply: x = " << reply.x << std::endl;
        std::cout << "reply: y = " << reply.y << std::endl;
        std::cout << "reply: z = " << reply.z << std::endl;
        std::cout << "reply: size = " << reply.size << std::endl;
        std::cout << "reply: return_type = " << reply.return_type << std::endl;
        std::cout << "=====end_time:" << getSystemMicroseconds() << std::endl;
    }
}

void queryServiceInfo(std::string serviceName[], int num[], int size, QueryInfo info[], const std::string broadcastAddress, const int port)
{
    /*
    查询服务信息
    */
    // 声明变量
    int sock;
    struct sockaddr_in sockertaddr, register_addr;
    socklen_t register_addr_len = sizeof(register_addr);
    char buffer[4 * 1024];
    // 创建UDP socket
    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
    {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    // 设置socket选项以允许广播
    int opt = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &opt, sizeof(opt)) < 0)
    {
        perror("setsockopt(SO_BROADCAST) failed");
        exit(EXIT_FAILURE);
    }

    // 初始化广播地址结构
    memset(&sockertaddr, 0, sizeof(sockertaddr));
    sockertaddr.sin_family = AF_INET;
    sockertaddr.sin_addr.s_addr = inet_addr(broadcastAddress.c_str());
    sockertaddr.sin_port = htons(port);

    // 构造查询请求消息
    for (int i = 0; i < size; i++)
    {
        json query_json;
        query_json["service_name"] = serviceName[i];
        query_json["service_num"] = num[i];

        std::string query_str = query_json.dump(4);
        query_str = formatResponse(query_str, 5, 1);

        // 发送注册报文到广播地址
        if (sendto(sock, query_str.c_str(), query_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0)
        {
            close(sock);
            exit(EXIT_FAILURE);
        }
        // 接收查询结果
        memset(buffer, 0, sizeof(buffer));
        int recv_len = recvfrom(sock, buffer, sizeof(buffer) - 1, 0, (struct sockaddr *)&register_addr, &register_addr_len);
        if (recv_len < 0)
        {
            perror("recvfrom failed");
            continue;
        }
        // 确保缓冲区以null结尾
        buffer[recv_len] = '\0';

        // 将接收到的数据分为两部分
        const int prefixLength = 28; // 前28个字节
        if (recv_len < prefixLength)
        {
            close(sock);
            throw std::runtime_error("接收到的数据不足28字节");
        }
        // 返回值类型转换
        std::string responseMessage(buffer, recv_len);
        std::string responseHeaderStr = responseMessage.substr(0, 28);
        std::string responseContentStr = responseMessage.substr(28);
        Header responseHeader = Header::deserialize(responseHeaderStr);
        try
        {
            json response_json = json::parse(responseContentStr)["data"];
            if (responseHeader.type == 6)
            {
                if (response_json["service_num"] == 0)
                {
                    printf("error: invalid service");
                }
                info[i].ip = response_json.at("instance_list").at(0).at("address").get<std::string>();
                info[i].port = response_json.at("instance_list").at(0).at("port").get<int>();
                info[i].server_name = response_json.at("instance_list").at(0).at("server_name").get<std::string>();
                info[i].role = response_json.at("instance_list").at(0).at("role").get<int>();
            }
        }
        catch (const std::exception &e)
        {
            std::cerr << "Exception: " << e.what() << std::endl;
            std::cerr << "Invalid JSON data received." << std::endl;
            close(sock);
        }
    }

    // 关闭socket
    close(sock);
}

std::string formatResponse(std::string contentStr, int32_t type, int32_t identifier)
{
    Header header = Header();
    header.identifier = identifier;
    header.sendTime = getCurrentTimeMillis();
    header.messageLength = contentStr.length();
    header.serialNumber = 1;
    header.checkBit = 1;
    header.type = type;
    std::string headerStr = Header::serialize(header);

    return headerStr + contentStr;
}

// 获取当前毫秒级时间戳
long long getCurrentTimeMillis()
{
    auto now = std::chrono::system_clock::now();
    auto duration = now.time_since_epoch();
    auto res = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
    return res;
}


// 获取当前微秒级时间戳（系统时钟）
uint64_t getSystemMicroseconds() {
    // 获取当前时间点（显式声明类型）
    std::chrono::system_clock::time_point now = std::chrono::system_clock::now();
    
    // 转换为自纪元起的时间间隔（显式声明类型）
    std::chrono::system_clock::duration since_epoch = now.time_since_epoch();
    
    // 转换为微秒（显式声明类型）
    std::chrono::microseconds microseconds = 
        std::chrono::duration_cast<std::chrono::microseconds>(since_epoch);
    
    return microseconds.count();
}