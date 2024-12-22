#ifndef _ATOMIC_SERVICE_MBSB_H_
#define _ATOMIC_SERVICE_MBSB_H_

/*------------------------ Include Begin --------------------------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*------------------------  Include End  -------------------------*/



/*------------------------  Service Info Begin  --------------------------*/
/**
  *
  * @file:    atomic_service_mbsb.h
  * @atomic_service_name: "atomic_service_mbsb"
  * @chinese_name: "chinese_service_mbsb"
  * @description: information about atomic_service_mbsb
  * @author:  Spiderman
  * @email:   Spidermsan@atomic_service_st.com
  * @version: V1.0.0
  * @date:    2024-09-21T09-21-21
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



#endif // _ATOMIC_SERVICE_MBSB_H_
