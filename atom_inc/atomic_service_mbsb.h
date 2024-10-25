#ifndef _ATOMIC_SERVICE_MBSB_H_
#define _ATOMIC_SERVICE_MBSB_H_

/*------------------------ include Begin --------------------------*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/*------------------------  include End    -------------------------*/

/**
  ******************************************************************************
  * @file    atomic_service_mbsb.h
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


// TODO: to add your return type

/************************************** åå­æå¡ï¼atomic_service_mbsbï¼ task_A / Begain*******************************************/
// Request /* task_A è¾å¥æ°æ® */
typedef struct
{
  int number1;
  int number2;
} atomic_service_mbsb_task_A_Request_st;
// Reply /* task_A è¾åºæ°æ® */
typedef struct
{
  int sum_result;
  int return_type;
} atomic_service_mbsb_task_A_Reply_st;
/************************************** åå­æå¡ï¼atomic_service_mbsbï¼ task_A / END*******************************************/

/************************************** åå­æå¡ï¼atomic_service_mbsbï¼ task_B / Begain*******************************************/
// Request /* task_B è¾å¥æ°æ® */
typedef struct
{
  int number1;
  int number2;
} atomic_service_mbsb_task_B_Request_st;
// Reply /* task_B è¾åºæ°æ® */
typedef struct
{
  int sub_result;
  int return_type;
} atomic_service_mbsb_task_B_Reply_st;
/************************************** åå­æå¡ï¼atomic_service_mbsbï¼ task_B / END*******************************************/


/* ç¨æ· ä»»å¡å½æ° (ä¸åçæ¥å£å½æ°) */
int atomic_service_fun_task_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply);
int atomic_service_fun_task_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply);

#endif // _ATOMIC_SERVICE_MBSB_H_
