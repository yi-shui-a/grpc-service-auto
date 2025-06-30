#include "atomic_show_hjrd.h"

int getHJRDData(hjrd_input *request, hjrd_output *reply){
        std::random_device rd; 
    std::mt19937 gen(rd()); 
    std::uniform_int_distribution<> dis(100, 1000); 
    reply->x = dis(gen);
    reply->y = dis(gen);
    reply->z = dis(gen);
    reply->size = dis(gen);
    return ATOMIC_SERVICE_SUCCESS;
}