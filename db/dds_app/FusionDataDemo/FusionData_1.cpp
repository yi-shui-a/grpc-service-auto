#include <iostream>
#include <chrono>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <vector>

#include "../../atomic_service/FusionData/idl/FusionData.h"
#include "../../atomic_service/ImageDetection/idl/ImageDetection.h"
#include "../../atomic_service/RobotPose/idl/RobotPose.h"
#include "../../atomic_service/RadarData/idl/RadarData.h"
#include "../../atomic_service/MotorData/idl/MotorData.h"

#include "../../atomic_service/FusionData/atomic_include/FusionData.h"
// #include "../../atomic_service/ImageDetection/atomic_include/ImageDetection.h"
// #include "../../atomic_service/RobotPose/atomic_include/RobotPose.h"
// #include "../../atomic_service/RadarData/atomic_include/RadarData.h"
// #include "../../atomic_service/MotorData/atomic_include/MotorData.h"
#include "dds/dds.h"

// 全局数据结构，存储每个Topic的最新消息
struct GlobalData
{
    // 图像检测数据
    DetectionResult image_data;
    std::mutex image_mutex;
    std::atomic<bool> image_initialized{false};

    // 电机数据
    MotorResult motor_data;
    std::mutex motor_mutex;
    std::atomic<bool> motor_initialized{false};

    // 雷达数据
    RadarResult radar_data;
    std::mutex radar_mutex;
    std::atomic<bool> radar_initialized{false};

    // 机器人姿态数据
    RobotResult robot_data;
    std::mutex robot_mutex;
    std::atomic<bool> robot_initialized{false};

    // 用于通知主线程的条件变量
    std::condition_variable cv;
    std::mutex cv_mutex;
} global_data;

// 订阅图像检测数据的线程函数
void image_detection_subscriber(dds_entity_t participant)
{
    dds_entity_t topic;
    dds_entity_t reader;
    dds_return_t rc;

    // 创建Topic
    topic = dds_create_topic(participant, &ImageDetection_DetectionResult_desc,
                             "ImageDetectionNode_1", NULL, NULL);
    if (topic < 0)
    {
        std::cerr << "ERROR: ImageDetectionNode_1 -- Failed to create topic: " << dds_strretcode(-topic) << std::endl;
        return;
    }

    // 创建读取器
    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10));
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);

    reader = dds_create_reader(participant, topic, qos, NULL);
    if (reader < 0)
    {
        std::cerr << "ERROR: ImageDetectionNode_1 -- Failed to create reader: " << dds_strretcode(-reader) << std::endl;
        dds_delete(topic);
        dds_delete_qos(qos);
        return;
    }
    dds_delete_qos(qos);

    std::cout << "ImageDetectionNode_1 subscriber ready" << std::endl;

    while (true)
    {
        void *samples[1];
        dds_sample_info_t infos[1];
        // 为sample分配空间
        for (int i = 0; i < 1; i++)
        {
            samples[i] = ImageDetection_DetectionResult__alloc();
        }

        // 阻塞读取数据
        rc = dds_take(reader, samples, infos, 1, 1);
        if (rc < 0)
        {
            std::cerr << "Error: ImageDetectionNode_1 -- Error reading: " << dds_strretcode(-rc) << std::endl;
            continue;
        }
        else if (rc == 0)
        {
            continue; // 无数据可用
        }

        if (infos[0].valid_data && samples[0] != NULL)
        {
            ImageDetection_DetectionResult *data = (ImageDetection_DetectionResult *)samples[0];

            // 加锁更新全局数据
            {
                std::lock_guard<std::mutex> lock(global_data.image_mutex);

                // 将接收到的数据复制到global_data中
                global_data.image_data.camera_id = data->camera_id;
                global_data.image_data.object_class = data->object_class;
                global_data.image_data.confidence = data->confidence;
                global_data.image_data.x_min = data->x_min;
                global_data.image_data.y_min = data->y_min;
                global_data.image_data.x_max = data->x_max;
                global_data.image_data.y_max = data->y_max;
                global_data.image_data.return_type = data->return_type;

                // 标记已初始化
                if (!global_data.image_initialized)
                {
                    global_data.image_initialized = true;
                    // 通知主线程
                    global_data.cv.notify_one();
                }
            }
            // 释放样本内存
            ImageDetection_DetectionResult_free(data, DDS_FREE_ALL);
        }
    }

    // 清理资源
    dds_delete(reader);
    dds_delete(topic);
}

