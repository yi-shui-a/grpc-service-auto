#ifndef _ATOMIC_SERVICE_MBSB_H_
#define _ATOMIC_SERVICE_MBSB_H_

/*------------------------ include Begain --------------------------*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
/*------------------------  include End    -------------------------*/

/**
  ******************************************************************************
  * @file    atom_service_mbsb.cpp
  * @author  Spiderman
  * @email   Spidermsan@atomic_service_st.com
  * @version V1.0.0
  * @date    2024-09-21T09-21-21
  * @brief
  *         + atom_service_mbsb is an implementation of the service interface
  *         + atom_service_mbsb
  * @priority  1
  *
  * @requirement
  *         + cpu_architecture: x86_64
  *         + operating_system: Linux
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
  *           + returned type
  ******************************************************************************
*/

/**
* @atomic_service_name: "atomic_service_mbsb"
* @details_description: information about atomic_service_mbsb
* @task_function_name:
// *   atomic_service_fun_task_A()
// *   atomic_service_fun_task_B()
// *	  atomic_service_fun_task_C()
// *	  atomic_service_fun_task_D()
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

enum class ReturnCode
{
  ATOMIC_SERVICE_SUCCESS = 0,
  OperationNotPermitted = 1,
  InterruptedSystemCall = 2,
  NoSuchDeviceORAddress = 3,
  ArgumentListTooLong = 4,
  InvalidArgument = 5,
  NoSuchFile = 6,
  NoSuchDir = 7,
  DATA_ERROR = 8
};

// TODO: to add your return type

/************************************** 原子服务（atomic_service_mbsb） task_A / Begain*******************************************/
// Request /* task_A 输入数据 */
typedef struct
{
  int number1;
  int number2;
} atomic_service_mbsb_task_A_Request_st;
// Reply /* task_A 输出数据 */
typedef struct
{
  int sum_result;
  /*return type*/
  int return_type;
} atomic_service_mbsb_task_A_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_A / END*******************************************/

/************************************** 原子服务（atomic_service_mbsb） task_B / Begain*******************************************/
// Request /* task_B 输入数据 */
typedef struct
{
  int number1;
  int number2;
} atomic_service_mbsb_task_B_Request_st;
// Reply /* task_B 输出数据 */
typedef struct
{
  int sub_result;
  /*return type*/
  int return_type;
} atomic_service_mbsb_task_B_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_B / END*******************************************/

/************************************** 原子服务（atomic_service_mbsb） task_C / Begain*******************************************/
// Request /* task_C 输入数据 */
typedef struct
{
  int number1;
  int number2;

} atomic_service_mbsb_task_C_Request_st;
// Reply /* task_C 输出数据 */
typedef struct
{
  int multiple_result;
  int integer_reply;

  /*return type*/
  int return_type;
} atomic_service_mbsb_task_C_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_C / END*******************************************/

/************************************** 原子服务（atomic_service_mbsb） task_D / Begain*******************************************/
// Request /* task_D 输入数据 */
typedef struct
{
  int number1;
  int number2;

} atomic_service_mbsb_task_D_Request_st;
// Reply /* task_D 输出数据 */
typedef struct
{
  int division_result;

  /*return type*/
  int return_type;
} atomic_service_mbsb_task_D_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_D / END*******************************************/

// TODO : add other task function

/* 用户 任务函数 (不同的接口函数) */
int atomic_service_fun_task_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply);
int atomic_service_fun_task_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply);
int atomic_service_fun_task_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply);
int atomic_service_fun_task_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply);

#endif // _ATOMIC_SERVICE_MBSB_H_
