#include <iostream>
#include <chrono>
#include <thread>
#include <random>
#include <vector>
#include <string>
#include <cstring>

#include "../../atomic_service/RobotPose/idl/RobotPose.h"
#include "../../atomic_service/RobotPose/atomic_include/RobotPose.h"
#include "dds/dds.h"

const char *request_topic_name = "StartPublisher_14";
const char *result_topic_name = "RobotPoseNode_1";

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
    request_topic = dds_create_topic(participant, &RobotPose_RequestSignal_desc,
                                     request_topic_name, NULL, NULL);
    result_topic = dds_create_topic(participant, &RobotPose_RobotResult_desc,
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
        return EXIT_FAILURE;
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

    std::cout << "RobotPoseNode_1 ready. Waiting for requests..." << std::endl;

    // 5. 主处理循环
    while (true)
    {
        void *samples[1];           // 用于接收样本的缓冲区
        dds_sample_info_t infos[1]; // 用于接收样本信息的缓冲区
        // 为sample分配空间
        for (int i = 0; i < 1; i++)
        {
            samples[i] = RobotPose_RequestSignal__alloc();
        }
        // 读取请求数据
        rc = dds_take(request_reader, samples, infos, 1, 1);
        if (rc < 0)
        {
            std::cerr << "ERROR: Error reading request: " << dds_strretcode(-rc) << std::endl;
            continue;
        }        else if (rc == 0)
        {
            continue; // 无数据可用
        }

        if (infos[0].valid_data)
        {
            // 接收订阅的数据
            RobotPose_RequestSignal *request = (RobotPose_RequestSignal *)samples[0];
            std::cout << "SUCCESS: Received request_1" << std::endl;
            // 打印接收到的数据
            std::cout << "Received request: " << request->signal << std::endl;

            // 构造函数输入数据
            RequestSignal *requestSignal = new RequestSignal();
            requestSignal->signal = request->signal;
            RobotResult *robotResult = new RobotResult();

            // 运行操作函数
            getRobotPose_func(requestSignal, robotResult);

            // 构造返回结果
            RobotPose_RobotResult *result = RobotPose_RobotResult__alloc();
            result->robot_id = robotResult->robot_id;
            result->x = robotResult->x;
            result->y = robotResult->y;
            result->z = robotResult->z;
            result->roll = robotResult->roll;
            result->pitch = robotResult->pitch;
            result->yaw = robotResult->yaw;
            result->return_type = robotResult->return_type;

            // 发布结果
            rc = dds_write(result_writer, result);
            if (rc != DDS_RETCODE_OK)
            {
                std::cerr << "ERROR: Failed to publish result: " << dds_strretcode(-rc) << std::endl;
            }
            else
            {
                std::cout << "SUCCESS: Published robot pose result for request " << request->signal << std::endl;
                // 打印发布的结果
                std::cout << "DEBUG: result->robot_id = " << result->robot_id << std::endl;
                std::cout << "DEBUG: result->x = " << result->x << std::endl;
                std::cout << "DEBUG: result->y = " << result->y << std::endl;
                std::cout << "DEBUG: result->z = " << result->z << std::endl;
                std::cout << "DEBUG: result->roll = " << result->roll << std::endl;
                std::cout << "DEBUG: result->pitch = " << result->pitch << std::endl;
                std::cout << "DEBUG: result->yaw = " << result->yaw << std::endl;
                std::cout << "DEBUG: result->return_type = " << result->return_type << std::endl;
            }
            delete requestSignal;
            delete robotResult;
            // 释放内存
            RobotPose_RobotResult_free(result, DDS_FREE_ALL);

            // 释放请求样本
            RobotPose_RequestSignal_free(request, DDS_FREE_ALL);
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