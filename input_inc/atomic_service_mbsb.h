#ifndef _ATOMIC_SERVICE_MBSB_H_
#define _ATOMIC_SERVICE_MBSB_H_

#include <grpcpp/grpcpp.h>
#include <string>
#include <vector>
#include <map>


/**
  ******************************************************************************
  * @file    atomic_service_mbsb.cpp
  * @author  Spiderman
  * @email   Spidermsan@atomic_service_st.com
  * @version V1.0.0
  * @date    2024-09-21T09-21-21
  * @brief
  *         + atom_service_mbsb is an implementation of the service interface
  *         + atom_service_mbsb
  * @priority  1
  *
  * @resource_requirement
  *         + cpu_architecture: x86_64
  *         + memory: 4GB
  *         + hard_disk: 50GB
  *
  *
  *
@verbatim
 ===============================================================================
                      ##### How to use this driver #####
 ===============================================================================

@endverbatim
  *
  ******************************************************************************
  * @attention
  ******************************************************************************
*/

/*------------------------  atomic_service_info  Begin -------------------------*/

/**
* @atomic_service_name "atomic_service_mbsb"
* @details_description information about atomic_service_mbsb
* @task_function_name
* @developer:
        +name: Spiderman
        +email: Spidermsan@atomic_service_fwgz.com
@maintainer:
        +name:IronMan
        +email:ironman@PNUI.com
@operating_system:
        +name:Linux
        +v1:5.13.0-117-generic
        +v2:5.14.0-117-generic
        +name:SylixOS
        +v1:1.0.0
        +v2:1.0.2

*/

// return type of service
#define ATOMIC_SERVICE_SUCCESS 0
#define OperationNotPermitted 1
#define InterruptedSystemCall 2
#define NoSuchDeviceORAddress 3
#define ArgumentListTooLong 4
#define InvalidArgument 5
#define NoSuchFile 6
#define NoSuchDir 7
#define DATA_ERROR 8




//Request
typedef struct atomic_service_mbsb_Request_struct {
    std::string name;
    int integer_field;
    double double_field;
    float float_field;
} atomic_service_mbsb_Request_st;
//Reply
typedef struct atomic_service_mbsb_Reply_struct{
    std::string message;
    int integer_reply;
    double double_reply;
    float float_reply;
} atomic_service_mbsb_Reply_st;

void atomic_service_mbsb_interface(atomic_service_mbsb_Request_st *request, atomic_service_mbsb_Reply_st *reply);

#endif // _ATOMIC_SERVICE_MBSB_H_
