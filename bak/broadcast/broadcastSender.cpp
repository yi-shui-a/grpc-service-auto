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
    const char *broadcastMessage = R"({"message": "Hello, broadcast!", "time": "2024-08-18T17:10:00Z"})";
    const char *broadcastIP = "255.255.255.255";
    int broadcastPort = 12345;

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
    while(true){
        if (sendto(sock, broadcastMessage, strlen(broadcastMessage), 0,
               (struct sockaddr *) &broadcastAddr, sizeof(broadcastAddr)) == -1) {
        std::cerr << "Error sending broadcast message" << std::endl;
        close(sock);
        return 1;
    }
    std::cout << "Broadcast message sent successfully." << std::endl;
    }
    close(sock);
    return 0;
}