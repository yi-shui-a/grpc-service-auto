#ifndef _ATOMIC_SHOW_YSDD_H_
#define _ATOMIC_SHOW_YSDD_H_

/*------------------------ Include Begin --------------------------*/

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
 * @name:     atomic_show_ysdd
 * @chinese_name: 数据融合
 * @description: information atomic_show_ysdd
 * @version: V1.0.0
 * @build_time: 2024-05-23 16:00:00
 * @license: MIT
 * @service_path: atomic_show_ysdd
 *
 * @resource_requirement:
 *         + cpu_architecture: x86_64
 *         + memory: 4GB
 *         + hard_disk: 50GB
 *
 * @developer:
 *      +name: Spiderman
 *      +email: Spidermsan@atomic_show_ysdd.com
 * @maintainer:
 *      +name: yishui
 *      +email:yishui@atomic_show_ysdd.com
 * @operating_system:
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

typedef struct
{
    int x;
    int y;
    int z;
    int size;
} ysdd_input;

typedef struct
{
    int x;
    int y;
    int z;
    int size;
    int return_type;
} ysdd_output;

/*------------------------  Message Info End  --------------------------*/

/*------------------------  Interface Declaration Begin  --------------------------*/

int getYSDDData(ysdd_input *request, ysdd_output *reply);

/*------------------------  Interface Declaration End  --------------------------*/

#endif // _ATOMIC_SHOW_YSDD_H_
