#include <cstdlib>
#include <iostream>
#include <chrono>
#include <thread>
#include <vector>
#include <mutex>
#include "dds/dds.hpp"

/* Include data type and specific traits to be used with the C++ DDS API. */
#include "MotorData.hpp"
#include "RobotPose.hpp"
#include "ImageDetection.hpp"
#include "RadarData.hpp"

#include "/usr/local/include/ddscxx/dds/domain/DomainParticipant.hpp"

using namespace org::eclipse::cyclonedds;

// 数据融合的结果存储结构
struct FusionResult {
    std::map<std::string, std::string> data;

    void add(const std::string& key, const std::string& value) {
        data[key] = value;
    }

    void print() const {
        auto now = std::chrono::system_clock::now();
        std::time_t now_time = std::chrono::system_clock::to_time_t(now);

        std::cout << "=== [FusionResult] === (Timestamp: " 
                  << std::put_time(std::localtime(&now_time), "%Y-%m-%d %H:%M:%S") << ")\n";
        for (const auto& [key, value] : data) {
            std::cout << key << ": " << value << "\n";
        }
        std::cout << "======================" << std::endl;
    }
};

template <typename T>
class Subscriber {
public:
    Subscriber(const std::string& topic_name)
        // : participant_(domain::default_id()),
        : participant_(org::eclipse::cyclonedds::domain::default_id()),
          topic_(participant_, topic_name),
          subscriber_(participant_),
          reader_(subscriber_, topic_) {}

    void run(std::function<void(const T&)> callback) {
        try {
            while (true) {
                dds::sub::LoanedSamples<T> samples = reader_.take();
                if (samples.length() > 0) {
                    for (const auto& sample : samples) {
                        if (sample.info().valid()) {
                            callback(sample.data());
                        }
                    }
                } else {
                    std::this_thread::sleep_for(std::chrono::milliseconds(20));
                }
            }
        } catch (const dds::core::Exception& e) {
            std::cerr << "=== [Subscriber] DDS exception: " << e.what() << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "=== [Subscriber] C++ exception: " << e.what() << std::endl;
        }
    }

private:
    dds::domain::DomainParticipant participant_;
    dds::topic::Topic<T> topic_;
    dds::sub::Subscriber subscriber_;
    dds::sub::DataReader<T> reader_;
};

// 数据融合器类
class DataFusion {
public:
    void add_motor_data(const std::string& data) {
        std::lock_guard<std::mutex> lock(mutex_);
        result_.add("MotorData", data);
        check_and_fuse();
    }

    void add_robot_pose(const std::string& data) {
        std::lock_guard<std::mutex> lock(mutex_);
        result_.add("RobotPose", data);
        check_and_fuse();
    }

    void add_image_detection(const std::string& data) {
        std::lock_guard<std::mutex> lock(mutex_);
        result_.add("ImageDetection", data);
        check_and_fuse();
    }

    void add_radar_data(const std::string& data) {
        std::lock_guard<std::mutex> lock(mutex_);
        result_.add("RadarData", data);
        check_and_fuse();
    }

private:
    FusionResult result_;
    FusionResult last_result_; // 上一次的融合结果
    std::mutex mutex_;

    void check_and_fuse() {
        if (result_.data.size() == 4) { // 确保有 4 种数据
            std::lock_guard<std::mutex> lock(mutex_);

            // 检查是否有变化
            if (result_.data != last_result_.data) {
                result_.print(); // 打印结果
                last_result_ = result_; // 更新上一次的结果
            }

            // 清空结果以便下一轮融合
            result_ = FusionResult();
        }
    }
};

int main() {
    DataFusion fusion;

    // 创建四个订阅线程
    std::thread thread_motor([&fusion]() {
        Subscriber<MotorData::MotorStatus> sub("MotorDataTopic");
        sub.run([&fusion](const MotorData::MotorStatus& msg) {
            fusion.add_motor_data("MotorID: " + std::to_string(msg.motor_id()) +
                                  ", Speed: " + std::to_string(msg.speed()) +
                                  ", Temp: " + std::to_string(msg.temperature()));
        });
    });

    std::thread thread_pose([&fusion]() {
        Subscriber<RobotPose::Pose> sub("RobotPoseTopic");
        sub.run([&fusion](const RobotPose::Pose& msg) {
            fusion.add_robot_pose("Pose(X: " + std::to_string(msg.x()) +
                                  ", Y: " + std::to_string(msg.y()) +
                                  ", Z: " + std::to_string(msg.z()) + ")");
        });
    });

    std::thread thread_image([&fusion]() {
        Subscriber<ImageDetection::DetectionResult> sub("ImageDetectionTopic");
        sub.run([&fusion](const ImageDetection::DetectionResult& msg) {
            fusion.add_image_detection("Object: " + msg.object_class() +
                                       ", Confidence: " + std::to_string(msg.confidence()));
        });
    });

    std::thread thread_radar([&fusion]() {
        Subscriber<RadarData::RadarScan> sub("RadarDataTopic");
        sub.run([&fusion](const RadarData::RadarScan& msg) {
            fusion.add_radar_data("Distance: " + std::to_string(msg.distance()) +
                                  ", Angle: " + std::to_string(msg.angle()) +
                                  ", Velocity: " + std::to_string(msg.velocity()));
        });
    });

    // 等待线程结束（实际上不会结束） 
    thread_motor.join();
    thread_pose.join();
    thread_image.join();
    thread_radar.join();

    return EXIT_SUCCESS;
}