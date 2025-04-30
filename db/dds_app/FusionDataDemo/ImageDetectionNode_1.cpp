#include <iostream>
#include <chrono>
#include <thread>
#include <random>
#include <vector>
#include <string>
#include <cstring>

#include "../../atomic_service/ImageDetection/idl/ImageDetection.h"
#include "../../atomic_service/ImageDetection/atomic_include/ImageDetection.h"
#include "dds/dds.h"

// 定义话题名称
const char *request_topic_name = "StartPublisher_11";
const char *result_topic_name = "ImageDetectionNode_1";

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
    request_topic = dds_create_topic(participant, &ImageDetection_RequestSignal_desc,
                                     request_topic_name, NULL, NULL);
    result_topic = dds_create_topic(participant, &ImageDetection_DetectionResult_desc,
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

    std::cout << "ImageDetectionNode_1 ready. Waiting for requests..." << std::endl;

    // 5. 主处理循环
    while (true)
    {
        void *samples[1];           // 用于接收样本的缓冲区
        dds_sample_info_t infos[1]; // 用于接收样本信息的缓冲区
        // 为sample分配空间
        for (int i = 0; i < 1; i++)
        {
            samples[i] = ImageDetection_RequestSignal__alloc();
        }

        // 读取请求数据
        rc = dds_take(request_reader, samples, infos, 1, 1);
        if (rc < 0)
        {
            std::cerr << "ERROR: Error reading request: " << dds_strretcode(-rc) << std::endl;
            continue;
        }
        else if (rc == 0)
        {
            continue; // 无数据可用
        }
        if (infos[0].valid_data && samples[0] != NULL)
        {
            // 接收订阅的数据
            ImageDetection_RequestSignal *request = (ImageDetection_RequestSignal *)samples[0];
            std::cout << "DEBUG: request->signal = " << request->signal << std::endl; // 打印调试
            std::cout << "SUCCESS: Received request_1" << std::endl;
            // 构造函数输入数据
            RequestSignal *requestSignal = new RequestSignal();
            requestSignal->signal = request->signal;
            DetectionResult *detectionResult = new DetectionResult();
            // 运行操作函数
            imageDetect_func(requestSignal, detectionResult);

            // 构造返回结果
            ImageDetection_DetectionResult *result = ImageDetection_DetectionResult__alloc();
            result->camera_id = detectionResult->camera_id;

            // 分配足够的内存
            result->object_class = new char[detectionResult->object_class.length() + 1];
            // 复制字符串
            std::strcpy(result->object_class, detectionResult->object_class.c_str());

            result->confidence = detectionResult->confidence;
            result->x_min = detectionResult->x_min;
            result->y_min = detectionResult->y_min;
            result->x_max = detectionResult->x_max;
            result->y_max = detectionResult->y_max;
            result->return_type = detectionResult->return_type;
            // 发布结果
            rc = dds_write(result_writer, result);
            if (rc != DDS_RETCODE_OK)
            {
                std::cerr << "ERROR: Failed to publish result: " << dds_strretcode(-rc) << std::endl;
            }
            else
            {
                std::cout << "SUCCESS: Published detection result for request " << std::endl;
                // 打印调试
                std::cout << "DEBUG: result->camera_id = " << result->camera_id << std::endl;
                std::cout << "DEBUG: result->object_class = " << result->object_class << std::endl;
                std::cout << "DEBUG: result->confidence = " << result->confidence << std::endl;
                std::cout << "DEBUG: result->x_min = " << result->x_min << std::endl;
                std::cout << "DEBUG: result->y_min = " << result->y_min << std::endl;
                std::cout << "DEBUG: result->x_max = " << result->x_max << std::endl;
                std::cout << "DEBUG: result->y_max = " << result->y_max << std::endl;
                std::cout << "DEBUG: result->return_type = " << result->return_type << std::endl;
            }
            delete requestSignal;   // 如果用 new
            delete detectionResult; // 如果用 new
            // 释放内存
            ImageDetection_DetectionResult_free(result, DDS_FREE_ALL);

            // 释放请求样本
            ImageDetection_RequestSignal_free(request, DDS_FREE_ALL);
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