// 订阅电机数据的线程函数
void motor_data_subscriber(dds_entity_t participant)
{
    dds_entity_t topic;
    dds_entity_t reader;
    dds_return_t rc;

    // 创建Topic
    topic = dds_create_topic(participant, &MotorData_MotorResult_desc,
                             "MotorDataNode_1", NULL, NULL);
    if (topic < 0)
    {
        std::cerr << "ERROR: MotorDataNode_1 -- Failed to create topic: " << dds_strretcode(-topic) << std::endl;
        return;
    }

    // 创建读取器
    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10));
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);

    reader = dds_create_reader(participant, topic, qos, NULL);
    if (reader < 0)
    {
        std::cerr << "ERROR: MotorDataNode_1 -- Failed to create reader: " << dds_strretcode(-reader) << std::endl;
        dds_delete(topic);
        dds_delete_qos(qos);
        return;
    }
    dds_delete_qos(qos);

    std::cout << "MotorDataNode_1 subscriber ready" << std::endl;

    while (true)
    {
        void *samples[1];
        dds_sample_info_t infos[1];
        // 为sample分配空间
        for (int i = 0; i < 1; i++)
        {
            samples[i] = MotorData_MotorResult__alloc();
        }
        // 阻塞读取数据
        rc = dds_take(reader, samples, infos, 1, 1);
        if (rc < 0)
        {
            std::cerr << "Error: MotorDataNode_1 -- Error reading: " << dds_strretcode(-rc) << std::endl;
            continue;
        }
        else if (rc == 0)
        {
            continue; // 无数据可用
        }

        if (infos[0].valid_data && samples[0] != NULL)
        {
            MotorData_MotorResult *data = (MotorData_MotorResult *)samples[0];

            // 加锁更新全局数据
            {
                std::lock_guard<std::mutex> lock(global_data.motor_mutex);

                // 将接收到的数据复制到global_data中
                global_data.motor_data.motor_id = data->motor_id;
                global_data.motor_data.speed = data->speed;
                global_data.motor_data.temperature = data->temperature;
                global_data.motor_data.status = data->status;
                global_data.motor_data.return_type = data->return_type;

                // 标记已初始化
                if (!global_data.motor_initialized)
                {
                    global_data.motor_initialized = true;
                    // 通知主线程
                    global_data.cv.notify_one();
                }
            }
            // 释放样本内存
            MotorData_MotorResult_free(data, DDS_FREE_ALL);
        }
    }

    // 清理资源
    dds_delete(reader);
    dds_delete(topic);
}

// 订阅雷达数据的线程函数
void radar_data_subscriber(dds_entity_t participant)
{
    dds_entity_t topic;
    dds_entity_t reader;
    dds_return_t rc;

    // 创建Topic
    topic = dds_create_topic(participant, &RadarData_RadarResult_desc,
                             "RadarDataNode_1", NULL, NULL);
    if (topic < 0)
    {
        std::cerr << "ERROR: RadarDataNode_1 -- Failed to create topic: " << dds_strretcode(-topic) << std::endl;
        return;
    }

    // 创建读取器
    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10));
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);

    reader = dds_create_reader(participant, topic, qos, NULL);
    if (reader < 0)
    {
        std::cerr << "ERROR: RadarDataNode_1 -- Failed to create reader: " << dds_strretcode(-reader) << std::endl;
        dds_delete(topic);
        dds_delete_qos(qos);
        return;
    }
    dds_delete_qos(qos);

    std::cout << "RadarDataNode_1 subscriber ready" << std::endl;

    while (true)
    {
        void *samples[1];
        dds_sample_info_t infos[1];
        // 为sample分配空间
        for (int i = 0; i < 1; i++)
        {
            samples[i] = RadarData_RadarResult__alloc();
        }
        // 阻塞读取数据
        rc = dds_take(reader, samples, infos, 1, 1);
        if (rc < 0)
        {
            std::cerr << "Error: RadarDataNode_1 -- Error reading: " << dds_strretcode(-rc) << std::endl;
            continue;
        }
        else if (rc == 0)
        {
            continue; // 无数据可用
        }

        if (infos[0].valid_data && samples[0] != NULL)
        {
            RadarData_RadarResult *data = (RadarData_RadarResult *)samples[0];

            // 加锁更新全局数据
            {
                std::lock_guard<std::mutex> lock(global_data.radar_mutex);

                // 将接收到的数据复制到global_data中
                global_data.radar_data.radar_id = data->radar_id;
                global_data.radar_data.distance = data->distance;
                global_data.radar_data.angle = data->angle;
                global_data.radar_data.velocity = data->velocity;
                global_data.radar_data.target_type = data->target_type;
                global_data.radar_data.return_type = data->return_type;

                // 标记已初始化
                if (!global_data.radar_initialized)
                {
                    global_data.radar_initialized = true;
                    // 通知主线程
                    global_data.cv.notify_one();
                }
            }
            // 释放样本内存
            RadarData_RadarResult_free(data, DDS_FREE_ALL);
        }
    }

    // 清理资源
    dds_delete(reader);
    dds_delete(topic);
}

