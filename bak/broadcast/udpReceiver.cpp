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

/********************************************************************************** */
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
    int port = 37020;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        std::cerr << "Error creating socket" << std::endl;
        return 1;
    }

    // Prepare the address structure
    struct sockaddr_in serverAddr;
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY); // Listen on all interfaces
    serverAddr.sin_port = htons(port);

    // Bind the socket to the address
    if (bind(sock, (struct sockaddr *) &serverAddr, sizeof(serverAddr)) == -1) {
        std::cerr << "Error binding socket" << std::endl;
        close(sock);
        return 1;
    }

    // Receive and parse the broadcast message
    char buffer[1024];
    struct sockaddr_in clientAddr;
    socklen_t clientAddrSize = sizeof(clientAddr);
    ssize_t received = recvfrom(sock, buffer, sizeof(buffer) - 1, 0,
                                (struct sockaddr *) &clientAddr, &clientAddrSize);
    if (received == -1) {
        std::cerr << "Error receiving broadcast message" << std::endl;
        close(sock);
        return 1;
    }
    buffer[received] = '\0';

    try {
        json jsonData = json::parse(buffer);
        std::cout << "Received JSON data: " << std::endl;
        std::cout << jsonData.dump(4) << std::endl; // 使用缩进为4的格式输出JSON
    } catch (json::parse_error& e) {
        std::cerr << "Failed to parse JSON: " << e.what() << std::endl;
    }

    close(sock);
    return 0;
}



int main() {
    // std::thread sender_thread(udpSender, "127.0.0.1", 12345); // 
    std::thread receiver_thread(udpReceiver, 12345); // 

    // sender_thread.join();
    receiver_thread.join();

    return 0;
}