#ifndef _ATOMIC_SERVICE_MBSB_H_
#define _ATOMIC_SERVICE_MBSB_H_

/*------------------------ include Begain --------------------------*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/*------------------------  include End    -------------------------*/

/**
  ******************************************************************************
  * @file    atom_service_mbsb.cpp
  * @author  Spiderman
  * @version V1.0.0
  * @date    2024-09-21T09-21-21
  * @brief   
  *         + atom_service_mbsb is an implementation of the service interface           
  *         + atom_service_mbsb 
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



/*------------------------  atomic_service_info  Begain -------------------------*/

/*
"basic_info": {
      "name": "atomic_service_mbsb_Service",
      "chinese_name":"原子服务——mbsb",
      "description": " ********** content ********** ",
      "chinese_description": "服务描述、功能介绍",
      "version": "1.0.0",
      "build_time": "2024-08-16T12:00:00Z",
      "developer": {
        "name": "Spiderman",
        "email": "Spidermsan@atomic_service_mbsb.com"
      },
      "maintainer": {
        "name": "IronMan",
        "email": "ironman@PNUI.com"
      },
      "resource_requirements": {
        "cpu_architecture": "x86_64",
        "memory": "4GB",
        "hard_disk": "50GB"
      },
      "operating_system":[
        {
          "name": "Linux",
          "version":5.13.0-117-generic
        },
      ]
    },
*/
/*------------------------  atomic_service_info  End   --------------------------*/


/**
* @atomic_service_name: "atomic_service_mbsb"
* @details_description: information about atomic_service_mbsb
* @task_function_name: 
*   atomic_service_fun_task_A()
*   atomic_service_fun_task_B()
*	  atomic_service_fun_task_C()
*	  atomic_service_fun_task_D()
*/

// return type of service 
#define ATOMIC_SERVICE_SUCCESS 0
#define OperationNotPermitted  1
#define InterruptedSystemCall  2 
#define NoSuchDeviceORAddress  3
#define ArgumentListTooLong    4 
#define InvalidArgument        5
#define NoSuchFile             6
#define NoSuchDir              7
#define DATA_ERROR             8
// TODO: to add your return type


/************************************** 原子服务（atomic_service_mbsb） task_A / Begain*******************************************/
//Request /* task_A 输入数据 */
typedef struct {
    int number1;
    int number2; 
} atomic_service_mbsb_task_A_Request_st;
//Reply /* task_A 输出数据 */
typedef struct {
    int sum_result;
    /*return type*/
    int return_type;
} atomic_service_mbsb_task_A_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_A / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_B / Begain*******************************************/
//Request /* task_B 输入数据 */
typedef struct {
    int number1;
    int number2; 
} atomic_service_mbsb_task_B_Request_st;
//Reply /* task_B 输出数据 */
typedef struct {
    int sub_result;
    /*return type*/
    int return_type; 
} atomic_service_mbsb_task_B_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_B / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_C / Begain*******************************************/
//Request /* task_C 输入数据 */
typedef struct {
    int number1;
    int number2; 
    // int integer_field;
    // double double_field;
    // float float_field;
    // std::string name;
    // std::vector<int32_t> int_array;
    // std::map<std::string, std::int32_t> string_int_map;
} atomic_service_mbsb_task_C_Request_st;
//Reply /* task_C 输出数据 */
typedef struct {
    int multiple_result;
    int integer_reply;
    // double double_reply;
    // float float_reply;
    // std::string message;
    // std::vector<int32_t> int_array_reply;
    // std::map<std::string, std::int32_t> string_int_map_reply;

    /*return type*/
    int return_type;   
} atomic_service_mbsb_task_C_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_C / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_D / Begain*******************************************/
//Request /* task_D 输入数据 */
typedef struct {
    int number1;
    int number2; 
    // int integer_field;
    // double double_field;
    // float float_field;
    // std::string name;
    // std::vector<int32_t> int_array;
    // std::map<std::string, std::int32_t> string_int_map;
} atomic_service_mbsb_task_D_Request_st;
//Reply /* task_D 输出数据 */
typedef struct {
    int division_result;
    // int integer_reply;
    // double double_reply;
    // float float_reply;
    // std::string message;
    // std::vector<int32_t> int_array_reply;
    // std::map<std::string, std::int32_t> string_int_map_reply;
    /*return type*/
    int return_type;   
} atomic_service_mbsb_task_D_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_D / END*******************************************/


// TODO : add other task function

/************************************** 原子服务（atomic_service_mbsb） task_E / Begain*******************************************/
// TODO: add input output data struct
/************************************** 原子服务（atomic_service_mbsb） task_E / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_F / Begain*******************************************/
// TODO: add input output data struct
/************************************** 原子服务（atomic_service_mbsb） task_F / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_G / Begain*******************************************/
// TODO: add input output data struct
/************************************** 原子服务（atomic_service_mbsb） task_G / END*******************************************/

/************************************** 原子服务（atomic_service_mbsb） task_H / Begain*******************************************/
// TODO: add input output data struct
/************************************** 原子服务（atomic_service_mbsb） task_H / END*******************************************

/* 用户 任务函数 (不同的接口函数) */
int atomic_service_fun_task_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply);
int atomic_service_fun_task_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply);
int atomic_service_fun_task_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply);
int atomic_service_fun_task_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply);

// eg:
/*
int atomic_service_fun_task_E(atomic_service_mbsb_task_E_Request_st *request, atomic_service_mbsb_task_E_Reply_st *reply);
int atomic_service_fun_task_F(atomic_service_mbsb_task_F_Request_st *request, atomic_service_mbsb_task_F_Reply_st *reply);
int atomic_service_fun_task_G(atomic_service_mbsb_task_G_Request_st *request, atomic_service_mbsb_task_G_Reply_st *reply);
int atomic_service_fun_task_H(atomic_service_mbsb_task_H_Request_st *request, atomic_service_mbsb_task_H_Reply_st *reply);
*/



/* 服务框架调用接口 */
void atomic_service_mbsb_func_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply);
void atomic_service_mbsb_func_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply);
void atomic_service_mbsb_func_C(atomic_service_mbsb_task_C_Request_st *request, atomic_service_mbsb_task_C_Reply_st *reply);
void atomic_service_mbsb_func_D(atomic_service_mbsb_task_D_Request_st *request, atomic_service_mbsb_task_D_Reply_st *reply);

// eg:
/*
int atomic_service_mbsb_funcE(atomic_service_mbsb_task_E_Request_st *request, atomic_service_mbsb_task_E_Reply_st *reply);
int atomic_service_mbsb_funcF(atomic_service_mbsb_task_F_Request_st *request, atomic_service_mbsb_task_F_Reply_st *reply);
int atomic_service_mbsb_funcG(atomic_service_mbsb_task_G_Request_st *request, atomic_service_mbsb_task_G_Reply_st *reply);
int atomic_service_mbsb_funcH(atomic_service_mbsb_task_H_Request_st *request, atomic_service_mbsb_task_H_Reply_st *reply);
*/
#endif // _ATOMIC_SERVICE_MBSB_H_