// 订阅机器人姿态数据的线程函数
void robot_pose_subscriber(dds_entity_t participant)
{
    dds_entity_t topic;
    dds_entity_t reader;
    dds_return_t rc;

    // 创建Topic
    topic = dds_create_topic(participant, &RobotPose_RobotResult_desc,
                             "RobotPoseNode_1", NULL, NULL);
    if (topic < 0)
    {
        std::cerr << "ERROR: RobotPoseNode_1 -- Failed to create topic: " << dds_strretcode(-topic) << std::endl;
        return;
    }

    // 创建读取器
    dds_qos_t *qos = dds_create_qos();
    dds_qset_reliability(qos, DDS_RELIABILITY_RELIABLE, DDS_SECS(10));
    dds_qset_history(qos, DDS_HISTORY_KEEP_LAST, 10);

    reader = dds_create_reader(participant, topic, qos, NULL);
    if (reader < 0)
    {
        std::cerr << "ERROR: RobotPoseNode_1 -- Failed to create reader: " << dds_strretcode(-reader) << std::endl;
        dds_delete(topic);
        dds_delete_qos(qos);
        return;
    }
    dds_delete_qos(qos);

    std::cout << "RobotPoseNode_1 subscriber ready" << std::endl;

    while (true)
    {
        void *samples[1];
        dds_sample_info_t infos[1];
        // 为sample分配空间
        for (int i = 0; i < 1; i++)
        {
            samples[i] = RobotPose_RobotResult__alloc();
        }
        // 阻塞读取数据
        rc = dds_take(reader, samples, infos, 1, 1);
        if (rc < 0)
        {
            std::cerr << "Error: RobotPoseNode_1 -- Error reading: " << dds_strretcode(-rc) << std::endl;
            continue;
        }else if (rc == 0)
        {
            continue; // 无数据可用
        }

        if (infos[0].valid_data && samples[0]!= NULL)
        {
            RobotPose_RobotResult *data = (RobotPose_RobotResult *)samples[0];

            // 加锁更新全局数据
            {
                std::lock_guard<std::mutex> lock(global_data.robot_mutex);

                // 将接收到的数据复制到global_data中
                global_data.robot_data.robot_id = data->robot_id;
                global_data.robot_data.x = data->x;
                global_data.robot_data.y = data->y;
                global_data.robot_data.z = data->z;
                global_data.robot_data.roll = data->roll;
                global_data.robot_data.pitch = data->pitch;
                global_data.robot_data.yaw = data->yaw;
                global_data.robot_data.return_type = data->return_type;

                // 标记已初始化
                if (!global_data.robot_initialized)
                {
                    global_data.robot_initialized = true;
                    // 通知主线程
                    global_data.cv.notify_one();
                }
            }
            // 释放样本内存
            RobotPose_RobotResult_free(data, DDS_FREE_ALL);
        }
    }

    // 清理资源
    dds_delete(reader);
    dds_delete(topic);
}

