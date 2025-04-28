#ifndef _ATOMIC_SERVICE_STANDARD_H_
#define _ATOMIC_SERVICE_STANDARD_H_

/*------------------------ Include Begin --------------------------*/

// C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <string>
#include <math.h>
#include <time.h>
#include <ctype.h>

// C++
#include <iostream>
#include <fstream>
#include <chrono>
#include <string>

#include <cmath>
#include <vector>
#include <map>
#include <set>
/*------------------------  Include End  -------------------------*/



/*------------------------  Service Info Begin  --------------------------*/
/**
  *
  * @name:    atomic_service_mbsb
  * @chinese_name: chinese_service_mbsb
  * @description: information about atomic_service_mbsb
  * @version: V1.0.0
  * @build_time: 2024-09-21T09-21-21
  * @license: MIT
  * @service_path: /atomic_service_mbsb
  *
  * @resource_requirement:
  *         + cpu_architecture: x86_64
  *         + memory: 4GB
  *         + hard_disk: 50GB
  *
  *@developer:
  *      +name: Spiderman
  *      +email: Spidermsan@atomic_service_fwgz.com
  *@maintainer:
  *      +name:IronMan
  *      +email:ironman@PNUI.com
  *@operating_system:
  *      +name:Linux
  *      +v1:5.13.0-117-generic
  *      +v2:5.14.0-117-generic
  *      +name:SylixOS
  *      +v1:1.0.0
  *      +v2:1.0.2
  * 
  * 
  * 
*/
/*------------------------  Service Info End  --------------------------*/


/*------------------------  Return Type Begin  --------------------------*/

#define ATOMIC_SERVICE_SUCCESS 0
#define ATOMIC_SERVICE_FAIL -1
#define ATOMIC_SERVICE_TIMEOUT -2
#define ATOMIC_SERVICE_ERROR -3
#define ATOMIC_SERVICE_NOT_SUPPORT -4
#define ATOMIC_SERVICE_NOT_READY -5
#define ATOMIC_SERVICE_NOT_INIT -6
#define ATOMIC_SERVICE_NOT_START -7
#define ATOMIC_SERVICE_NOT_STOP -8
#define ATOMIC_SERVICE_NOT_RELEASE -9
#define ATOMIC_SERVICE_NOT_DESTROY -10
#define ATOMIC_SERVICE_NOT_CREATE -11
#define ATOMIC_SERVICE_NOT_OPEN -12
#define ATOMIC_SERVICE_NOT_CLOSE -13
#define ATOMIC_SERVICE_NOT_READ -14
#define ATOMIC_SERVICE_NOT_WRITE -15
#define ATOMIC_SERVICE_NOT_SEEK -16
#define ATOMIC_SERVICE_NOT_TELL -17
#define ATOMIC_SERVICE_NOT_SIZE -18
#define ATOMIC_SERVICE_NOT_SEEK_END -19
#define ATOMIC_SERVICE_NOT_SEEK_SET -20
#define ATOMIC_SERVICE_NOT_SEEK_CUR -21
#define ATOMIC_SERVICE_NOT_SEEK_ABS -22

/*------------------------  Return Type End  --------------------------*/




/*------------------------  Message Info Begin  --------------------------*/
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
  int return_type;
} atomic_service_mbsb_task_A_Reply_st;

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
  int return_type;
} atomic_service_mbsb_task_B_Reply_st;
/*------------------------  Message Info End  --------------------------*/


/*------------------------  Interface Declaration Begin  --------------------------*/

int atomic_service_fun_task_A(atomic_service_mbsb_task_A_Request_st *request, atomic_service_mbsb_task_A_Reply_st *reply);
int atomic_service_fun_task_B(atomic_service_mbsb_task_B_Request_st *request, atomic_service_mbsb_task_B_Reply_st *reply);

/*------------------------  Interface Declaration End  --------------------------*/



#endif // _ATOMIC_SERVICE_STANDARD_H_
