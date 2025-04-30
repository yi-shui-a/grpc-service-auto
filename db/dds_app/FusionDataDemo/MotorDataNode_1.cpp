#include <iostream>
#include <chrono>
#include <thread>
#include <random>
#include <vector>
#include <string>
#include <cstring>

#include "../../atomic_service/MotorData/idl/MotorData.h"
#include "../../atomic_service/MotorData/atomic_include/MotorData.h"
#include "dds/dds.h"

// 定义话题名称
const char *request_topic_name = "StartPublisher_12";
const char *result_topic_name = "MotorDataNode_1";

int main(int argc, char *argv[])
{
    dds_entity_t participant;
    dds_entity_t request_topic;
    dds_entity_t result_topic;
    dds_entity_t subscriber;
    dds_entity_t publisher;
    dds_entity_t request_reader;
    dds_entity_t result_writer;
    dds_return_t rc;

    // 1. 创建域参与者
    participant = dds_create_participant(0, NULL, NULL);
    if (participant < 0)
    {
        std::cerr << "ERROR: Failed to create participant: " << dds_strretcode(-participant) << std::endl;
        return EXIT_FAILURE;
    }

    // 2. 创建请求和结果话题
    request_topic = dds_create_topic(participant, &MotorData_RequestSignal_desc,
                                     request_topic_name, NULL, NULL);
    result_topic = dds_create_topic(participant, &MotorData_MotorResult_desc,
                                    result_topic_name, NULL, NULL);

    if (request_topic < 0)
    {
        std::cerr << "ERROR: Failed to create topics" << std::endl;
        dds_delete(participant);
        return EXIT_FAILURE;
    }
    if (result_topic < 0)
    {
        std::cerr << "ERROR: Failed to create topics" << std::endl;
        dds_delete(participant);
        return EXIT_FAILURE;
    }

    // 3. 创建订阅者和发布者
    subscriber = dds_create_subscriber(participant, NULL, NULL);
    publisher = dds_create_publisher(participant, NULL, NULL);

    if (subscriber < 0)
    {
        std::cerr << "ERROR: Failed to create subscriber" << std::endl;
        dds_delete(request_topic);
        dds_delete(result_topic);
        dds_delete(participant);
        return EXIT_FAILURE;
    }
    if (publisher < 0)
    {
        std::cerr << "ERROR: Failed to create publisher" << std::endl;
        dds_delete(request_topic);
        dds_delete(result_topic);
        dds_delete(participant);
    }

    // 4. 创建读取器和写入器
    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10));
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);

    request_reader = dds_create_reader(subscriber, request_topic, qos, NULL);
    result_writer = dds_create_writer(publisher, result_topic, qos, NULL);

    if (request_reader < 0)
    {
        std::cerr << "ERROR: Failed to create reader" << std::endl;
        dds_delete_qos(qos);
        dds_delete(subscriber);
        dds_delete(publisher);
        dds_delete(request_topic);
        dds_delete(result_topic);
        dds_delete(participant);
        return EXIT_FAILURE;
    }
    if (result_writer < 0)
    {
        std::cerr << "ERROR: Failed to create writer" << std::endl;
        dds_delete_qos(qos);
        dds_delete(subscriber);
        dds_delete(publisher);
        dds_delete(request_topic);
        dds_delete(result_topic);
        dds_delete(participant);
        return EXIT_FAILURE;
    }

    dds_delete_qos(qos);

    std::cout << "MotorDataNode_1 ready. Waiting for requests..." << std::endl;

    // 5. 主处理循环
    while (true)
    {
        void *samples[1];           // 用于接收样本的缓冲区
        dds_sample_info_t infos[1]; // 用于接收样本信息的缓冲区
        // 为sample分配空间
        for (int i = 0; i < 1; i++)
        {
            samples[i] = MotorData_RequestSignal__alloc();
        }

        // 读取请求数据
        rc = dds_take(request_reader, samples, infos, 1, 1);
        if (rc < 0)
        {
            std::cerr << "ERROR: Error reading request: " << dds_strretcode(-rc) << std::endl;
            continue;
        }else if (rc == 0)
        {
            continue; // 无数据可用
        }

        if (infos[0].valid_data && samples[0] != NULL)
        {
            // 接收订阅的数据
            MotorData_RequestSignal *request = (MotorData_RequestSignal *)samples[0];
            std::cout << "SUCCESS: Received request_1" << std::endl;
            // 打印接收到的数据
            std::cout << "Received request: " << request->signal << std::endl;

            // 构造函数输入数据
            RequestSignal *requestSignal = new RequestSignal();
            requestSignal->signal = request->signal;
            MotorResult *motorResult = new MotorResult();

            // 运行操作函数
            statusDetect_func(requestSignal, motorResult);

            // 构造返回结果
            MotorData_MotorResult *result = MotorData_MotorResult__alloc();
            result->motor_id = motorResult->motor_id;
            result->speed = motorResult->speed;
            result->temperature = motorResult->temperature;
            // 分配足够的内存
            result->status = new char[motorResult->status.length() + 1];
            // 复制字符串
            std::strcpy(result->status, motorResult->status.c_str());
            result->return_type = motorResult->return_type;

            // 发布结果
            rc = dds_write(result_writer, result);
            if (rc != DDS_RETCODE_OK)
            {
                std::cerr << "ERROR: Failed to publish result: " << dds_strretcode(-rc) << std::endl;
            }
            else
            {
                std::cout << "SUCCESS: Published detection result for request " << request->signal << std::endl;
                // 打印调试
                std::cout << "DEBUG: result->motor_id = " << result->motor_id << std::endl;
                std::cout << "DEBUG: result->speed = " << result->speed << std::endl;
                std::cout << "DEBUG: result->temperature = " << result->temperature << std::endl;
                std::cout << "DEBUG: result->status = " << result->status << std::endl;
                std::cout << "DEBUG: result->return_type = " << result->return_type << std::endl;
            }
            delete requestSignal;
            delete motorResult;
            // 释放内存
            MotorData_MotorResult_free(result, DDS_FREE_ALL);

            // 释放请求样本
            MotorData_RequestSignal_free(request, DDS_FREE_ALL);
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    // 清理资源 (通常不会执行到这里)
    dds_delete(request_reader);
    dds_delete(result_writer);
    dds_delete(subscriber);
    dds_delete(publisher);
    dds_delete(request_topic);
    dds_delete(result_topic);
    dds_delete(participant);

    return EXIT_SUCCESS;
}