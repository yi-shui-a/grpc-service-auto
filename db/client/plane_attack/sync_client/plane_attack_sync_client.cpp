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


#include "../../../atomic_service/atomic_attack_radar/sync_client_impl/atomic_attack_radar_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_attack_infrared/sync_client_impl/atomic_attack_infrared_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_attack_decode/sync_client_impl/atomic_attack_decode_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_attack_fusion/sync_client_impl/atomic_attack_fusion_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_attack_detect/sync_client_impl/atomic_attack_detect_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_attack_range/sync_client_impl/atomic_attack_range_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_attack_lock/sync_client_impl/atomic_attack_lock_sync_client_impl.cpp"

#include "../../../atomic_service/atomic_attack_release/sync_client_impl/atomic_attack_release_sync_client_impl.cpp"


#include "dds/dds.h"

#include "../idl/StartRequestRadar/StartRequestRadar.h"

#include "../idl/StartRequestInfrared/StartRequestInfrared.h"

#include "../idl/endResponseSF/endResponseSF.h"


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


StartRequestRadar_radar_info *receiveData_537948(dds_entity_t participant, dds_entity_t topic, dds_entity_t reader);

StartRequestInfrared_infrared_info *receiveData_7915608(dds_entity_t participant, dds_entity_t topic, dds_entity_t reader);



