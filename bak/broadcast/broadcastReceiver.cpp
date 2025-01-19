#include <iostream>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    int port = 12345;
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
    while(1){
        // ssize_t received = recvfrom(sock, buffer, sizeof(buffer) - 1, 0,
        //                         (struct sockaddr *) &clientAddr, &clientAddrSize);
        // if (received == -1) {
        //     std::cerr << "Error receiving broadcast message" << std::endl;
        //     close(sock);
        //     return 1;
        // }
        // buffer[received] = '\0';

        // try {
        //     json jsonData = json::parse(buffer);
        //     std::cout << "Received JSON data: " << std::endl;
        //     std::cout << jsonData.dump(4) << std::endl; // 使用缩进为4的格式输出JSON
        // } catch (json::parse_error& e) {
        //     std::cerr << "Failed to parse JSON: " << e.what() << std::endl;
        // }
            ssize_t received = recvfrom(sock, buffer, sizeof(buffer) - 1, 0,
                                (struct sockaddr *) &clientAddr, &clientAddrSize);
            if (received == -1) {
                std::cerr << "Error receiving broadcast message" << std::endl;
                close(sock);
                return 1;
            }
            buffer[received] = '\0'; 
            // std::cout << "Received JSON data _buffer: "<< buffer << std::endl;

            try {
                json jsonData = json::parse(buffer);
                // std::cout << "Received JSON data parse_jsonData: "<< jsonData << std::endl;
                std::cout << "Received JSON data.dump(4): "<< jsonData.dump(4)  << std::endl;
                std::cout << "Received JSON data _jsonData: "<< jsonData["server"]["author"] << std::endl;
            } catch (json::parse_error& e) {
                std::cerr << "Failed to parse JSON: " << e.what() << std::endl;
            }
    }
    close(sock);
    return 0;
}