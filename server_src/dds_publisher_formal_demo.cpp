#include "dds/dds.h"
#include "../IDL_inc/example.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>

int main(int argc, char **argv)
{
    dds_entity_t participant;
    dds_entity_t topic;
    dds_entity_t writer;
    dds_return_t rc;
    FormalTest_test1 msg;
    uint32_t status = 0;

    // 创建参与者
    participant = dds_create_participant(DDS_DOMAIN_DEFAULT, NULL, NULL);
    if (participant < 0)
        DDS_FATAL("dds_create_participant: %s\n", dds_strretcode(-participant));

    // 创建主题
    topic = dds_create_topic(
        participant, &FormalTest_test1_desc, "FormalTest_test1", NULL, NULL);
    if (topic < 0)
        DDS_FATAL("dds_create_topic: %s\n", dds_strretcode(-topic));

    // 创建写入者
    writer = dds_create_writer(participant, topic, NULL, NULL);
    if (writer < 0)
        DDS_FATAL("dds_create_writer: %s\n", dds_strretcode(-writer));

    printf("=== [Publisher] Waiting for a reader to be discovered ...\n");
    fflush(stdout);

    // 设置状态掩码
    rc = dds_set_status_mask(writer, DDS_PUBLICATION_MATCHED_STATUS);
    if (rc != DDS_RETCODE_OK)
        DDS_FATAL("dds_set_status_mask: %s\n", dds_strretcode(-rc));

    // 等待订阅者
    while (!(status & DDS_PUBLICATION_MATCHED_STATUS))
    {
        rc = dds_get_status_changes(writer, &status);
        if (rc != DDS_RETCODE_OK)
            DDS_FATAL("dds_get_status_changes: %s\n", dds_strretcode(-rc));

        dds_sleepfor(DDS_MSECS(20));
    }

    // 创建消息
    msg.number1 = 1;
    msg.number2 = 2;
    msg.doubleNumber1 = 3.14;
    msg.doubleNumber2 = 2.71;
    msg.message1 = "Hello";
    msg.message2 = "World";

    printf("=== [Publisher] Writing: ");
    printf("Message (number1: %d, number2: %d, doubleNumber1: %f, doubleNumber2: %f, message1: %s, message2: %s)\n",
           msg.number1, msg.number2, msg.doubleNumber1, msg.doubleNumber2, msg.message1, msg.message2);
    fflush(stdout);

    // 写入消息
    rc = dds_write(writer, &msg);
    if (rc != DDS_RETCODE_OK)
        DDS_FATAL("dds_write: %s\n", dds_strretcode(-rc));

    // 删除参与者
    rc = dds_delete(participant);
    if (rc != DDS_RETCODE_OK)
        DDS_FATAL("dds_delete: %s\n", dds_strretcode(-rc));

    return EXIT_SUCCESS;
}