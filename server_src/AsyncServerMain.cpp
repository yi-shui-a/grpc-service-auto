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

#include "../rpc_server_inc/atomic_service_sfzt_impl.h"
#include "../atom_inc/atomic_service_sfzt.h"

#include "../rpc_server_inc/atomic_service_skzt_impl.h"
#include "../atom_inc/atomic_service_skzt.h"

#include "../rpc_server_inc/atomic_service_mbsb_impl.h"
#include "../atom_inc/atomic_service_mbsb.h"

#include "../rpc_server_inc/atomic_service_sj_impl.h"
#include "../atom_inc/atomic_service_sj.h"

#include "../rpc_server_inc/atomic_service_st_impl.h"
#include "../atom_inc/atomic_service_st.h"

using json = nlohmann::json;

void loadConfig(const std::string &filename, std::string &ip, std::string &port,
                std::string &broadcastAddress, std::string &broadcastPort)
{
    std::ifstream config_file(filename);
    if (!config_file.is_open())
    {
        std::cerr << "Failed to open configuration file: " << filename << std::endl;
        return;
    }
    try
    {
        json config = json::parse(config_file);
        ip = config["server"]["ip"].get<std::string>();
        port = config["server"]["port"].get<std::string>();
        broadcastAddress = config["server"]["broadcastAddress"].get<std::string>();
        broadcastPort = config["server"]["broadcastPort"].get<std::string>();
    }
    catch (const json::parse_error &e)
    {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
    }
    catch (const json::type_error &e)
    {
        std::cerr << "JSON type error: " << e.what() << std::endl;
    }
    catch (...)
    {
        std::cerr << "An unexpected error occurred while parsing the JSON file." << std::endl;
    }
}

void createSystemStatusJson(json &js)
{
    js["system_version"] = "1.0";
    js["architecture"] = "x86_64";
    // other system_Status_info...
    js["memory_usage"] = "10086";
    js["network_usage"] = "11111";
    js["answer"]["everything"] = "Ubuntu20.04";
    js["object"] = {{"currency", "USD"}, {"value", 42.99}};
}

void udpSender(const char *server_host, const char *server_port)
{
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        std::cerr << "Cannot open socket: " << strerror(errno) << std::endl;
        return;
    }
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(atoi(server_port));

    if (inet_pton(AF_INET, server_host, &serv_addr.sin_addr) <= 0)
    {
        std::cerr << "Invalid address / Address not supported: " << strerror(errno) << std::endl;
        close(sockfd);
        return;
    }
    json j;
    createSystemStatusJson(j);
    while (true)
    {
        sendto(sockfd, j.dump().c_str(), j.dump().length(), 0,
               (const struct sockaddr *)&serv_addr, sizeof(serv_addr));
        std::this_thread::sleep_for(std::chrono::seconds(1)); // sleep for 1 second
    }
    close(sockfd);
}

void udpReceiver(uint16_t listen_port)
{
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        std::cerr << "Cannot open socket: " << strerror(errno) << std::endl;
        return;
    }
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(listen_port);
    if (bind(sockfd, (const struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        std::cerr << "Cannot bind socket: " << strerror(errno) << std::endl;
        close(sockfd);
        return;
    }
    char buffer[1024];
    socklen_t len = sizeof(serv_addr);
    while (true)
    {
        ssize_t byte_read = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                                     (struct sockaddr *)&serv_addr, &len);
        if (byte_read > 0)
        {
            // handle received data
            std::cout << "Received data: " << std::string(buffer, byte_read) << std::endl;
        }
    }
    close(sockfd);
}

nlohmann::json readJsonDataFromFile(const std::string &file_path)
{
    std::ifstream json_file(file_path);
    if (!json_file.is_open())
    {
        throw std::runtime_error("Cannot open JSON file");
    }
    nlohmann::json j;
    json_file >> j;
    return j;
}

