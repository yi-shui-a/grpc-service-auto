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

#include <vector>
#include <map>

#include <grpcpp/grpcpp.h>

#include "../rpc_client_inc/atomic_service_mbsb_client.h"
#include "../rpc_client_inc/atomic_service_sf_client.h"

#include "../atom_service/atomic_service_mbsb/atomic_service_mbsb.h"
#include "../atom_service/atomic_service_sf/atomic_service_sf.h"

#include "dds/dds.h"
#include "../IDL_inc/example.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

#include <nlohmann/json.hpp>
using json = nlohmann::json;

typedef struct
{
    char ip[20];
    int port;
    char server_name[20];
    int role;
} QueryInfo;

// 定义包含 channel 和 IP 地址的结构体
typedef struct
{
    std::shared_ptr<grpc::Channel> channel;
    std::string ip;
} ChannelInfo;

// 统计数字位数
int getDigit(int number);
// 更新字符数
int updateNumber(int number);

void queryServiceInfo(char *serviceName[], int num[], int size, QueryInfo info[], const char *broadcastAddress, const int port);

FormalTest_test1 *receiveData();

void sendInfo()
{
}

int main(int argc, char **argv)
{
    //===============================================================================
    //                             init :初始化程序
    //===============================================================================
    // 创建ip和端口，此处为注册中心的的ip和端口号
    char *broadcastAddress = "255.255.255.255"; // Default broadcast addressIP "192.168.0.255"
    int broadcastPort = 8888;                   // Default broadcast port
    // 定义服务名，此处为代码生成
    char *serviceName[2] = {"atomic_service_mbsb", "atomic_service_sf"};
    // 定义服务数量
    int num[2];
    for (int i = 0; i < 2; i++)
    {
        num[i] = 1; // 假设只有一个该服务
    }
    // 定义返回值列表，依次查询服务信息
    QueryInfo queryInfo[2];
    // 查询服务信息
    queryServiceInfo(serviceName, num, 2, queryInfo, broadcastAddress, broadcastPort);

    // 创建grpc channel
    // 创建一个 ChannelInfo 结构体的 vector
    std::vector<ChannelInfo> channel_list;
    for (int i = 0; i < 2; i++)
    {
        // 使用std::ostringstream来构建字符串
        std::ostringstream oss;
        oss << queryInfo[i].ip << ":" << queryInfo[i].port;
        // 将构建的字符串赋值给std::string对象
        std::string temp_str = oss.str();
        int unequal_num = 0;
        for (int size_v = 0; size_v < channel_list.size(); size_v++)
        {
            if (temp_str != channel_list[size_v].ip)
            {
                unequal_num++;
            }
        }
        if (unequal_num == channel_list.size())
        {
            auto channel = grpc::CreateChannel(temp_str, grpc::InsecureChannelCredentials());
            std::string ip = temp_str;
            ChannelInfo info = {channel, ip};
            channel_list.push_back(info);
        }
    }

    // 创建与服务器的通信通道
    atomic_service_mbsb_Service_Client atomic_service_mbsb(channel_list[0].channel);
    atomic_service_sf_Service_Client atomic_service_sf(channel_list[0].channel);
    for (int i = 0; i < channel_list.size(); i++)
    {
        if (channel_list[i].ip == std::string(queryInfo[0].ip) + ":" + std::to_string(queryInfo[0].port))
        {
            atomic_service_mbsb_Service_Client atomic_service_mbsb(channel_list[i].channel);
        }
        if (channel_list[i].ip == std::string(queryInfo[1].ip) + ":" + std::to_string(queryInfo[1].port))
        {
            atomic_service_sf_Service_Client atomic_service_sf(channel_list[i].channel);
        }
    }

    //===============================================================================
    //                             receiveData :接收输入数据
    //===============================================================================

    FormalTest_test1 *data = receiveData();

    //===============================================================================
    //                             sendData :向前端发送信号
    //===============================================================================

    sendInfo();

    //===============================================================================
    //                             setParam :设置结构体变量值
    //===============================================================================

    // 声明变量并赋值
    atomic_service_mbsb_task_A_Request_st request_a;
    request_a.number1 = data->number1;
    request_a.number2 = data->number2;
    atomic_service_mbsb_task_B_Request_st request_b;
    request_b.number1 = data->number1;
    request_b.number2 = data->number2;

    // 声明变量
    atomic_service_sf_task_C_Request_st request_c;
    atomic_service_sf_task_D_Request_st request_d;

    //===============================================================================
    //                                 调用服务流程
    //===============================================================================

    // 调用第一层服务
    atomic_service_mbsb_task_A_Reply_st reply_a = atomic_service_mbsb.atomic_service_fun_task_A(request_a);
    atomic_service_mbsb_task_B_Reply_st reply_b = atomic_service_mbsb.atomic_service_fun_task_B(request_b);

    // 使用上一个服务的运行结果，构造下一个服务的入参
    request_d.int_array.push_back(reply_a.sum_result);
    request_d.int_array.push_back(reply_b.sub_result);
    // 调用第二层服务
    atomic_service_sf_task_D_Reply_st reply_d = atomic_service_sf.atomic_service_fun_task_D(request_d);

    // 调用第三层服务
    atomic_service_sf_task_C_Reply_st reply_c = atomic_service_sf.atomic_service_fun_task_C(request_c);

    std::cout << "Greeter received: " << reply_a.sum_result << "     return_type: " << reply_a.return_type << std::endl;
    std::cout << "Greeter received: " << reply_b.sub_result << "     return_type: " << reply_b.return_type << std::endl;
    std::cout << "Greeter received: " << reply_c.result << "     return_type: " << reply_c.return_type << std::endl;
    // std::cout << "Greeter received: " << reply_d.string_int_map_reply << "     return_type: " << reply_d.return_type << std::endl;

    return 0;
}

