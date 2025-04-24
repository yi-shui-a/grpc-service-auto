#ifndef _ATOMIC_SERVICE_SF_H_
#define _ATOMIC_SERVICE_SF_H_

/*------------------------ include Begin --------------------------*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <map>
#include <sstream>
/*------------------------  include End    -------------------------*/

/*------------------------  Service Info Begin  --------------------------*/
/**
  ******************************************************************************
  * @file:    atomic_service_sf.h
  * @author:  Spiderman
  * @email:   Spidermsan@atomic_service_st.com
  * @version: V1.0.2
  * @date:    2024-09-30T09-21-21
  * @brief:
  *         +atom_service_sf is an implementation of the service interface
  *         +atom_service_sf
  * @priority:  1
  *
  * @resource_requirement:
  *         +cpu_architecture: x86_64
  *         +memory: 4GB
  *         +hard_disk: 50GB
  *
* @atomic_service_name: "atomic_service_sf"
* @details_description: information about atomic_service_sf
* @task_function_name:
* @developer:
        +name: yishui
        +email: yishui@atomic_service_fwgz.com
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
/*------------------------  Service Info End  --------------------------*/

/*------------------------  Return Type Begin  --------------------------*/
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
/*------------------------  Return Type End  --------------------------*/

/*------------------------  Message Info Begin  --------------------------*/

// Request /* task_C 输入数据 */
typedef struct
{
  std::string name;
  std::string title;
} atomic_service_sf_task_C_Request_st;
// Reply /* task_C 输出数据 */
typedef struct
{
  std::string result;
  int return_type;
} atomic_service_sf_task_C_Reply_st;
// Request /* task_D 输入数据 */
typedef struct
{
  std::vector<int32_t> int_array;
} atomic_service_sf_task_D_Request_st;
// Reply /* task_D 输出数据 */
typedef struct
{
  std::map<std::string, std::int32_t> string_int_map_reply;
  int return_type;
} atomic_service_sf_task_D_Reply_st;


/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

/* 用户 任务函数 (不同的接口函数) */
int atomic_service_fun_task_C(atomic_service_sf_task_C_Request_st *request, atomic_service_sf_task_C_Reply_st *reply);
int atomic_service_fun_task_D(atomic_service_sf_task_D_Request_st *request, atomic_service_sf_task_D_Reply_st *reply);

/*------------------------  Interface Declaration End  --------------------------*/


/* 服务框架调用接口 */
// void atomic_service_sf_func_C(atomic_service_sf_task_C_Request_st *request, atomic_service_sf_task_C_Reply_st *reply);
// void atomic_service_sf_func_D(atomic_service_sf_task_D_Request_st *request, atomic_service_sf_task_D_Reply_st *reply);


#endif // _ATOMIC_SERVICE_SF_H_