nlohmann::json readJsonFile(const std::string &filename)
{
    std::ifstream jsonFile(filename);
    if (!jsonFile.is_open())
    {
        throw std::runtime_error("Cannot open file: " + filename);
    }

    try
    {
        nlohmann::json j;
        jsonFile >> j;
        return j;
    }
    catch (const json::parse_error &pe)
    {
        std::cerr << "JSON parse error: " << pe.what() << std::endl;
        throw;
    }
}

void broadcastStructData(const std::string &broadcastIP, const std::string &broadcastPort)
{

    const char *broadcastMessage = R"({"message": "Hello, broadcast!", "time": "2024-08-18T17:10:00Z"})";
    // const char *broadcastIP = "255.255.255.255";
    // int broadcastPort = 12345;

    // Create a UDP socket
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1)
    {
        std::cerr << "Error creating socket" << std::endl;
        return;
    }
    // Set the broadcast option
    int broadcastPermission = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcastPermission, sizeof(broadcastPermission)) == -1)
    {
        std::cerr << "Error setting broadcast option" << std::endl;
        close(sock);
        return;
    }
    // Prepare the address structure
    struct sockaddr_in broadcastAddr;
    memset(&broadcastAddr, 0, sizeof(broadcastAddr));
    broadcastAddr.sin_family = AF_INET;
    broadcastAddr.sin_port = htons(atoi(broadcastPort.c_str()));
    if (inet_aton(broadcastIP.c_str(), &broadcastAddr.sin_addr) == 0)
    {
        std::cerr << "Invalid broadcast IP address" << std::endl;
        close(sock);
        return;
    }
    // Send the broadcast message
    while (true)
    {
        if (sendto(sock, broadcastMessage, strlen(broadcastMessage), 0,
                   (struct sockaddr *)&broadcastAddr, sizeof(broadcastAddr)) == -1)
        {
            std::cerr << "Error sending broadcast message" << std::endl;
            close(sock);
            return;
        }
        std::cout << "Broadcast message sent successfully." << std::endl;
    }
    close(sock);
}

void broadcastJsonData(const std::string &broadcastAddress, const std::string &port, const nlohmann::json &j)
{
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
    {
        std::cerr << "Cannot open socket" << std::endl;
        return;
    }
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(atoi(port.c_str()));
    inet_pton(AF_INET, broadcastAddress.c_str(), &serv_addr.sin_addr);

    int opt = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &opt, sizeof(opt)))
    {
        perror("setsockopt");
        close(sockfd);
        return;
    }

    const std::string message = j.dump();
    while (true)
    {
        if (sendto(sockfd, message.c_str(), message.size(), 0,
                   (const struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
        {
            perror("sendto");
        }
        // std::cout << "Broadcast JSON data: " << message << std::endl;
        std::cout << "Broadcast JSON data Successfully...... " << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1)); // sleep for 1 second
    }
}
/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Async_server_class BEGAIN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
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

        atomic_service_sfzt_cq_->Shutdown();

        atomic_service_skzt_cq_->Shutdown();

        atomic_service_mbsb_cq_->Shutdown();

        atomic_service_sj_cq_->Shutdown();

        atomic_service_st_cq_->Shutdown();
    }
#if 1
    // There is no shutdown handling in this code.
    void Run()
    {
        std::string server_address(ip + ":" + port);
        ServerBuilder builder;
        builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
        /* TODO: Add other services */

        builder.RegisterService(&atomic_service_sfzt_service_);
        atomic_service_sfzt_cq_ = builder.AddCompletionQueue();

        builder.RegisterService(&atomic_service_skzt_service_);
        atomic_service_skzt_cq_ = builder.AddCompletionQueue();

        builder.RegisterService(&atomic_service_mbsb_service_);
        atomic_service_mbsb_cq_ = builder.AddCompletionQueue();

        builder.RegisterService(&atomic_service_sj_service_);
        atomic_service_sj_cq_ = builder.AddCompletionQueue();

        builder.RegisterService(&atomic_service_st_service_);
        atomic_service_st_cq_ = builder.AddCompletionQueue();

        // Finally assemble the server.
        server_ = builder.BuildAndStart();
        std::cout << "Server listening on " << server_address << std::endl;
    }
