#ifndef _ATOMIC_TEST_RADAR_H_
#define _ATOMIC_TEST_RADAR_H_

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
  * @file:    atomic_test_radar.h
  * @author:  Spiderman
  * @email:   Spidermsan@atomic_test_radar.com
  * @version: V1.0.2
  * @date:    2024-09-30T09-21-21
  * @chinese_name: 雷达检测服务

  * @priority:  1
  *
  * @resource_requirement:
  *         +cpu_architecture: x86_64
  *         +memory: 4GB
  *         +hard_disk: 50GB
  *
* @atomic_service_name: "atomic_test_radar"
* @details_description: information about atomic_attack_radar
* @task_function_name:
* @developer:
        +name: yishui
        +email: yishui@atomic_test_radar.com
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
  int x;
  int y;
  int z;
  int size;
} radar_info;

typedef struct
{
  int size;
  int x;
  int y;
  int z;
  int return_type;
} radar_result;

typedef struct
{
  int id;
} radar_signal;

typedef struct
{
  int id;
  int state;
  std::string result;
  int return_type;
} radar_state;


/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

/* 用户 任务函数 (不同的接口函数) */
int getRaderMonitor(radar_info *request, radar_result *reply);
int getRaderState(radar_signal *request, radar_state *reply);
/*------------------------  Interface Declaration End  --------------------------*/


#endif // _ATOMIC_TEST_RADAR_H_
