#include <iostream>
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


// use nlohmann/json for json handling
using json = nlohmann::json;

void createSystemStatusJson(json& js) {
    js["system_version"] = "1.0";
    js["architecture"] = "x86_64";
    // 其他系统状态信息...
    // j["memory_usage"] = ...;
    // j["network_usage"] = ...;
}

void udpSender(const char* server_host, uint16_t server_port) {
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Cannot open socket: " << strerror(errno) << std::endl;
        return;
    }
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(server_port);

    if (inet_pton(AF_INET, server_host, &serv_addr.sin_addr) <= 0) {
        std::cerr << "Invalid address / Address not supported: " << strerror(errno) << std::endl;
        close(sockfd);
        return;
    }
    json j;
    createSystemStatusJson(j);
    while (true) {
        sendto(sockfd, j.dump().c_str(), j.dump().length(), 0,
               (const struct sockaddr *) &serv_addr, sizeof(serv_addr));
        std::this_thread::sleep_for(std::chrono::seconds(1)); // sleep for 1 second
    }
    close(sockfd);
}


void udpReceiver(uint16_t listen_port) {
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        std::cerr << "Cannot open socket: " << strerror(errno) << std::endl;
        return;
    }
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(listen_port);
    if (bind(sockfd, (const struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "Cannot bind socket: " << strerror(errno) << std::endl;
        close(sockfd);
        return;
    }
    char buffer[1024];
    socklen_t len = sizeof(serv_addr);
    while (true) {
        ssize_t byte_read = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                                     (struct sockaddr *) &serv_addr, &len);
        if (byte_read > 0) {
            // handle received data
            std::cout << "Received data: " << std::string(buffer, byte_read) << std::endl;
        }
    }
    close(sockfd);
}
/*------------------------------------------------------------------------------------------*/

#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <nlohmann/json.hpp> // 使用 nlohmann/json 库

using json = nlohmann::json;

int main() {
    const char *broadcastMessage = R"({"message": "Hello, broadcast!", "time": "2024-08-18T17:10:00Z"})";
    const char *broadcastIP = "255.255.255.255";
    int broadcastPort = 37020;

    // Create a UDP socket
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        std::cerr << "Error creating socket" << std::endl;
        return 1;
    }

    // Set the broadcast option
    int broadcastPermission = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcastPermission, sizeof(broadcastPermission)) == -1) {
        std::cerr << "Error setting broadcast option" << std::endl;
        close(sock);
        return 1;
    }

    // Prepare the address structure
    struct sockaddr_in broadcastAddr;
    memset(&broadcastAddr, 0, sizeof(broadcastAddr));
    broadcastAddr.sin_family = AF_INET;
    broadcastAddr.sin_port = htons(broadcastPort);
    if (inet_aton(broadcastIP, &broadcastAddr.sin_addr) == 0) {
        std::cerr << "Invalid broadcast IP address" << std::endl;
        close(sock);
        return 1;
    }

    // Send the broadcast message
    if (sendto(sock, broadcastMessage, strlen(broadcastMessage), 0,
               (struct sockaddr *) &broadcastAddr, sizeof(broadcastAddr)) == -1) {
        std::cerr << "Error sending broadcast message" << std::endl;
        close(sock);
        return 1;
    }

    std::cout << "Broadcast message sent successfully." << std::endl;
    close(sock);
    return 0;
}
/*********************************************************************************/
#include <fstream>
#include <nlohmann/json.hpp>
using json = nlohmann::json;

// ...

std::ifstream f("example.json");
json data = json::parse(f);

/*********************************************************************************/
// Using (raw) string literals and json::parse
json ex1 = json::parse(R"(
  {
    "pi": 3.141,
    "happy": true
  }
)");

// Using user-defined (raw) string literals
using namespace nlohmann::literals;
json ex2 = R"(
  {
    "pi": 3.141,
    "happy": true
  }
)"_json;

// Using initializer lists
json ex3 = {
  {"happy", true},
  {"pi", 3.141},
};


/*********************************************************************************/
// create an empty structure (null)
json j;
j["name"] = "John";
// add a number that is stored as double (note the implicit conversion of j to an object)
j["pi"] = 3.141;

// add a Boolean that is stored as bool
j["happy"] = true;

// add a string that is stored as std::string
j["name"] = "Niels";

// add another null object by passing nullptr
j["nothing"] = nullptr;

// add an object inside the object
j["answer"]["everything"] = 42;

// add an array that is stored as std::vector (using an initializer list)
j["list"] = { 1, 0, 2 };

// add another object (using an initializer list of pairs)
j["object"] = { {"currency", "USD"}, {"value", 42.99} };

// instead, you could also write (which looks very similar to the JSON above)
json j2 = {
  {"pi", 3.141},
  {"happy", true},
  {"name", "Niels"},
  {"nothing", nullptr},
  {"answer", {
    {"everything", 42}
  }},
  {"list", {1, 0, 2}},
  {"object", {
    {"currency", "USD"},
    {"value", 42.99}
  }}
};
/************************************************************************************/
int main() {
    std::thread sender_thread(udpSender, "127.0.0.1", 12345); // 
    // std::thread receiver_thread(udpReceiver, 12345); // 

    sender_thread.join();
    // receiver_thread.join();

    return 0;
}