int main(int argc, char *argv[])
{
    dds_entity_t participant;

    // 1. 创建域参与者
    participant = dds_create_participant(0, NULL, NULL);
    if (participant < 0)
    {
        std::cerr << "ERROR: Failed to create participant: " << dds_strretcode(-participant) << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "EndSubscriber_1 starting..." << std::endl;

    // 2. 创建四个订阅线程
    std::thread image_thread(image_detection_subscriber, participant);
    std::thread motor_thread(motor_data_subscriber, participant);
    std::thread radar_thread(radar_data_subscriber, participant);
    std::thread pose_thread(robot_pose_subscriber, participant);

    // 3. 等待所有子线程收到第一条消息
    {
        std::unique_lock<std::mutex> lock(global_data.cv_mutex);
        global_data.cv.wait(lock, []
                            { return global_data.image_initialized.load() &&
                                     global_data.motor_initialized.load() &&
                                     global_data.radar_initialized.load() &&
                                     global_data.robot_initialized.load(); });
    }

    std::cout << "All subscribers initialized. Starting main loop..." << std::endl;

    // 4. 主循环 - 每2000ms打印一次最新数据
    while (true)
    {
        // 获取当前时间戳
        auto now = std::chrono::system_clock::now();
        auto timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(
                             now.time_since_epoch())
                             .count();

        // 加锁读取全局数据
        std::lock(global_data.image_mutex, global_data.motor_mutex,
                  global_data.radar_mutex, global_data.robot_mutex);

        // 使用lock_guard保证锁会在作用域结束时释放
        std::lock_guard<std::mutex> lock1(global_data.image_mutex, std::adopt_lock);
        std::lock_guard<std::mutex> lock2(global_data.motor_mutex, std::adopt_lock);
        std::lock_guard<std::mutex> lock3(global_data.radar_mutex, std::adopt_lock);
        std::lock_guard<std::mutex> lock4(global_data.robot_mutex, std::adopt_lock);

        // 打印分隔线
        std::cout << "\n=== System Status at " << timestamp << " ===" << std::endl;

        // 打印图像检测数据
        std::cout << "[ImageData] Camera ID: " << global_data.image_data.camera_id << std::endl
                  << ", Object_class: " << global_data.image_data.object_class << std::endl
                  << ", Confidence: " << global_data.image_data.confidence << std::endl
                  << ", X_min: " << global_data.image_data.x_min << std::endl
                  << ", Y_min: " << global_data.image_data.y_min << std::endl
                  << ", X_max: " << global_data.image_data.x_max << std::endl
                  << ", Y_max: " << global_data.image_data.y_max << std::endl;
        std::cout << std::endl;

        // 打印电机数据
        std::cout << "[MotorData] Motor ID: " << global_data.motor_data.motor_id << std::endl
                  << ", Speed: " << global_data.motor_data.speed << std::endl
                  << ", Temperature: " << global_data.motor_data.temperature << std::endl
                  << ", Status: " << global_data.motor_data.status << std::endl;
        std::cout << std::endl;

        // 打印雷达数据
        std::cout << "[RadarData] Radar ID: " << global_data.radar_data.radar_id << std::endl
                  << ", Distance: " << global_data.radar_data.distance << std::endl
                  << ", Angle: " << global_data.radar_data.angle << std::endl
                  << ", Velocity: " << global_data.radar_data.velocity << std::endl
                  << ", Target Type: " << global_data.radar_data.target_type << std::endl;
        std::cout << std::endl;

        // 打印机器人姿态数据
        std::cout << "[RobotPose] Robot ID: " << global_data.robot_data.robot_id << std::endl
                  << ", X: " << global_data.robot_data.x << std::endl
                  << ", Y: " << global_data.robot_data.y << std::endl
                  << ", Z: " << global_data.robot_data.z << std::endl
                  << ", Roll: " << global_data.robot_data.roll << std::endl
                  << ", Pitch: " << global_data.robot_data.pitch << std::endl
                  << ", Yaw: " << global_data.robot_data.yaw << std::endl;
        std::cout << std::endl;

        // 休眠2000ms
        std::this_thread::sleep_for(std::chrono::milliseconds(2000));
    }

    // 理论上不会执行到这里
    image_thread.join();
    motor_thread.join();
    radar_thread.join();
    pose_thread.join();

    dds_delete(participant);
    return EXIT_SUCCESS;
}