#include <iostream>
#include <dds/dds.h>
#include "StartRequest.h" // IDL生成的C语言头文件

// DDS实体句柄
static dds_entity_t participant;
static dds_entity_t topic;
static dds_entity_t publisher;
static dds_entity_t writer;

// 清理DDS资源
static void cleanup()
{
    if (writer != DDS_HANDLE_NIL)
        dds_delete(writer);
    if (publisher != DDS_HANDLE_NIL)
        dds_delete(publisher);
    if (topic != DDS_HANDLE_NIL)
        dds_delete(topic);
    if (participant != DDS_HANDLE_NIL)
        dds_delete(participant);
}

int main()
{
    dds_return_t rc;

    // 1. 初始化DDS参与者（DomainParticipant）
    participant = dds_create_participant(DDS_DOMAIN_DEFAULT, NULL, NULL);
    if (participant < 0)
    {
        std::cerr << "错误：创建参与者失败，原因：" << dds_strretcode(-participant) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }

    // 2. 创建主题（Topic），名称需与订阅者一致
    topic = dds_create_topic(
        participant,
        &StartRequest_atomic_service_mbsb_task_A_Request_st_desc, // IDL生成的类型描述
        "startA",                                                 // 主题名称（必须与订阅者一致）
        NULL, NULL);
    if (topic < 0)
    {
        std::cerr << "错误：创建主题失败，原因：" << dds_strretcode(-topic) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }

    // 3. 创建发布者（Publisher）
    publisher = dds_create_publisher(participant, NULL, NULL);
    if (publisher < 0)
    {
        std::cerr << "错误：创建发布者失败，原因：" << dds_strretcode(-publisher) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }

    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10));
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);

    // 4. 创建数据写入器（DataWriter）
    writer = dds_create_writer(publisher, topic, qos, NULL);
    if (writer < 0)
    {
        std::cerr << "错误：创建写入器失败，原因：" << dds_strretcode(-writer) << std::endl;
        cleanup();
        return EXIT_FAILURE;
    }
    dds_delete_qos(qos);

    std::cout << "DDS发布者已启动，开始发送数据..." << std::endl;

    // 5. 循环发送数据（示例：发送5次，每次间隔1秒）
    for (int i = 0; i < 10; i++)
    {
        // 构造待发送的数据（栈上分配，无需手动释放）
        StartRequest_atomic_service_mbsb_task_A_Request_st data;
        data.number1 = 10 * i; // 示例number1（可自定义）
        data.number2 = 20 * i; // 示例number2（可自定义）

        // 发送数据
        rc = dds_write(writer, &data);
        if (rc != DDS_RETCODE_OK)
        {
            std::cerr << "错误：dds_write失败，原因：" << dds_strretcode(-rc) << std::endl;
            cleanup();
            return EXIT_FAILURE;
        }

        // 使用cout打印发送的信息
        std::cout << "==============================" << std::endl;
        std::cout << "已发送数据（第" << (i + 1) << "次）:" << std::endl;
        std::cout << "number1: " << data.number1 << std::endl;
        std::cout << "number2: " << data.number2 << std::endl;
        std::cout << "==============================" << std::endl;

        // 间隔1秒发送
        dds_sleepfor(DDS_SECS(1));
    }

    // 清理资源
    cleanup();
    return EXIT_SUCCESS;
}
