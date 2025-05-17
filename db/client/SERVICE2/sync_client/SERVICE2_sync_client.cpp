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


#include "../../../atomic_service/atomic_service_mbsb/sync_client_impl/atomic_service_mbsb_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_service_sf/sync_client_impl/atomic_service_sf_sync_client_impl.cpp"


#include "dds/dds.h"

#include "../idl/StartRequest/StartRequest.h"

#include "../idl/EndResponse/EndResponse.h"


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


StartRequest_atomic_service_mbsb_task_A_Request_st *receiveData_7251674(dds_entity_t participant, dds_entity_t topic, dds_entity_t reader);



EndResponse_atomic_service_sf_task_E_Reply_st end_0292837;
void sendData_0292837(dds_entity_t participant, dds_entity_t topic, dds_entity_t writer, EndResponse_atomic_service_sf_task_E_Reply_st data);


int main(int argc, char **argv)
{
    //===============================================================================
    //                             init :初始化程序
    //===============================================================================
    std::cout << "INFO: client start" << std::endl;

    // 创建ip和端口，此处为注册中心的的ip和端口号
    std::string broadcastAddress = "255.255.255.255"; // Default broadcast addressIP "192.168.0.255"
    int broadcastPort = 10450;                        // Default broadcast port
    // 定义服务名，此处为代码生成
    std::string serviceName[2] = {
        
        "atomic_service_mbsb",
        
        "atomic_service_sf"
    };
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
    
    atomic_service_mbsb_Service_Client *atomic_service_mbsb = nullptr;
    
    atomic_service_sf_Service_Client *atomic_service_sf = nullptr;
    

    for (int i = 0; i < channel_list.size(); i++)
    {
        
        if (channel_list[i].ip == queryInfo[0].ip + ":" + std::to_string(queryInfo[0].port))
        {
            atomic_service_mbsb = new atomic_service_mbsb_Service_Client(channel_list[i].channel);
        }
        
        if (channel_list[i].ip == queryInfo[0].ip + ":" + std::to_string(queryInfo[0].port))
        {
            atomic_service_sf = new atomic_service_sf_Service_Client(channel_list[i].channel);
        }
        
    }

    std::cout << "INFO: grpc connect finish." << std::endl;

    //创建DDS相关函数
    // 初始化 DDS 参与者实体
    dds_entity_t participant;  
    participant = dds_create_participant(0, NULL, NULL);
    if (participant < 0)
    {
        std::cerr << "ERROR: Failed to create participant: " << dds_strretcode(-participant) << std::endl;
        return EXIT_FAILURE;
    }
    // 创建Qos
    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10));
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);

    
    // 创建Topic
    dds_entity_t startA;
    startA = dds_create_topic(participant, &StartRequest_atomic_service_mbsb_task_A_Request_st_desc, "startA", NULL, NULL);
    if (startA < 0)
    {
        std::cerr << "ERROR: startA -- Failed to create topic: " << dds_strretcode(-startA) << std::endl;
        return 0;
    }
    // 创建subscriber
    dds_entity_t startA_subscriber;
    startA_subscriber = dds_create_subscriber(participant, NULL, NULL);
    if (startA_subscriber < 0) {
        std::cerr << "ERROR: Failed to create subscriber: " << dds_strretcode(-startA_subscriber) << std::endl;
        dds_delete(startA);
        dds_delete_qos(qos);
        dds_delete(participant);
        return EXIT_FAILURE;
    }
    // 创建读取器
    dds_entity_t startA_reader;
    startA_reader = dds_create_reader(startA_subscriber, startA, qos, NULL);
    if (startA_reader < 0)
    {
        std::cerr << "ERROR: startA -- Failed to create reader: " << dds_strretcode(-startA_reader) << std::endl;
        dds_delete(startA);
        dds_delete_qos(qos);
        return 0;
    }
    

    
    // 创建Topic
    dds_entity_t endA;
    endA = dds_create_topic(participant, &EndResponse_atomic_service_sf_task_E_Reply_st_desc, "endA", NULL, NULL);
    if (endA < 0)
    {
        std::cerr << "ERROR: endA -- Failed to create topic: " << dds_strretcode(-endA) << std::endl;
        return 0;
    }
    // 创建写入器
    dds_entity_t endA_writer;
    endA_writer = dds_create_writer(participant, endA, qos, NULL);
        if (endA_writer < 0)
        {
            std::cerr << "ERROR: Failed to create writer for " << endA << ": "
                      << dds_strretcode(-endA_writer) << std::endl;
            // 清理已创建的写入器
            dds_delete_qos(qos);
            dds_delete(participant);
            return EXIT_FAILURE;
        }
    
    // QoS配置不再需要，可以删除
    dds_delete_qos(qos);
    std::cout << "INFO: DDS initial finish." << std::endl;


    //===============================================================================
    //                             receiveData :接收输入数据
    //===============================================================================

