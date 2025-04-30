#include <iostream>
#include <chrono>
#include <thread>
#include <random>
#include <string>
#include <vector>
#include <mutex>

// 包含生成的DDS头文件和C++ API
#include "../../atomic_service/ImageDetection/idl/ImageDetection.h"
#include "../../atomic_service/RobotPose/idl/RobotPose.h"
#include "../../atomic_service/RadarData/idl/RadarData.h"
#include "../../atomic_service/MotorData/idl/MotorData.h"

#include "dds/dds.h"

// 定义不同的Topic名称，对应四个不同的数据通道
const char *topic_names[4] = {
    "StartPublisher_11",
    "StartPublisher_12",
    "StartPublisher_13",
    "StartPublisher_14"};

// 定义4个不同的数据类型描述符，与上面的Topic一一对应
const dds_topic_descriptor_t *type_descs[4] = {
    &ImageDetection_RequestSignal_desc,
    &MotorData_RequestSignal_desc,
    &RadarData_RequestSignal_desc,
    &RobotPose_RequestSignal_desc};

// 全局互斥锁，用于保护cout输出
std::mutex cout_mutex;

// 线程函数，用于发布特定topic的数据
void publish_thread_func(dds_entity_t writer, int topic_index, int count)
{
    dds_return_t rc;

    for (int i = 0; i < count; ++i)
    {
        switch (topic_index)
        {
        case 0:
        {
            ImageDetection_RequestSignal imageDetection_data = {.signal = 11};
            rc = dds_write(writer, &imageDetection_data);
            {
                std::lock_guard<std::mutex> lock(cout_mutex);
                if (rc != DDS_RETCODE_OK)
                {
                    std::cout << "ERROR: Failed to write topic_1: " << dds_strretcode(-rc) << std::endl;
                }
                else
                {
                    std::cout << "SUCCESS: Published topic_1" << std::endl;
                }
            }
            break;
        }
        case 1:
        {
            MotorData_RequestSignal motorData_data = {.signal = 22, .motor_id = 222};
            rc = dds_write(writer, &motorData_data);
            {
                std::lock_guard<std::mutex> lock(cout_mutex);
                if (rc != DDS_RETCODE_OK)
                {
                    std::cout << "ERROR: Failed to write topic_2: " << dds_strretcode(-rc) << std::endl;
                }
                else
                {
                    std::cout << "SUCCESS: Published topic_2" << std::endl;
                }
            }
            break;
        }
        case 2:
        {
            RadarData_RequestSignal radarData_data = {.signal = 33, .radar_id = 333};
            rc = dds_write(writer, &radarData_data);
            {
                std::lock_guard<std::mutex> lock(cout_mutex);
                if (rc != DDS_RETCODE_OK)
                {
                    std::cout << "ERROR: Failed to write topic_3: " << dds_strretcode(-rc) << std::endl;
                }
                else
                {
                    std::cout << "SUCCESS: Published topic_3" << std::endl;
                }
            }
            break;
        }
        case 3:
        {
            RobotPose_RequestSignal robotPose_data = {.signal = 44};
            rc = dds_write(writer, &robotPose_data);
            {
                std::lock_guard<std::mutex> lock(cout_mutex);
                if (rc != DDS_RETCODE_OK)
                {
                    std::cout << "ERROR: Failed to write topic_4: " << dds_strretcode(-rc) << std::endl;
                }
                else
                {
                    std::cout << "SUCCESS: Published topic_4" << std::endl;
                }
            }
            break;
        }
        }
        std::this_thread::sleep_for(std::chrono::seconds(5));
    }
}
int main(int argc, char *argv[])
{
    // DDS实体声明
    dds_entity_t participant; // 域参与者
    dds_entity_t topics[4];   // Topic实体
    dds_entity_t publisher;   // 发布者
    dds_entity_t writers[4];  // 数据写入器
    dds_return_t rc;          // 操作返回值

    /**************************************************************************
     * 1. 创建DDS域参与者
     * 参数说明：
     *   - 第一个参数：域ID，0表示默认域
     *   - 第二个参数：QoS配置，NULL表示使用默认配置
     *   - 第三个参数：监听器，NULL表示不使用
     *************************************************************************/
    participant = dds_create_participant(0, NULL, NULL);
    if (participant < 0)
    {
        std::cerr << "ERROR: Failed to create participant: " << dds_strretcode(-participant) << std::endl;
        return EXIT_FAILURE;
    }

    /**************************************************************************
     * 2. 创建四个Topic
     * 注意：Cyclone DDS v0.11.0无需显式注册数据类型，创建Topic时会自动处理
     * 参数说明：
     *   - 第一个参数：域参与者
     *   - 第二个参数：数据类型描述符
     *   - 第三个参数：Topic名称
     *   - 第四个参数：QoS配置，NULL表示使用默认配置
     *   - 第五个参数：监听器，NULL表示不使用
     *************************************************************************/
    topics[0] = dds_create_topic(participant, type_descs[0], topic_names[0], NULL, NULL);
    topics[1] = dds_create_topic(participant, type_descs[1], topic_names[1], NULL, NULL);
    topics[2] = dds_create_topic(participant, type_descs[2], topic_names[2], NULL, NULL);
    topics[3] = dds_create_topic(participant, type_descs[3], topic_names[3], NULL, NULL);
    // 检查Topic创建是否成功
    for (int i = 0; i < 4; i++)
    {
        if (topics[i] < 0)
        {
            std::cerr << "ERROR: Failed to create topic " << topic_names[i] << ": "
                      << dds_strretcode(-topics[i]) << std::endl;
            // 清理已创建的Topic
            for (int j = 0; j < i; j++)
                dds_delete(topics[j]);
            dds_delete(participant);
            return EXIT_FAILURE;
        }
    }

    /**************************************************************************
     * 3. 创建发布者
     * 参数说明：
     *   - 第一个参数：域参与者
     *   - 第二个参数：QoS配置，NULL表示使用默认配置
     *   - 第三个参数：监听器，NULL表示不使用
     *************************************************************************/
    publisher = dds_create_publisher(participant, NULL, NULL);
    if (publisher < 0)
    {
        std::cerr << "ERROR: Failed to create publisher: " << dds_strretcode(-publisher) << std::endl;
        for (int i = 0; i < 4; i++)
            dds_delete(topics[i]);
        dds_delete(participant);
        return EXIT_FAILURE;
    }

    /**************************************************************************
     * 4. 创建四个数据写入器(DataWriter)，每个对应一个Topic
     * 首先创建QoS配置：
     *   - 可靠性：RELIABLE（可靠传输）
     *   - 历史记录：保留最后10个样本
     *************************************************************************/
    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10)); // 可靠传输，超时10秒
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);                  // 保留最后10个样本
    // 为每个Topic创建数据写入器
    for (int i = 0; i < 4; i++)
    {
        writers[i] = dds_create_writer(publisher, topics[i], qos, NULL);
        if (writers[i] < 0)
        {
            std::cerr << "ERROR: Failed to create writer for " << topic_names[i] << ": "
                      << dds_strretcode(-writers[i]) << std::endl;
            // 清理已创建的写入器
            for (int j = 0; j < i; j++)
                dds_delete(writers[j]);
            dds_delete_qos(qos);
            for (int i = 0; i < 4; i++)
                dds_delete(topics[i]);
            dds_delete(publisher);
            dds_delete(participant);
            return EXIT_FAILURE;
        }
    }

    // QoS配置不再需要，可以删除
    dds_delete_qos(qos);

    std::cout << "Publisher ready. Sending data..." << std::endl;

    // 5. 准备数据
    // 如果不需要处理数据，则不需要该步骤

    /**************************************************************************
     * 6. 数据发布主循环
     * 这里循环20次，每次向四个Topic各发布一条消息
     *************************************************************************/
    const int publish_count = 20;
    std::vector<std::thread> threads;

    for (int i = 0; i < 4; ++i)
    {
        threads.emplace_back(publish_thread_func, writers[i], i, publish_count);
    }

    // 等待所有线程完成
    for (auto &thread : threads)
    {
        thread.join();
    }

    /**************************************************************************
     * 7. 清理资源
     * 按照DDS实体的创建顺序反向删除：
     * 1. 数据写入器
     * 2. Topic
     * 3. 发布者
     * 4. 域参与者
     *************************************************************************/
    std::cout << "Publisher shutting down..." << std::endl;
    for (int i = 0; i < 4; i++)
    {
        dds_delete(writers[i]);
        dds_delete(topics[i]);
    }
    dds_delete(publisher);
    dds_delete(participant);

    return EXIT_SUCCESS;
}