void queryServiceInfo(char *serviceName[], int num[], int size, QueryInfo info[], const char *broadcastAddress, const int port)
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
    sockertaddr.sin_addr.s_addr = inet_addr(broadcastAddress);
    sockertaddr.sin_port = htons(port);

    // 构造查询请求消息
    for (int i = 0; i < size; i++)
    {
        json query_json;
        json header;
        header["protocol_identifier"] = 22;
        header["send_time"] = time(NULL);
        header["message_length"] = 1;
        header["message_serial_number"] = 1;
        header["check_bit"] = 4;
        header["type"] = 5;
        query_json["header"] = header;
        query_json["service_name"] = serviceName[i];
        query_json["service_num"] = num[i];

        std::string query_str = query_json.dump();
        header["message_length"] = updateNumber(query_str.size());
        query_str = query_json.dump();

        // 发送注册报文到广播地址
        if (sendto(sock, query_str.c_str(), query_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0)
        {
            close(sock);
            exit(EXIT_FAILURE);
        }
        // 接收查询结果
        memset(buffer, 0, sizeof(buffer));
        int recv_len = recvfrom(sock, buffer, sizeof(buffer), 0, (struct sockaddr *)&register_addr, &register_addr_len);
        if (recv_len < 0)
        {
            perror("recvfrom failed");
            continue;
        }
        // 解析接收到的json消息
        json response_json = json::parse(buffer);
        if (response_json["header"]["type"] == 6)
        {
            if (response_json.at("service_num").get<int>() == 0)
            {
                printf("error: invalid service");
                exit(EXIT_FAILURE);
            }
            strcpy(info[i].ip, response_json["instance_list"][0]["address"].get<std::string>().c_str());
            info[i].port = response_json.at("instance_list").at(0).at("port").get<int>();
            strcpy(info[i].server_name, response_json.at("instance_list").at(0).at("server_name").get<std::string>().c_str());
            info[i].role = response_json.at("instance_list").at(0).at("role").get<int>();
        }
    }

    // 关闭socket
    close(sock);
}

// 统计数字位数
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

// 更新字符数
int updateNumber(int number)
{
    int i = number;
    i = i + getDigit(i);
    i -= 1;
    return i;
}