while(1){
    // 接收输入数据
    
    StartRequest_atomic_service_mbsb_task_A_Request_st *start_7251674 = receiveData_7251674(participant, startA, startA_reader);
    
    

    std::cout << "INFO: start info received." << std::endl;

    //===============================================================================
    //                             setParam :设置结构体变量值
    //===============================================================================

    // 声明变量并赋值
    
    atomic_service_mbsb_task_A_Request_st request_6405196;
    
    atomic_service_sf_task_E_Request_st request_3473875;
    
    
    //为开始的服务赋值
    
    request_6405196.number1 = start_7251674->number1;
    
    request_6405196.number2 = start_7251674->number2;
    

    //===============================================================================
    //                                 调用服务流程
    //===============================================================================
    // 运行服务
    
    atomic_service_mbsb_task_A_Reply_st reply_6405196 = atomic_service_mbsb->atomic_service_fun_task_A(request_6405196);
    


    // 赋值
    
    request_3473875.sum_result = reply_6405196.sum_result;
    
    // 运行服务
    
    atomic_service_sf_task_E_Reply_st reply_3473875 = atomic_service_sf->atomic_service_fun_task_E(request_3473875);
    


    // 赋值
    
    std::cout << "SERVICE2 output: " << std::endl
    
            << reply_3473875.sum_result << std::endl
    
            << reply_3473875.return_type << std::endl;

    // 赋值
    
    end_0292837.sum_result = reply_3473875.sum_result;
    
    end_0292837.return_type = reply_3473875.return_type;
    
    
    sendData_0292837(participant, endA, endA_writer, end_0292837);
    
    std::cout << "INFO: program operation info finish." << std::endl;
}
    // 删除 DDS 参与者
    dds_return_t rc = dds_delete(participant);
    if (rc != DDS_RETCODE_OK)
        DDS_FATAL("dds_delete: %s\n", dds_strretcode(-rc));
    return 0;
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


StartRequest_atomic_service_mbsb_task_A_Request_st *receiveData_7251674(dds_entity_t participant, dds_entity_t topic, dds_entity_t reader)
{
    // 定义dds数据类型
    dds_return_t rc;
    StartRequest_atomic_service_mbsb_task_A_Request_st *msg;
    void *samples[1];
    dds_sample_info_t infos[1];

    // 为sample分配空间
    for (int i = 0; i < 1; i++)
    {
        samples[i] = StartRequest_atomic_service_mbsb_task_A_Request_st__alloc();
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
            msg = (StartRequest_atomic_service_mbsb_task_A_Request_st *)samples[0];
            printf("=== [Subscriber] Received: ");
            //printf("Message (number1: %d, number2: %d, doubleNumber1: %f, doubleNumber2: %f, message1: %s, message2: %s)\n",
            //       msg->number1, msg->number2, msg->doubleNumber1, msg->doubleNumber2, msg->message1, msg->message2);
            // 强制刷新标准输出缓冲区，确保消息立即显示在控制台上
            fflush(stdout);

            // 如果需要返回消息，可以在这里复制数据
            StartRequest_atomic_service_mbsb_task_A_Request_st *ret_msg = (StartRequest_atomic_service_mbsb_task_A_Request_st *)malloc(sizeof(StartRequest_atomic_service_mbsb_task_A_Request_st));
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
            

            
            
            

            // 返回接收到的消息
            return ret_msg;
        }
        // 让线程休眠 300 ms，避免循环占用过多CPU资源。
        dds_sleepfor(DDS_MSECS(300));
    }

    return NULL;
}




void sendData_0292837(dds_entity_t participant, dds_entity_t topic, dds_entity_t writer, EndResponse_atomic_service_sf_task_E_Reply_st data){
    dds_entity_t rc = dds_write(writer, &data);
    {
        if (rc != DDS_RETCODE_OK)
        {
            std::cout << "ERROR: Failed to write topic_1: " << dds_strretcode(-rc) << std::endl;
        }
        else
        {
            std::cout << "SUCCESS: Published endA" << std::endl;
        }
    }
}
