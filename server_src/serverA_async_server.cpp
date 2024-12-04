#include <iostream>
#include <fstream>
#include <thread>
#include <chrono>
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include <netdb.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <nlohmann/json.hpp>

#include <grpcpp/grpcpp.h>
#include <grpc/support/log.h>

using grpc::Server;
using grpc::ServerAsyncResponseWriter;
using grpc::ServerBuilder;
using grpc::ServerCompletionQueue;
using grpc::ServerContext;
using grpc::Status;

#include <nlohmann/json.hpp>
using json = nlohmann::json;

#include "../rpc_server_inc/atomic_service_mbsb_impl.h"

#include "../rpc_server_inc/atomic_service_sf_impl.h"

class atomic_service_mbsb_Service_ServerImpl;

class atomic_service_sf_Service_ServerImpl;

// 统计数字位数
int getDigit(int number)
{
    int count = 0;
    while (number != 0)
    {
        number /= 10;
        count++;
    }
    return count;
}

// 更新字符数
int updateNumber(int number)
{
    int i = number;
    i = i + getDigit(i);
    i -= 1;
    return i;
}

void monitorComm(const std::string &broadcastAddress, const int port)
{
    int sock;
    struct sockaddr_in sockertaddr;
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

    // 构造注册信息
    json registry_json;
    json header;
    header["protocol_identifier"] = 22;
    header["send_time"] = time(NULL);
    header["message_length"] = 1;
    header["message_serial_number"] = 1;
    header["check_bit"] = 4;
    header["type"] = 1;
    registry_json["header"] = header;
    registry_json["server_name"] = "serverA";
    registry_json["address"] = "0.0.0.0";
    registry_json["port"] = 50051;

    json registry_services_list = json::array();

    registry_services_list.push_back({{"service_name", "atomic_service_mbsb"}, {"role", 1}});

    registry_services_list.push_back({{"service_name", "atomic_service_sf"}, {"role", 1}});

    registry_json["services_list"] = registry_services_list;
    std::string registry_str = registry_json.dump();
    header["message_length"] = updateNumber(registry_str.size());
    registry_str = registry_json.dump();
    // 发送注册报文到广播地址
    if (sendto(sock, registry_str.c_str(), registry_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0)
    {
        close(sock);
        exit(EXIT_FAILURE);
    }

    // 构造元数据信息
    json metadata_registry_json;
    header["protocol_identifier"] = 22;
    header["send_time"] = time(NULL);
    header["message_length"] = 1;
    header["message_serial_number"] = 1;
    header["check_bit"] = 4;
    header["type"] = 3;
    metadata_registry_json["header"] = header;
    metadata_registry_json["server_name"] = "serverA";
    metadata_registry_json["address"] = "0.0.0.0";
    metadata_registry_json["port"] = 50051;
    json metadata_registry_services_list = json::array();

    metadata_registry_services_list.push_back({{"metadata", {{"version", "V1.0.0"}, {"decription", ""}, {"developer", "Spiderman"}, {"build_time", "2024-09-21T09-21-21"}}}, {"service_name", "atomic_service_mbsb"}, {"card", "atlas"}, {"os", "openeuler"}});

    metadata_registry_services_list.push_back({{"metadata", {{"version", "V1.0.2"}, {"decription", ""}, {"developer", "yishui"}, {"build_time", "2024-09-30T09-21-21"}}}, {"service_name", "atomic_service_sf"}, {"card", "atlas"}, {"os", "openeuler"}});

    metadata_registry_json["services_list"] = metadata_registry_services_list;
    std::string metadata_registry_str = metadata_registry_json.dump();
    header["message_length"] = updateNumber(metadata_registry_str.size());
    metadata_registry_str = metadata_registry_json.dump();
    // 发送注册报文到广播地址
    if (sendto(sock, metadata_registry_str.c_str(), metadata_registry_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0)
    {
        close(sock);
        exit(EXIT_FAILURE);
    }

    // 构造心跳信息
    json heartbeat_json;
    json heartbeat_services_list;
    while (1)
    {
        // 无限循环，每30秒发送一次
        header["protocol_identifier"] = 22;
        header["send_time"] = time(NULL);
        header["message_length"] = 1;
        header["message_serial_number"] = 1;
        header["check_bit"] = 4;
        header["type"] = 7;
        heartbeat_json["header"] = header;
        heartbeat_json["server_name"] = "serverA";
        heartbeat_json["address"] = "0.0.0.0";
        heartbeat_json["port"] = 50051;
        heartbeat_services_list = json::array();

        heartbeat_services_list.push_back({{"service_name", "atomic_service_mbsb"}, {"role", 1}});

        heartbeat_services_list.push_back({{"service_name", "atomic_service_sf"}, {"role", 1}});

        registry_json["services_list"] = metadata_registry_services_list;
        std::string heartbeat_str = heartbeat_json.dump();
        header["message_length"] = updateNumber(heartbeat_str.size());
        heartbeat_str = heartbeat_json.dump();
        // 发送注册报文到广播地址
        if (sendto(sock, heartbeat_str.c_str(), heartbeat_str.size(), 0, (struct sockaddr *)&sockertaddr, sizeof(sockertaddr)) < 0)
        {
            close(sock);
            exit(EXIT_FAILURE);
        }

        sleep(30);
    }

    // 关闭socket
    close(sock);
}

/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Async_server_class BEGIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
class AsyncServerImpl final
{
private:
    std::string ip;
    std::string port;

public:
    AsyncServerImpl(std::string ip, std::string port) : ip(ip), port(port) {}
    ~AsyncServerImpl()
    {
        server_->Shutdown();
        // Always shutdown the completion queue after the server.

        atomic_service_mbsb_atomic_service_fun_task_A_cq_->Shutdown();

        atomic_service_mbsb_atomic_service_fun_task_B_cq_->Shutdown();

        atomic_service_sf_atomic_service_fun_task_C_cq_->Shutdown();

        atomic_service_sf_atomic_service_fun_task_D_cq_->Shutdown();
    }
#if 1
    // There is no shutdown handling in this code.
    void Run()
    {
        std::string server_address(ip + ":" + port);
        ServerBuilder builder;
        builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
        /* TODO: Add other services */

        builder.RegisterService(&atomic_service_mbsb_atomic_service_fun_task_A_service_);
        atomic_service_mbsb_atomic_service_fun_task_A_cq_ = builder.AddCompletionQueue();

        builder.RegisterService(&atomic_service_mbsb_atomic_service_fun_task_B_service_);
        atomic_service_mbsb_atomic_service_fun_task_B_cq_ = builder.AddCompletionQueue();

        builder.RegisterService(&atomic_service_sf_atomic_service_fun_task_C_service_);
        atomic_service_sf_atomic_service_fun_task_C_cq_ = builder.AddCompletionQueue();

        builder.RegisterService(&atomic_service_sf_atomic_service_fun_task_D_service_);
        atomic_service_sf_atomic_service_fun_task_D_cq_ = builder.AddCompletionQueue();

        // Finally assemble the server.
        server_ = builder.BuildAndStart();
        std::cout << "Server listening on " << server_address << std::endl;
    }
#endif

    //-----> Step1 Class encompasing the state and logic needed to serve a request.
private:
    /* CallData class atomic_service_mbsb_atomic_service_fun_task_A_CallData  BEGIN */
    class atomic_service_mbsb_atomic_service_fun_task_A_CallData
    {
    public:
        atomic_service_mbsb_atomic_service_fun_task_A_CallData(atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_mbsb_atomic_service_fun_task_A_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_mbsb_atomic_service_fun_task_A_service_->Requestatomic_service_fun_task_A(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_mbsb_atomic_service_fun_task_A_CallData(atomic_service_mbsb_atomic_service_fun_task_A_service_, cq_);
                // The actual processing.
                /*TODO: */
                atomic_service_mbsb_task_A_Request_st atomic_service_mbsb_Request_t;
                atomic_service_mbsb_task_A_Reply_st atomic_service_mbsb_Reply_t;

                atomic_service_mbsb_Request_t.number1 = request_.number1();

                atomic_service_mbsb_Request_t.number2 = request_.number2();

                /******************************************************************/
                atomic_service_fun_task_A_func(&atomic_service_mbsb_Request_t, &atomic_service_mbsb_Reply_t);

                /******************************************************************/

                reply_.Clear(); // clear reply message

                reply_.set_sum_result(atomic_service_mbsb_Reply_t.sum_result);

                reply_.set_return_type(atomic_service_mbsb_Reply_t.return_type);

                std::cout << "This is Method = atomic_service_fun_task_A, ServiceName=atomic_service_mbsb" << std::endl;
                // return grpc::Status::OK;

                status_ = FINISH;
                responder_.Finish(reply_, Status::OK, this);
            }
            else
            {
                GPR_ASSERT(status_ == FINISH);
                delete this;
            }
        }

    private:
        atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService *atomic_service_mbsb_atomic_service_fun_task_A_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_mbsb_Package::atomic_service_mbsb_task_A_Request_st request_;
        atomic_service_mbsb_Package::atomic_service_mbsb_task_A_Reply_st reply_;
        ServerAsyncResponseWriter<atomic_service_mbsb_Package::atomic_service_mbsb_task_A_Reply_st> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_mbsb_CallData  END */

    /* CallData class atomic_service_mbsb_atomic_service_fun_task_B_CallData  BEGIN */
    class atomic_service_mbsb_atomic_service_fun_task_B_CallData
    {
    public:
        atomic_service_mbsb_atomic_service_fun_task_B_CallData(atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_mbsb_atomic_service_fun_task_B_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_mbsb_atomic_service_fun_task_B_service_->Requestatomic_service_fun_task_B(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_mbsb_atomic_service_fun_task_B_CallData(atomic_service_mbsb_atomic_service_fun_task_B_service_, cq_);
                // The actual processing.
                /*TODO: */
                atomic_service_mbsb_task_B_Request_st atomic_service_mbsb_Request_t;
                atomic_service_mbsb_task_B_Reply_st atomic_service_mbsb_Reply_t;

                atomic_service_mbsb_Request_t.number1 = request_.number1();

                atomic_service_mbsb_Request_t.number2 = request_.number2();

                /******************************************************************/
                atomic_service_fun_task_B_func(&atomic_service_mbsb_Request_t, &atomic_service_mbsb_Reply_t);

                /******************************************************************/

                reply_.Clear(); // clear reply message

                reply_.set_sub_result(atomic_service_mbsb_Reply_t.sub_result);

                reply_.set_return_type(atomic_service_mbsb_Reply_t.return_type);

                std::cout << "This is Method = atomic_service_fun_task_B, ServiceName=atomic_service_mbsb" << std::endl;
                // return grpc::Status::OK;

                status_ = FINISH;
                responder_.Finish(reply_, Status::OK, this);
            }
            else
            {
                GPR_ASSERT(status_ == FINISH);
                delete this;
            }
        }

    private:
        atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService *atomic_service_mbsb_atomic_service_fun_task_B_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_mbsb_Package::atomic_service_mbsb_task_B_Request_st request_;
        atomic_service_mbsb_Package::atomic_service_mbsb_task_B_Reply_st reply_;
        ServerAsyncResponseWriter<atomic_service_mbsb_Package::atomic_service_mbsb_task_B_Reply_st> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_mbsb_CallData  END */

    /* CallData class atomic_service_sf_atomic_service_fun_task_C_CallData  BEGIN */
    class atomic_service_sf_atomic_service_fun_task_C_CallData
    {
    public:
        atomic_service_sf_atomic_service_fun_task_C_CallData(atomic_service_sf_Package::atomic_service_sf_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_sf_atomic_service_fun_task_C_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_sf_atomic_service_fun_task_C_service_->Requestatomic_service_fun_task_C(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_sf_atomic_service_fun_task_C_CallData(atomic_service_sf_atomic_service_fun_task_C_service_, cq_);
                // The actual processing.
                /*TODO: */
                atomic_service_sf_task_C_Request_st atomic_service_sf_Request_t;
                atomic_service_sf_task_C_Reply_st atomic_service_sf_Reply_t;

                atomic_service_sf_Request_t.name = request_.name();

                atomic_service_sf_Request_t.title = request_.title();

                /******************************************************************/
                atomic_service_fun_task_C_func(&atomic_service_sf_Request_t, &atomic_service_sf_Reply_t);

                /******************************************************************/

                reply_.Clear(); // clear reply message

                reply_.set_result(atomic_service_sf_Reply_t.result);

                reply_.set_return_type(atomic_service_sf_Reply_t.return_type);

                std::cout << "This is Method = atomic_service_fun_task_C, ServiceName=atomic_service_sf" << std::endl;
                // return grpc::Status::OK;

                status_ = FINISH;
                responder_.Finish(reply_, Status::OK, this);
            }
            else
            {
                GPR_ASSERT(status_ == FINISH);
                delete this;
            }
        }

    private:
        atomic_service_sf_Package::atomic_service_sf_Service::AsyncService *atomic_service_sf_atomic_service_fun_task_C_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_sf_Package::atomic_service_sf_task_C_Request_st request_;
        atomic_service_sf_Package::atomic_service_sf_task_C_Reply_st reply_;
        ServerAsyncResponseWriter<atomic_service_sf_Package::atomic_service_sf_task_C_Reply_st> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_sf_CallData  END */

    /* CallData class atomic_service_sf_atomic_service_fun_task_D_CallData  BEGIN */
    class atomic_service_sf_atomic_service_fun_task_D_CallData
    {
    public:
        atomic_service_sf_atomic_service_fun_task_D_CallData(atomic_service_sf_Package::atomic_service_sf_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_sf_atomic_service_fun_task_D_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_sf_atomic_service_fun_task_D_service_->Requestatomic_service_fun_task_D(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_sf_atomic_service_fun_task_D_CallData(atomic_service_sf_atomic_service_fun_task_D_service_, cq_);
                // The actual processing.
                /*TODO: */
                atomic_service_sf_task_D_Request_st atomic_service_sf_Request_t;
                atomic_service_sf_task_D_Reply_st atomic_service_sf_Reply_t;

                for (int i = 0; i < request_.int_array_size(); ++i)
                {
                    atomic_service_sf_Request_t.int_array.push_back(request_.int_array(i));
                }

                /******************************************************************/
                atomic_service_fun_task_D_func(&atomic_service_sf_Request_t, &atomic_service_sf_Reply_t);

                /******************************************************************/

                reply_.Clear(); // clear reply message

                for (const auto &item : atomic_service_sf_Reply_t.string_int_map_reply)
                {
                    reply_.mutable_string_int_map_reply()->insert({item.first, item.second});
                }

                reply_.set_return_type(atomic_service_sf_Reply_t.return_type);

                std::cout << "This is Method = atomic_service_fun_task_D, ServiceName=atomic_service_sf" << std::endl;
                // return grpc::Status::OK;

                status_ = FINISH;
                responder_.Finish(reply_, Status::OK, this);
            }
            else
            {
                GPR_ASSERT(status_ == FINISH);
                delete this;
            }
        }

    private:
        atomic_service_sf_Package::atomic_service_sf_Service::AsyncService *atomic_service_sf_atomic_service_fun_task_D_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_sf_Package::atomic_service_sf_task_D_Request_st request_;
        atomic_service_sf_Package::atomic_service_sf_task_D_Reply_st reply_;
        ServerAsyncResponseWriter<atomic_service_sf_Package::atomic_service_sf_task_D_Reply_st> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_sf_CallData  END */

    //-----> Step2 This can be run in multiple threads if needed.
public:
    void atomic_service_mbsb_atomic_service_fun_task_A_HandleRpcs()
    {
        new atomic_service_mbsb_atomic_service_fun_task_A_CallData(&atomic_service_mbsb_atomic_service_fun_task_A_service_, atomic_service_mbsb_atomic_service_fun_task_A_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_mbsb_atomic_service_fun_task_A_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_mbsb_atomic_service_fun_task_A_CallData *>(tag)->Proceed();
        }
    }

    void atomic_service_mbsb_atomic_service_fun_task_B_HandleRpcs()
    {
        new atomic_service_mbsb_atomic_service_fun_task_B_CallData(&atomic_service_mbsb_atomic_service_fun_task_B_service_, atomic_service_mbsb_atomic_service_fun_task_B_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_mbsb_atomic_service_fun_task_B_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_mbsb_atomic_service_fun_task_B_CallData *>(tag)->Proceed();
        }
    }

    void atomic_service_sf_atomic_service_fun_task_C_HandleRpcs()
    {
        new atomic_service_sf_atomic_service_fun_task_C_CallData(&atomic_service_sf_atomic_service_fun_task_C_service_, atomic_service_sf_atomic_service_fun_task_C_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_sf_atomic_service_fun_task_C_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_sf_atomic_service_fun_task_C_CallData *>(tag)->Proceed();
        }
    }

    void atomic_service_sf_atomic_service_fun_task_D_HandleRpcs()
    {
        new atomic_service_sf_atomic_service_fun_task_D_CallData(&atomic_service_sf_atomic_service_fun_task_D_service_, atomic_service_sf_atomic_service_fun_task_D_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_sf_atomic_service_fun_task_D_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_sf_atomic_service_fun_task_D_CallData *>(tag)->Proceed();
        }
    }

    /* class var */
private:
    std::unique_ptr<Server> server_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_mbsb_atomic_service_fun_task_A_cq_;
    atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService atomic_service_mbsb_atomic_service_fun_task_A_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_mbsb_atomic_service_fun_task_B_cq_;
    atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService atomic_service_mbsb_atomic_service_fun_task_B_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_sf_atomic_service_fun_task_C_cq_;
    atomic_service_sf_Package::atomic_service_sf_Service::AsyncService atomic_service_sf_atomic_service_fun_task_C_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_sf_atomic_service_fun_task_D_cq_;
    atomic_service_sf_Package::atomic_service_sf_Service::AsyncService atomic_service_sf_atomic_service_fun_task_D_service_;
};

/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Async_server_class END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
int main(int argc, char **argv)
{

    std::string ip = "0.0.0.0";
    std::string port = "50051";
    std::string broadcastAddress = "255.255.255.255"; // Default broadcast addressIP "192.168.0.255"
    std::string broadcastPort = "8888";               // Default broadcast port

    std::cout << ">>>>[INFO] Server IP: " << ip << std::endl;
    std::cout << ">>>>[INFO] Server Port: " << port << std::endl;
    std::cout << ">>>>[INFO] Broadcast Address: " << broadcastAddress << std::endl;
    std::cout << ">>>>[INFO] Broadcast Port: " << broadcastPort << std::endl;

    /* Create AsyncServerImpl BEGIN */
    AsyncServerImpl serverPersonal(ip, port);
    serverPersonal.Run();

    std::thread atomic_service_mbsb_atomic_service_fun_task_A_thread(&AsyncServerImpl::atomic_service_mbsb_atomic_service_fun_task_A_HandleRpcs, &serverPersonal);

    std::thread atomic_service_mbsb_atomic_service_fun_task_B_thread(&AsyncServerImpl::atomic_service_mbsb_atomic_service_fun_task_B_HandleRpcs, &serverPersonal);

    std::thread atomic_service_sf_atomic_service_fun_task_C_thread(&AsyncServerImpl::atomic_service_sf_atomic_service_fun_task_C_HandleRpcs, &serverPersonal);

    std::thread atomic_service_sf_atomic_service_fun_task_D_thread(&AsyncServerImpl::atomic_service_sf_atomic_service_fun_task_D_HandleRpcs, &serverPersonal);

    std::thread senderThread(monitorComm, broadcastAddress, std::stoi(broadcastPort));

    atomic_service_mbsb_atomic_service_fun_task_A_thread.join();

    atomic_service_mbsb_atomic_service_fun_task_B_thread.join();

    atomic_service_sf_atomic_service_fun_task_C_thread.join();

    atomic_service_sf_atomic_service_fun_task_D_thread.join();

    /* Create AsyncServerImpl END */

    senderThread.join();

    return 0;
}