#endif

    //-----> Step1 Class encompasing the state and logic needed to serve a request.
private:
    /* CallData class atomic_service_sfzt_CallData  BEGAIN */
    class atomic_service_sfzt_CallData
    {
    public:
        atomic_service_sfzt_CallData(atomic_service_sfzt_Package::atomic_service_sfzt_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_sfzt_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_sfzt_service_->RequestUnitaryStream(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_sfzt_CallData(atomic_service_sfzt_service_, cq_);
                // The actual processing.
                /*TODO: */
                // std::string prefix("Hello atomic_service_sfzt ");
                // reply_.set_message(prefix + request_.name());

                atomic_service_sfzt_Request_st atomic_service_sfzt_Request_t;
                atomic_service_sfzt_Reply_st atomic_service_sfzt_Reply_t;

                atomic_service_sfzt_Request_t.name = request_.name();

                atomic_service_sfzt_Request_t.integer_field = request_.integer_field();

                atomic_service_sfzt_Request_t.double_field = request_.double_field();

                atomic_service_sfzt_Request_t.float_field = request_.float_field();

                for (int i = 0; i < request_.int_array_size(); ++i)
                {
                    atomic_service_sfzt_Request_t.int_array.push_back(request_.int_array(i));
                }

                for (const auto &item : request_.string_int_map())
                {
                    atomic_service_sfzt_Request_t.string_int_map[item.first] = item.second;
                }

                /******************************************************************/
                atomic_service_sfzt_interface(&atomic_service_sfzt_Request_t, &atomic_service_sfzt_Reply_t);

                /******************************************************************/
                reply_.Clear(); // clear reply message

                reply_.set_message(atomic_service_sfzt_Reply_t.message);

                reply_.set_integer_reply(atomic_service_sfzt_Reply_t.integer_reply);

                reply_.set_double_reply(atomic_service_sfzt_Reply_t.double_reply);

                reply_.set_float_reply(atomic_service_sfzt_Reply_t.float_reply);

                for (int i = 0; i < atomic_service_sfzt_Reply_t.int_array_reply.size(); ++i)
                {
                    reply_.mutable_int_array_reply()->Add(atomic_service_sfzt_Reply_t.int_array_reply[i]);
                }

                for (const auto &item : atomic_service_sfzt_Reply_t.string_int_map_reply)
                {
                    reply_.mutable_string_int_map_reply()->insert({item.first, item.second});
                }

                std::cout << "This is Method = UnitaryStream ServiceName=atomic_service_sfzt_Service" << std::endl;
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
        atomic_service_sfzt_Package::atomic_service_sfzt_Service::AsyncService *atomic_service_sfzt_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_sfzt_Package::atomic_service_sfzt_Request request_;
        atomic_service_sfzt_Package::atomic_service_sfzt_Reply reply_;
        ServerAsyncResponseWriter<atomic_service_sfzt_Package::atomic_service_sfzt_Reply> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_sfzt_CallData  END */

    /* CallData class atomic_service_skzt_CallData  BEGAIN */
    class atomic_service_skzt_CallData
    {
    public:
        atomic_service_skzt_CallData(atomic_service_skzt_Package::atomic_service_skzt_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_skzt_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_skzt_service_->RequestUnitaryStream(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_skzt_CallData(atomic_service_skzt_service_, cq_);
                // The actual processing.
                /*TODO: */
                // std::string prefix("Hello atomic_service_skzt ");
                // reply_.set_message(prefix + request_.name());

                atomic_service_skzt_Request_st atomic_service_skzt_Request_t;
                atomic_service_skzt_Reply_st atomic_service_skzt_Reply_t;

                atomic_service_skzt_Request_t.name = request_.name();

                atomic_service_skzt_Request_t.integer_field = request_.integer_field();

                atomic_service_skzt_Request_t.double_field = request_.double_field();

                atomic_service_skzt_Request_t.float_field = request_.float_field();

                for (int i = 0; i < request_.int_array_size(); ++i)
                {
                    atomic_service_skzt_Request_t.int_array.push_back(request_.int_array(i));
                }

                for (const auto &item : request_.string_int_map())
                {
                    atomic_service_skzt_Request_t.string_int_map[item.first] = item.second;
                }

                /******************************************************************/
                atomic_service_skzt_interface(&atomic_service_skzt_Request_t, &atomic_service_skzt_Reply_t);

                /******************************************************************/
                reply_.Clear(); // clear reply message

                reply_.set_message(atomic_service_skzt_Reply_t.message);

                reply_.set_integer_reply(atomic_service_skzt_Reply_t.integer_reply);

                reply_.set_double_reply(atomic_service_skzt_Reply_t.double_reply);

                reply_.set_float_reply(atomic_service_skzt_Reply_t.float_reply);

                for (int i = 0; i < atomic_service_skzt_Reply_t.int_array_reply.size(); ++i)
                {
                    reply_.mutable_int_array_reply()->Add(atomic_service_skzt_Reply_t.int_array_reply[i]);
                }

                for (const auto &item : atomic_service_skzt_Reply_t.string_int_map_reply)
                {
                    reply_.mutable_string_int_map_reply()->insert({item.first, item.second});
                }

                std::cout << "This is Method = UnitaryStream ServiceName=atomic_service_skzt_Service" << std::endl;
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
        atomic_service_skzt_Package::atomic_service_skzt_Service::AsyncService *atomic_service_skzt_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_skzt_Package::atomic_service_skzt_Request request_;
        atomic_service_skzt_Package::atomic_service_skzt_Reply reply_;
        ServerAsyncResponseWriter<atomic_service_skzt_Package::atomic_service_skzt_Reply> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_skzt_CallData  END */

    /* CallData class atomic_service_mbsb_CallData  BEGAIN */
    class atomic_service_mbsb_CallData
    {
    public:
        atomic_service_mbsb_CallData(atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_mbsb_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_mbsb_service_->RequestUnitaryStream(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_mbsb_CallData(atomic_service_mbsb_service_, cq_);
                // The actual processing.
                /*TODO: */
                // std::string prefix("Hello atomic_service_mbsb ");
                // reply_.set_message(prefix + request_.name());

                atomic_service_mbsb_Request_st atomic_service_mbsb_Request_t;
                atomic_service_mbsb_Reply_st atomic_service_mbsb_Reply_t;

                atomic_service_mbsb_Request_t.name = request_.name();

                atomic_service_mbsb_Request_t.integer_field = request_.integer_field();

                atomic_service_mbsb_Request_t.double_field = request_.double_field();

                atomic_service_mbsb_Request_t.float_field = request_.float_field();

                for (int i = 0; i < request_.int_array_size(); ++i)
                {
                    atomic_service_mbsb_Request_t.int_array.push_back(request_.int_array(i));
                }

                for (const auto &item : request_.string_int_map())
                {
                    atomic_service_mbsb_Request_t.string_int_map[item.first] = item.second;
                }

                /******************************************************************/
                atomic_service_mbsb_interface(&atomic_service_mbsb_Request_t, &atomic_service_mbsb_Reply_t);

                /******************************************************************/
                reply_.Clear(); // clear reply message

                reply_.set_message(atomic_service_mbsb_Reply_t.message);

                reply_.set_integer_reply(atomic_service_mbsb_Reply_t.integer_reply);

                reply_.set_double_reply(atomic_service_mbsb_Reply_t.double_reply);

                reply_.set_float_reply(atomic_service_mbsb_Reply_t.float_reply);

                for (int i = 0; i < atomic_service_mbsb_Reply_t.int_array_reply.size(); ++i)
                {
                    reply_.mutable_int_array_reply()->Add(atomic_service_mbsb_Reply_t.int_array_reply[i]);
                }

                for (const auto &item : atomic_service_mbsb_Reply_t.string_int_map_reply)
                {
                    reply_.mutable_string_int_map_reply()->insert({item.first, item.second});
                }

                std::cout << "This is Method = UnitaryStream ServiceName=atomic_service_mbsb_Service" << std::endl;
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
        atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService *atomic_service_mbsb_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_mbsb_Package::atomic_service_mbsb_Request request_;
        atomic_service_mbsb_Package::atomic_service_mbsb_Reply reply_;
        ServerAsyncResponseWriter<atomic_service_mbsb_Package::atomic_service_mbsb_Reply> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_mbsb_CallData  END */

    /* CallData class atomic_service_sj_CallData  BEGAIN */
    class atomic_service_sj_CallData
    {
    public:
        atomic_service_sj_CallData(atomic_service_sj_Package::atomic_service_sj_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_sj_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_sj_service_->RequestUnitaryStream(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_sj_CallData(atomic_service_sj_service_, cq_);
                // The actual processing.
                /*TODO: */
                // std::string prefix("Hello atomic_service_sj ");
                // reply_.set_message(prefix + request_.name());

                atomic_service_sj_Request_st atomic_service_sj_Request_t;
                atomic_service_sj_Reply_st atomic_service_sj_Reply_t;

                atomic_service_sj_Request_t.name = request_.name();

                atomic_service_sj_Request_t.integer_field = request_.integer_field();

                atomic_service_sj_Request_t.double_field = request_.double_field();

                atomic_service_sj_Request_t.float_field = request_.float_field();

                for (int i = 0; i < request_.int_array_size(); ++i)
                {
                    atomic_service_sj_Request_t.int_array.push_back(request_.int_array(i));
                }

                for (const auto &item : request_.string_int_map())
                {
                    atomic_service_sj_Request_t.string_int_map[item.first] = item.second;
                }

                /******************************************************************/
                atomic_service_sj_interface(&atomic_service_sj_Request_t, &atomic_service_sj_Reply_t);

                /******************************************************************/
                reply_.Clear(); // clear reply message

                reply_.set_message(atomic_service_sj_Reply_t.message);

                reply_.set_integer_reply(atomic_service_sj_Reply_t.integer_reply);

                reply_.set_double_reply(atomic_service_sj_Reply_t.double_reply);

                reply_.set_float_reply(atomic_service_sj_Reply_t.float_reply);

                for (int i = 0; i < atomic_service_sj_Reply_t.int_array_reply.size(); ++i)
                {
                    reply_.mutable_int_array_reply()->Add(atomic_service_sj_Reply_t.int_array_reply[i]);
                }

                for (const auto &item : atomic_service_sj_Reply_t.string_int_map_reply)
                {
                    reply_.mutable_string_int_map_reply()->insert({item.first, item.second});
                }

                std::cout << "This is Method = UnitaryStream ServiceName=atomic_service_sj_Service" << std::endl;
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
        atomic_service_sj_Package::atomic_service_sj_Service::AsyncService *atomic_service_sj_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_sj_Package::atomic_service_sj_Request request_;
        atomic_service_sj_Package::atomic_service_sj_Reply reply_;
        ServerAsyncResponseWriter<atomic_service_sj_Package::atomic_service_sj_Reply> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_sj_CallData  END */

    /* CallData class atomic_service_st_CallData  BEGAIN */
    class atomic_service_st_CallData
    {
    public:
        atomic_service_st_CallData(atomic_service_st_Package::atomic_service_st_Service::AsyncService *service, ServerCompletionQueue *cq)
            : atomic_service_st_service_(service), cq_(cq), responder_(&ctx_), status_(CREATE)
        {
            Proceed();
        }
        void Proceed()
        {
            if (status_ == CREATE)
            {
                status_ = PROCESS;
                atomic_service_st_service_->RequestUnitaryStream(&ctx_, &request_, &responder_, cq_, cq_, this);
            }
            else if (status_ == PROCESS)
            {
                new atomic_service_st_CallData(atomic_service_st_service_, cq_);
                // The actual processing.
                /*TODO: */
                // std::string prefix("Hello atomic_service_st ");
                // reply_.set_message(prefix + request_.name());

                atomic_service_st_Request_st atomic_service_st_Request_t;
                atomic_service_st_Reply_st atomic_service_st_Reply_t;

                atomic_service_st_Request_t.name = request_.name();

                atomic_service_st_Request_t.integer_field = request_.integer_field();

                atomic_service_st_Request_t.double_field = request_.double_field();

                atomic_service_st_Request_t.float_field = request_.float_field();

                for (int i = 0; i < request_.int_array_size(); ++i)
                {
                    atomic_service_st_Request_t.int_array.push_back(request_.int_array(i));
                }

                for (const auto &item : request_.string_int_map())
                {
                    atomic_service_st_Request_t.string_int_map[item.first] = item.second;
                }

                /******************************************************************/
                atomic_service_st_interface(&atomic_service_st_Request_t, &atomic_service_st_Reply_t);

                /******************************************************************/
                reply_.Clear(); // clear reply message

                reply_.set_message(atomic_service_st_Reply_t.message);

                reply_.set_integer_reply(atomic_service_st_Reply_t.integer_reply);

                reply_.set_double_reply(atomic_service_st_Reply_t.double_reply);

                reply_.set_float_reply(atomic_service_st_Reply_t.float_reply);

                for (int i = 0; i < atomic_service_st_Reply_t.int_array_reply.size(); ++i)
                {
                    reply_.mutable_int_array_reply()->Add(atomic_service_st_Reply_t.int_array_reply[i]);
                }

                for (const auto &item : atomic_service_st_Reply_t.string_int_map_reply)
                {
                    reply_.mutable_string_int_map_reply()->insert({item.first, item.second});
                }

                std::cout << "This is Method = UnitaryStream ServiceName=atomic_service_st_Service" << std::endl;
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
        atomic_service_st_Package::atomic_service_st_Service::AsyncService *atomic_service_st_service_;
        ServerCompletionQueue *cq_;
        ServerContext ctx_;
        atomic_service_st_Package::atomic_service_st_Request request_;
        atomic_service_st_Package::atomic_service_st_Reply reply_;
        ServerAsyncResponseWriter<atomic_service_st_Package::atomic_service_st_Reply> responder_;
        enum CallStatus
        {
            CREATE,
            PROCESS,
            FINISH
        };
        CallStatus status_; // The current serving state.
    };
    /* CallData class atomic_service_st_CallData  END */

    //-----> Step2 This can be run in multiple threads if needed.
public:
    // atomic_service_sfzt_HandleRpcs()
    void atomic_service_sfzt_HandleRpcs()
    {
        new atomic_service_sfzt_CallData(&atomic_service_sfzt_service_, atomic_service_sfzt_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_sfzt_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_sfzt_CallData *>(tag)->Proceed();
        }
    }

    // atomic_service_skzt_HandleRpcs()
    void atomic_service_skzt_HandleRpcs()
    {
        new atomic_service_skzt_CallData(&atomic_service_skzt_service_, atomic_service_skzt_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_skzt_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_skzt_CallData *>(tag)->Proceed();
        }
    }

    // atomic_service_mbsb_HandleRpcs()
    void atomic_service_mbsb_HandleRpcs()
    {
        new atomic_service_mbsb_CallData(&atomic_service_mbsb_service_, atomic_service_mbsb_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_mbsb_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_mbsb_CallData *>(tag)->Proceed();
        }
    }

    // atomic_service_sj_HandleRpcs()
    void atomic_service_sj_HandleRpcs()
    {
        new atomic_service_sj_CallData(&atomic_service_sj_service_, atomic_service_sj_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_sj_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_sj_CallData *>(tag)->Proceed();
        }
    }

    // atomic_service_st_HandleRpcs()
    void atomic_service_st_HandleRpcs()
    {
        new atomic_service_st_CallData(&atomic_service_st_service_, atomic_service_st_cq_.get());
        void *tag;
        bool ok;
        while (true)
        {
            GPR_ASSERT(atomic_service_st_cq_->Next(&tag, &ok));
            GPR_ASSERT(ok);
            static_cast<atomic_service_st_CallData *>(tag)->Proceed();
        }
    }

    /* class var */
private:
    std::unique_ptr<Server> server_;
    // helloworld::Greeter::AsyncService helloworld_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_sfzt_cq_;
    atomic_service_sfzt_Package::atomic_service_sfzt_Service::AsyncService atomic_service_sfzt_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_skzt_cq_;
    atomic_service_skzt_Package::atomic_service_skzt_Service::AsyncService atomic_service_skzt_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_mbsb_cq_;
    atomic_service_mbsb_Package::atomic_service_mbsb_Service::AsyncService atomic_service_mbsb_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_sj_cq_;
    atomic_service_sj_Package::atomic_service_sj_Service::AsyncService atomic_service_sj_service_;

    std::unique_ptr<ServerCompletionQueue> atomic_service_st_cq_;
    atomic_service_st_Package::atomic_service_st_Service::AsyncService atomic_service_st_service_;
};
/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Async_server_class END >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
int main(int argc, char **argv)
{

    std::string ip;
    std::string port;
    std::string broadcastAddress; // Default broadcast addressIP "192.168.0.255"
    std::string broadcastPort;    // Default broadcast port
    // Load configurationInfo from ../Jinja2/ServerBaseInfo.json
    loadConfig("../Jinja2/ServerBaseInfo.json", ip, port, broadcastAddress, broadcastPort);

    std::cout << ">>>>[INFO] Server IP:   " << ip << std::endl;
    std::cout << ">>>>[INFO] Server Port: " << port << std::endl;
    std::cout << ">>>>[INFO] Broadcast Address: " << broadcastAddress << std::endl;
    std::cout << ">>>>[INFO] Broadcast Port:    " << broadcastPort << std::endl;
    std::cout << " " << std::endl;

    json js;
    createSystemStatusJson(js);

    // auto j = readJsonDataFromFile("../Jinja2/ServerBaseInfo.json");
    // nlohmann::json j = readJsonFile("../Jinja2/ServerBaseInfo.json");
    nlohmann::json j = readJsonFile("../Jinja2/ServerInfo.json");

    // createSystemStatusJson(j);
    // std::thread senderThread(broadcastJsonData, broadcastAddress, broadcastPort, std::cref(j));
    std::thread senderThread(broadcastJsonData, broadcastAddress, broadcastPort, j);
    // TODO: Add other threads here

    /* Create AsyncServerImpl BEGAIN */
    AsyncServerImpl serverPersonal(ip, port);
    serverPersonal.Run();

    std::thread atomic_service_sfzt_thread(&AsyncServerImpl::atomic_service_sfzt_HandleRpcs, &serverPersonal);

    std::thread atomic_service_skzt_thread(&AsyncServerImpl::atomic_service_skzt_HandleRpcs, &serverPersonal);

    std::thread atomic_service_mbsb_thread(&AsyncServerImpl::atomic_service_mbsb_HandleRpcs, &serverPersonal);

    std::thread atomic_service_sj_thread(&AsyncServerImpl::atomic_service_sj_HandleRpcs, &serverPersonal);

    std::thread atomic_service_st_thread(&AsyncServerImpl::atomic_service_st_HandleRpcs, &serverPersonal);

    atomic_service_sfzt_thread.join();

    atomic_service_skzt_thread.join();

    atomic_service_mbsb_thread.join();

    atomic_service_sj_thread.join();

    atomic_service_st_thread.join();

    /* Create AsyncServerImpl END */

    senderThread.join();

    return 0;
}