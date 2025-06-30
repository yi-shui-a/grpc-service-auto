#include <iostream>
#include <dds/dds.h>
#include "endResponseSF.h"  // IDL生成的C语言头文件

// DDS实体句柄
static dds_entity_t participant;
static dds_entity_t topic;
static dds_entity_t subscriber;
static dds_entity_t reader;

// 清理DDS资源
static void cleanup() {
    if (reader != DDS_HANDLE_NIL) dds_delete(reader);
    if (subscriber != DDS_HANDLE_NIL) dds_delete(subscriber);
    if (topic != DDS_HANDLE_NIL) dds_delete(topic);
    if (participant != DDS_HANDLE_NIL) dds_delete(participant);
}

int main() {
    dds_return_t rc;
    void *samples[1];       // 存储DDS样本的数组（最多1个样本）
    dds_sample_info_t info; // 样本元信息（如有效性、时间戳等）

    // 1. 初始化DDS参与者（DomainParticipant）
    participant = dds_create_participant(DDS_DOMAIN_DEFAULT, NULL, NULL);
    if (participant < 0) {
        std::cerr << "错误：创建参与者失败，原因：" << dds_strretcode(-participant) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }

    // 2. 创建主题（Topic），名称需与发布者一致
    topic = dds_create_topic(
        participant,
        &endResponseSF_release_result_desc,  // IDL生成的类型描述
        "endSF",  // 主题名称（必须与发布者一致）
        NULL, NULL
    );
    if (topic < 0) {
        std::cerr << "错误：创建主题失败，原因：" << dds_strretcode(-topic) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }

    // 3. 创建订阅者（Subscriber）
    subscriber = dds_create_subscriber(participant, NULL, NULL);
    if (subscriber < 0) {
        std::cerr << "错误：创建订阅者失败，原因：" << dds_strretcode(-subscriber) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }

    // 4. 创建数据读取器（DataReader）
    reader = dds_create_reader(subscriber, topic, NULL, NULL);
    if (reader < 0) {
        std::cerr << "错误：创建读取器失败，原因：" << dds_strretcode(-reader) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }

    std::cout << "DDS订阅者已启动，等待接收数据..." << std::endl;

    // 5. 循环读取数据
    while (1) {
        // 分配样本内存（需与IDL生成的结构体类型匹配）
        samples[0] = endResponseSF_release_result__alloc();
        if (samples[0] == NULL) {
            std::cerr << "错误：分配样本内存失败" << std::endl;
            cleanup();
            return EXIT_FAILURE;
        }

        // 从读取器中获取数据（最多1个样本）
        rc = dds_take(reader, samples, &info, 1, 1);
        if (rc < 0) {
            std::cerr << "错误：dds_take失败，原因：" << dds_strretcode(-rc) << std::endl;
            endResponseSF_release_result_free(samples[0], DDS_FREE_ALL);
            cleanup();
            return EXIT_FAILURE;
        }

        // 检查是否有有效数据
        if (rc > 0 && info.valid_data) {
            // 转换为目标结构体类型
            endResponseSF_release_result *data = 
                (endResponseSF_release_result *)samples[0];

            // 使用cout打印数据
            std::cout << "==============================" << std::endl;
            std::cout << "接收到新数据:" << std::endl;
            std::cout << "x: " << data->x << std::endl;
            std::cout << "y: " << data->y << std::endl;
            std::cout << "z: " << data->z << std::endl;
            std::cout << "return_type: " << data->return_type << std::endl;
            std::cout << "==============================" << std::endl;
        }

        // 释放样本内存
        endResponseSF_release_result_free(samples[0], DDS_FREE_ALL);

        // 休眠100ms避免CPU占用过高
        dds_sleepfor(DDS_MSECS(100));
    }

    // 清理资源（实际不会执行到，可通过Ctrl+C终止程序）
    cleanup();
    return EXIT_SUCCESS;
}