FormalTest_test1 *receiveData()
{
    // 定义dds数据类型
    dds_entity_t participant;
    dds_entity_t topic;
    dds_entity_t reader;
    dds_return_t rc;
    FormalTest_test1 *msg;
    void *samples[1];
    dds_sample_info_t infos[1];

    // 创建参与者
    participant = dds_create_participant(DDS_DOMAIN_DEFAULT, NULL, NULL);
    if (participant < 0)
        DDS_FATAL("dds_create_participant: %s\n", dds_strretcode(-participant));

    // 创建主题
    topic = dds_create_topic(
        participant, &FormalTest_test1_desc, "FormalTest_test1", NULL, NULL);
    if (topic < 0)
        DDS_FATAL("dds_create_topic: %s\n", dds_strretcode(-topic));

    // 创建读取者
    reader = dds_create_reader(participant, topic, NULL, NULL);
    if (reader < 0)
        DDS_FATAL("dds_create_reader: %s\n", dds_strretcode(-reader));

    // 为sample分配空间
    for (int i = 0; i < 1; i++)
    {
        samples[i] = FormalTest_test1__alloc();
    }

    printf("=== [Subscriber] Waiting for a message ...\n");
    fflush(stdout);

    // 读取消息
    while (true)
    {
        // 从reader中读取，存储在 samples 数组中
        // infos: 存储与数据样本相关的元信息（如样本的状态、时间戳等）长度与sample相同
        // 最后两个参数，分别是samples数组和infos数组的长度
        rc = dds_take(reader, samples, infos, 1, 1);
        if (rc < 0)
            DDS_FATAL("dds_take: %s\n", dds_strretcode(-rc));
            
        // infos[0].valid_data: 判断infos[0]中的数据是否有效
        if ((rc > 0) && (infos[0].valid_data))
        {
            // 显式类型转换
            msg = (FormalTest_test1 *)samples[0];
            printf("=== [Subscriber] Received: ");
            printf("Message (number1: %d, number2: %d, doubleNumber1: %f, doubleNumber2: %f, message1: %s, message2: %s)\n",
                   msg->number1, msg->number2, msg->doubleNumber1, msg->doubleNumber2, msg->message1, msg->message2);
            // 强制刷新标准输出缓冲区，确保消息立即显示在控制台上
            fflush(stdout);

            // 如果需要返回消息，可以在这里复制数据
            FormalTest_test1 *ret_msg = (FormalTest_test1 *)malloc(sizeof(FormalTest_test1));
            if (ret_msg == NULL)
            {
                DDS_FATAL("Failed to allocate memory for return message\n");
                // 删除参与者
                dds_delete(participant);
                return NULL;
            }

            /**
             * 复制数据
             */
            // 复制基本数据类型
            ret_msg->number1 = msg->number1;
            ret_msg->number2 = msg->number2;
            ret_msg->doubleNumber1 = msg->doubleNumber1;
            ret_msg->doubleNumber2 = msg->doubleNumber2;

            // 复制字符串 message1
            ret_msg->message1 = strdup(msg->message1); // 使用 strdup 分配并复制字符串
            if (ret_msg->message1 == NULL)
            {
                DDS_FATAL("Failed to allocate memory for message1\n");
                free(ret_msg); // 释放已分配的内存
                dds_delete(participant);
                return NULL;
            }

            // 复制字符串 message2
            ret_msg->message2 = strdup(msg->message2); // 使用 strdup 分配并复制字符串
            if (ret_msg->message2 == NULL)
            {
                DDS_FATAL("Failed to allocate memory for message2\n");
                free(ret_msg->message1); // 释放已分配的 message1
                free(ret_msg);           // 释放已分配的内存
                dds_delete(participant);
                return NULL;
            }

            // 删除 DDS 资源
            rc = dds_delete(participant);
            if (rc != DDS_RETCODE_OK)
                DDS_FATAL("dds_delete: %s\n", dds_strretcode(-rc));

            // 返回接收到的消息
            return ret_msg;
        }
        // 让线程休眠 1000 ms，避免循环占用过多CPU资源。
        dds_sleepfor(DDS_MSECS(1000));
    }

    // 删除参与者
    rc = dds_delete(participant);
    if (rc != DDS_RETCODE_OK)
        DDS_FATAL("dds_delete: %s\n", dds_strretcode(-rc));

    return NULL;
}