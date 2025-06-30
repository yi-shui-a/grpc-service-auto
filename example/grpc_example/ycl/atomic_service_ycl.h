#ifndef _ATOMIC_SERVICE_YCL_H_
#define _ATOMIC_SERVICE_YCL_H_

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
  * @file:    atomic_service_ycl.h
  * @author:  Spiderman
  * @email:   Spidermsan@atomic_service_st.com
  * @version: V1.0.2
  * @date:    2024-09-30T09-21-21
  * @brief:
  *         +atomic_service_ycl is an implementation of the service interface
  *         +atomic_service_ycl
  * @priority:  1
  *
  * @resource_requirement:
  *         +cpu_architecture: x86_64
  *         +memory: 4GB
  *         +hard_disk: 50GB
  *
* @atomic_service_name: "atomic_service_ycl"
* @details_description: information about atomic_service_ycl
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

typedef struct
{
  int number1;
  int number2;
} input_info;
typedef struct
{
  double x; // X 坐标
  double y; // Y 坐标
  double z; // Z 坐标
  int return_type;
} process_result;

/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

/* 用户 任务函数 (不同的接口函数) */
int atomic_service_fun_task_E(input_info *request, process_result *reply);

/*------------------------  Interface Declaration End  --------------------------*/

#endif // _ATOMIC_SERVICE_YCL_H_
