#ifndef _ATOMIC_SERVICE_MBSB_H_
#define _ATOMIC_SERVICE_MBSB_H_

#include <grpcpp/grpcpp.h>
#include <string>
#include <vector>
#include <map>
/**
* 
* @details_description: Generic interface
* @function_name: "atomic_service_mbsb"
* @parameter: 
*       input parameter:
*       output parameter: 
*/

//Request
 typedef struct atomic_service_mbsb_Request_struct {
    std::string name;
    int32_t integer_field;
    double double_field;
    float float_field;
    std::vector<int32_t> int_array;
    std::map<std::string, std::int32_t> string_int_map;
} atomic_service_mbsb_Request_st;
//Reply
 typedef struct atomic_service_mbsb_Reply_struct{
    std::string message;
    int32_t integer_reply;
    double double_reply;
    float float_reply;
    std::vector<int32_t> int_array_reply;
    std::map<std::string, std::int32_t> string_int_map_reply;
    /*error type*/
    int32_t error_type;  
} atomic_service_mbsb_Reply_st;

void atomic_service_mbsb_interface(atomic_service_mbsb_Request_st *request, atomic_service_mbsb_Reply_st *reply);

int atomic_service_mbsb(atomic_service_mbsb_Request_st *request, atomic_service_mbsb_Reply_st *reply);

#endif // _ATOMIC_SERVICE_MBSB_H_
