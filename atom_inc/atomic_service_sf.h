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

/**
  ******************************************************************************
  * @file    atomic_service_sf.h
  * @author  Spiderman
  * @email   Spidermsan@atomic_service_st.com
  * @version V1.0.2
  * @date    2024-09-30T09-21-21
  * @brief
  *         + atom_service_sf is an implementation of the service interface
  *         + atom_service_sf
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
* @atomic_service_name "atomic_service_sf"
* @details_description information about atomic_service_sf
* @task_function_name
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

/************************************** åå­æå¡ï¼atomic_service_sfï¼ task_C / Begain*******************************************/
// Request /* task_C è¾å¥æ°æ® */
typedef struct
{
  std::string name;
  std::string title;
} atomic_service_sf_task_C_Request_st;
// Reply /* task_C è¾åºæ°æ® */
typedef struct
{
  std::string result;
  int return_type;
} atomic_service_sf_task_C_Reply_st;
/************************************** åå­æå¡ï¼atomic_service_sfï¼ task_C / END*******************************************/

/************************************** åå­æå¡ï¼atomic_service_sfï¼ task_D / Begain*******************************************/
// Request /* task_D è¾å¥æ°æ® */
typedef struct
{
  std::vector<int32_t> int_array;
} atomic_service_sf_task_D_Request_st;
// Reply /* task_D è¾åºæ°æ® */
typedef struct
{
  std::map<std::string, std::int32_t> string_int_map_reply;
  int return_type;
} atomic_service_sf_task_D_Reply_st;
/************************************** åå­æå¡ï¼atomic_service_sfï¼ task_D / END*******************************************/


/* ç¨æ· ä»»å¡å½æ° (ä¸åçæ¥å£å½æ°) */
int atomic_service_fun_task_C(atomic_service_sf_task_C_Request_st *request, atomic_service_sf_task_C_Reply_st *reply);
int atomic_service_fun_task_D(atomic_service_sf_task_D_Request_st *request, atomic_service_sf_task_D_Reply_st *reply);



/* æå¡æ¡æ¶è°ç¨æ¥å£ */
// void atomic_service_sf_func_C(atomic_service_sf_task_C_Request_st *request, atomic_service_sf_task_C_Reply_st *reply);
// void atomic_service_sf_func_D(atomic_service_sf_task_D_Request_st *request, atomic_service_sf_task_D_Reply_st *reply);



void atomic_service_fun_task_C_func(atomic_service_sf_task_C_Request_st *request, atomic_service_sf_task_C_Reply_st *reply);
void atomic_service_fun_task_D_func(atomic_service_sf_task_D_Request_st *request, atomic_service_sf_task_D_Reply_st *reply);
#endif // _ATOMIC_SERVICE_SF_H_