endResponseSF_release_result end_0154375;
void sendData_0154375(dds_entity_t participant, dds_entity_t topic, dds_entity_t writer, endResponseSF_release_result data);


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
    std::string serviceName[8] = {
        
        "atomic_attack_radar",
        
        "atomic_attack_infrared",
        
        "atomic_attack_decode",
        
        "atomic_attack_fusion",
        
        "atomic_attack_detect",
        
        "atomic_attack_range",
        
        "atomic_attack_lock",
        
        "atomic_attack_release"
    };
    // 定义服务数量
    int num[8];
    for (int i = 0; i < 8; i++)
    {
        num[i] = 1; // 假设只有一个该服务
    }
    // 定义返回值列表，依次查询服务信息
    QueryInfo queryInfo[8];
    // 查询服务信息
    queryServiceInfo(serviceName, num, 8, queryInfo, broadcastAddress, broadcastPort);

    // 创建grpc channel
    // 创建一个 ChannelInfo 结构体的 vector
    std::vector<ChannelInfo> channel_list;
    for (int i = 0; i < 8; i++)
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
    
    atomic_attack_radar_Service_Client *atomic_attack_radar = nullptr;
    
    atomic_attack_infrared_Service_Client *atomic_attack_infrared = nullptr;
    
    atomic_attack_decode_Service_Client *atomic_attack_decode = nullptr;
    
    atomic_attack_fusion_Service_Client *atomic_attack_fusion = nullptr;
    
    atomic_attack_detect_Service_Client *atomic_attack_detect = nullptr;
    
    atomic_attack_range_Service_Client *atomic_attack_range = nullptr;
    
    atomic_attack_lock_Service_Client *atomic_attack_lock = nullptr;
    
    atomic_attack_release_Service_Client *atomic_attack_release = nullptr;
    

    for (int i = 0; i < channel_list.size(); i++)
    {
        
        if (channel_list[i].ip == queryInfo[0].ip + ":" + std::to_string(queryInfo[0].port))
        {
            atomic_attack_radar = new atomic_attack_radar_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[0].ip << "   " << queryInfo[0].port << std::endl;
        }
        
        if (channel_list[i].ip == queryInfo[1].ip + ":" + std::to_string(queryInfo[1].port))
        {
            atomic_attack_infrared = new atomic_attack_infrared_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[1].ip << "   " << queryInfo[1].port << std::endl;
        }
        
        if (channel_list[i].ip == queryInfo[2].ip + ":" + std::to_string(queryInfo[2].port))
        {
            atomic_attack_decode = new atomic_attack_decode_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[2].ip << "   " << queryInfo[2].port << std::endl;
        }
        
        if (channel_list[i].ip == queryInfo[3].ip + ":" + std::to_string(queryInfo[3].port))
        {
            atomic_attack_fusion = new atomic_attack_fusion_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[3].ip << "   " << queryInfo[3].port << std::endl;
        }
        
        if (channel_list[i].ip == queryInfo[4].ip + ":" + std::to_string(queryInfo[4].port))
        {
            atomic_attack_detect = new atomic_attack_detect_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[4].ip << "   " << queryInfo[4].port << std::endl;
        }
        
        if (channel_list[i].ip == queryInfo[5].ip + ":" + std::to_string(queryInfo[5].port))
        {
            atomic_attack_range = new atomic_attack_range_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[5].ip << "   " << queryInfo[5].port << std::endl;
        }
        
        if (channel_list[i].ip == queryInfo[6].ip + ":" + std::to_string(queryInfo[6].port))
        {
            atomic_attack_lock = new atomic_attack_lock_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[6].ip << "   " << queryInfo[6].port << std::endl;
        }
        
        if (channel_list[i].ip == queryInfo[7].ip + ":" + std::to_string(queryInfo[7].port))
        {
            atomic_attack_release = new atomic_attack_release_Service_Client(channel_list[i].channel);
            std::cout << queryInfo[7].ip << "   " << queryInfo[7].port << std::endl;
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
    dds_entity_t startRadar;
    startRadar = dds_create_topic(participant, &StartRequestRadar_radar_info_desc, "startRadar", NULL, NULL);
    if (startRadar < 0)
    {
        std::cerr << "ERROR: startRadar -- Failed to create topic: " << dds_strretcode(-startRadar) << std::endl;
        return 0;
    }
    // 创建subscriber
    dds_entity_t startRadar_subscriber;
    startRadar_subscriber = dds_create_subscriber(participant, NULL, NULL);
    if (startRadar_subscriber < 0) {
        std::cerr << "ERROR: Failed to create subscriber: " << dds_strretcode(-startRadar_subscriber) << std::endl;
        dds_delete(startRadar);
        dds_delete_qos(qos);
        dds_delete(participant);
        return EXIT_FAILURE;
    }
    // 创建读取器
    dds_entity_t startRadar_reader;
    startRadar_reader = dds_create_reader(startRadar_subscriber, startRadar, qos, NULL);
    if (startRadar_reader < 0)
    {
        std::cerr << "ERROR: startRadar -- Failed to create reader: " << dds_strretcode(-startRadar_reader) << std::endl;
        dds_delete(startRadar);
        dds_delete_qos(qos);
        return 0;
    }
    
    // 创建Topic
    dds_entity_t startInfrared;
    startInfrared = dds_create_topic(participant, &StartRequestInfrared_infrared_info_desc, "startInfrared", NULL, NULL);
    if (startInfrared < 0)
    {
        std::cerr << "ERROR: startInfrared -- Failed to create topic: " << dds_strretcode(-startInfrared) << std::endl;
        return 0;
    }
    // 创建subscriber
    dds_entity_t startInfrared_subscriber;
    startInfrared_subscriber = dds_create_subscriber(participant, NULL, NULL);
    if (startInfrared_subscriber < 0) {
        std::cerr << "ERROR: Failed to create subscriber: " << dds_strretcode(-startInfrared_subscriber) << std::endl;
        dds_delete(startInfrared);
        dds_delete_qos(qos);
        dds_delete(participant);
        return EXIT_FAILURE;
    }
    // 创建读取器
    dds_entity_t startInfrared_reader;
    startInfrared_reader = dds_create_reader(startInfrared_subscriber, startInfrared, qos, NULL);
    if (startInfrared_reader < 0)
    {
        std::cerr << "ERROR: startInfrared -- Failed to create reader: " << dds_strretcode(-startInfrared_reader) << std::endl;
        dds_delete(startInfrared);
        dds_delete_qos(qos);
        return 0;
    }
    

    
    // 创建Topic
    dds_entity_t endSF;
    endSF = dds_create_topic(participant, &endResponseSF_release_result_desc, "endSF", NULL, NULL);
    if (endSF < 0)
    {
        std::cerr << "ERROR: endSF -- Failed to create topic: " << dds_strretcode(-endSF) << std::endl;
        return 0;
    }
    // 创建写入器
    dds_entity_t endSF_writer;
    endSF_writer = dds_create_writer(participant, endSF, qos, NULL);
        if (endSF_writer < 0)
        {
            std::cerr << "ERROR: Failed to create writer for " << endSF << ": "
                      << dds_strretcode(-endSF_writer) << std::endl;
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
    
    StartRequestRadar_radar_info *start_537948 = receiveData_537948(participant, startRadar, startRadar_reader);
    
    StartRequestInfrared_infrared_info *start_7915608 = receiveData_7915608(participant, startInfrared, startInfrared_reader);
    
    

    std::cout << "INFO: start info received." << std::endl;

    //===============================================================================
    //                             setParam :设置结构体变量值
    //===============================================================================

    // 声明变量并赋值
    
    radar_info request_4168460;
    
    infrared_info request_259612;
    
    iamge_input request_1854839;
    
    fusion_input request_731251;
    
    detect_request request_0807829;
    
    range_request request_4251873;
    
    lock_request request_0461617;
    
    release_request request_015813;
    
    
    //为开始的服务赋值
    
    request_4168460.x = start_537948->x;
    
    request_4168460.y = start_537948->y;
    
    request_4168460.z = start_537948->z;
    
    request_4168460.size = start_537948->size;
    
    request_259612.x = start_7915608->x;
    
    request_259612.y = start_7915608->y;
    
    request_259612.z = start_7915608->z;
    
    request_259612.size = start_7915608->size;
    

    //===============================================================================
    //                                 调用服务流程
    //===============================================================================
    // 运行服务
    
    radar_result reply_4168460 = atomic_attack_radar->getRaderMonitor(request_4168460);
    
    infrared_result reply_259612 = atomic_attack_infrared->getInfraredMonitor(request_259612);
    


    // 赋值
    
    request_731251.size = reply_4168460.size;
    
    request_731251.x = reply_4168460.x;
    
    request_731251.y = reply_4168460.y;
    
    request_731251.z = reply_4168460.z;
    
    request_1854839.size = reply_259612.size;
    
    request_1854839.x = reply_259612.x;
    
    request_1854839.y = reply_259612.y;
    
    request_1854839.z = reply_259612.z;
    
    // 运行服务
    
    iamge_output reply_1854839 = atomic_attack_decode->decodeImage(request_1854839);
    


    // 赋值
    
    request_731251.x = reply_1854839.x;
    
    request_731251.y = reply_1854839.y;
    
    request_731251.z = reply_1854839.z;
    
    request_731251.size = reply_1854839.size;
    
    // 运行服务
    
    fusion_output reply_731251 = atomic_attack_fusion->getFusionData(request_731251);
    


    // 赋值
    
    request_0807829.x = reply_731251.x;
    
    request_0807829.y = reply_731251.y;
    
    request_0807829.z = reply_731251.z;
    
    request_0807829.size = reply_731251.size;
    
    request_4251873.x = reply_731251.x;
    
    request_4251873.y = reply_731251.y;
    
    request_4251873.z = reply_731251.z;
    
    request_4251873.size = reply_731251.size;
    
    // 运行服务
    
    detect_result reply_0807829 = atomic_attack_detect->imageDetect(request_0807829);
    
    range_result reply_4251873 = atomic_attack_range->imageRange(request_4251873);
    


    // 赋值
    
    request_0461617.object_class = reply_0807829.object_class;
    
    request_0461617.confidence = reply_0807829.confidence;
    
    request_0461617.x_min = reply_0807829.x_min;
    
    request_0461617.y_min = reply_0807829.y_min;
    
    request_0461617.x_max = reply_0807829.x_max;
    
    request_0461617.y_max = reply_0807829.y_max;
    
    request_0461617.z = reply_4251873.z;
    
    // 运行服务
    
    lock_result reply_0461617 = atomic_attack_lock->targetLock(request_0461617);
    


    // 赋值
    
    request_015813.x = reply_0461617.x;
    
    request_015813.y = reply_0461617.y;
    
    request_015813.z = reply_0461617.z;
    
    // 运行服务
    
    release_result reply_015813 = atomic_attack_release->getTargetInfo(request_015813);
    


    // 赋值
    
    std::cout << "plane_attack output: " << std::endl
    
            << reply_015813.x << std::endl
    
            << reply_015813.y << std::endl
    
            << reply_015813.z << std::endl
    
            << reply_015813.return_type << std::endl;

    // 赋值
    
    end_0154375.x = reply_015813.x;
    
    end_0154375.y = reply_015813.y;
    
    end_0154375.z = reply_015813.z;
    
    end_0154375.return_type = reply_015813.return_type;
    
    
    sendData_0154375(participant, endSF, endSF_writer, end_0154375);
    
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


StartRequestRadar_radar_info *receiveData_537948(dds_entity_t participant, dds_entity_t topic, dds_entity_t reader)
{
    // 定义dds数据类型
    dds_return_t rc;
    StartRequestRadar_radar_info *msg;
    void *samples[1];
    dds_sample_info_t infos[1];

    // 为sample分配空间
    for (int i = 0; i < 1; i++)
    {
        samples[i] = StartRequestRadar_radar_info__alloc();
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
            msg = (StartRequestRadar_radar_info *)samples[0];
            printf("=== [Subscriber] Received: ");
            //printf("Message (number1: %d, number2: %d, doubleNumber1: %f, doubleNumber2: %f, message1: %s, message2: %s)\n",
            //       msg->number1, msg->number2, msg->doubleNumber1, msg->doubleNumber2, msg->message1, msg->message2);
            // 强制刷新标准输出缓冲区，确保消息立即显示在控制台上
            fflush(stdout);

            // 如果需要返回消息，可以在这里复制数据
            StartRequestRadar_radar_info *ret_msg = (StartRequestRadar_radar_info *)malloc(sizeof(StartRequestRadar_radar_info));
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
            
            
            

            
            ret_msg->x = msg->x;
            

            

            
            ret_msg->y = msg->y;
            

            

            
            ret_msg->z = msg->z;
            

            

            
            ret_msg->size = msg->size;
            

            
            
            

            // 返回接收到的消息
            return ret_msg;
        }
        // 让线程休眠 50 ms，避免循环占用过多CPU资源。
        dds_sleepfor(DDS_MSECS(50));
    }

    return NULL;
}

StartRequestInfrared_infrared_info *receiveData_7915608(dds_entity_t participant, dds_entity_t topic, dds_entity_t reader)
{
    // 定义dds数据类型
    dds_return_t rc;
    StartRequestInfrared_infrared_info *msg;
    void *samples[1];
    dds_sample_info_t infos[1];

    // 为sample分配空间
    for (int i = 0; i < 1; i++)
    {
        samples[i] = StartRequestInfrared_infrared_info__alloc();
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
            msg = (StartRequestInfrared_infrared_info *)samples[0];
            printf("=== [Subscriber] Received: ");
            //printf("Message (number1: %d, number2: %d, doubleNumber1: %f, doubleNumber2: %f, message1: %s, message2: %s)\n",
            //       msg->number1, msg->number2, msg->doubleNumber1, msg->doubleNumber2, msg->message1, msg->message2);
            // 强制刷新标准输出缓冲区，确保消息立即显示在控制台上
            fflush(stdout);

            // 如果需要返回消息，可以在这里复制数据
            StartRequestInfrared_infrared_info *ret_msg = (StartRequestInfrared_infrared_info *)malloc(sizeof(StartRequestInfrared_infrared_info));
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
            
            
            

            
            ret_msg->x = msg->x;
            

            

            
            ret_msg->y = msg->y;
            

            

            
            ret_msg->z = msg->z;
            

            

            
            ret_msg->size = msg->size;
            

            
            
            

            // 返回接收到的消息
            return ret_msg;
        }
        // 让线程休眠 50 ms，避免循环占用过多CPU资源。
        dds_sleepfor(DDS_MSECS(50));
    }

    return NULL;
}




void sendData_0154375(dds_entity_t participant, dds_entity_t topic, dds_entity_t writer, endResponseSF_release_result data){
    dds_entity_t rc = dds_write(writer, &data);
    {
        if (rc != DDS_RETCODE_OK)
        {
            std::cout << "ERROR: Failed to write topic_1: " << dds_strretcode(-rc) << std::endl;
        }
        else
        {
            std::cout << "SUCCESS: Published endSF" << std::endl;
        }
    }
}
