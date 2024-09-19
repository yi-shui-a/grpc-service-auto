#ifndef _ATOMIC_SERVICE_MBSB_H_
#define _ATOMIC_SERVICE_MBSB_H_

#include <grpcpp/grpcpp.h>
#include <string>
#include <vector>
#include <map>
/**
* @atomic_service_name: "atomic_service_mbsb"
* @details_description: information about atomic_service_mbsb
* @task_function_name: 
*   atomic_service_fun_task_A()
*   atomic_service_fun_task_B()
*	atomic_service_fun_task_C()
*	atomic_service_fun_task_D()
*/ 

/*
"OS error code   1:  Operation not permitted"
"OS error code   2:  No such file or directory"
"OS error code   3:  No such process"
"OS error code   4:  Interrupted system call"
"OS error code   5:  Input/output error"
"OS error code   6:  No such device or address"
"OS error code   7:  Argument list too long"
"OS error code   8:  Exec format error"
"OS error code   9:  Bad file descriptor"
"OS error code  10:  No child processes"
"OS error code  11:  Resource temporarily unavailable"
"OS error code  12:  Cannot allocate memory"
"OS error code  13:  Permission denied"
"OS error code  14:  Bad address"
"OS error code  15:  Block device required"
"OS error code  16:  Device or resource busy"
"OS error code  22:  Invalid argument"
"OS error code  23:  Too many open files in system"
"OS error code  24:  Too many open files"
"OS error code  25:  Inappropriate ioctl for device"
"OS error code  26:  Text file busy"
"OS error code  27:  File too large"
"OS error code  28:  No space left on device"
"OS error code  29:  Illegal seek"
"OS error code  30:  Read-only file system"
"OS error code  31:  Too many links"
"OS error code  32:  Broken pipe"
"OS error code  33:  Numerical argument out of domain"
"OS error code  34:  Numerical result out of range"
"OS error code  35:  Resource deadlock avoided"
"OS error code  36:  File name too long"
"OS error code  37:  No locks available"
"OS error code  38:  Function not implemented"
"OS error code  39:  Directory not empty"
"OS error code  40:  Too many levels of symbolic links"
"OS error code  42:  No message of desired type"
"OS error code  43:  Identifier removed"
"OS error code  44:  Channel number out of range"
...

TODO: add your error type
*/

define OperationNotPermitted 1
define NoSuchFile            2
define NoSuchDir             3
define InterruptedSystemCall 4
define InvalidArgument       5
define NoSuchDeviceORAddress 6
define ArgumentListTooLong   7
// TODO: to add your error type


/************************************** 原子服务（atomic_service_mbsb） task_A / Begain*******************************************/
//Request /* task_A 输入数据 */
typedef struct {
    std::string name;
    int32_t integer_field;
    double double_field;
    float float_field;
    std::vector<int32_t> int_array;
    std::map<std::string, std::int32_t> string_int_map;
} atomic_service_mbsb_task_A_Request_st;
//Reply /* task_A 输出数据 */
typedef struct {
    std::string message;
    int32_t integer_reply;
    double double_reply;
    float float_reply;
    std::vector<int32_t> int_array_reply;
    std::map<std::string, std::int32_t> string_int_map_reply;
    /*error type*/
    int32_t error_type;   
} atomic_service_mbsb_task_A_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_A / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_B / Begain*******************************************/
//Request /* task_B 输入数据 */
typedef struct {
    std::string name;
    int32_t integer_field;
    double double_field;
    float float_field;
    std::vector<int32_t> int_array;
    std::map<std::string, std::int32_t> string_int_map;
} atomic_service_mbsb_task_B_Request_st;
//Reply /* task_B 输出数据 */
typedef struct {
    std::string message;
    int32_t integer_reply;
    double double_reply;
    float float_reply;
    std::vector<int32_t> int_array_reply;
    std::map<std::string, std::int32_t> string_int_map_reply;
    /*error type*/
    int32_t error_type;   
} atomic_service_mbsb_task_B_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_B / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_C / Begain*******************************************/
//Request /* task_C 输入数据 */
typedef struct {
    std::string name;
    int32_t integer_field;
    double double_field;
    float float_field;
    std::vector<int32_t> int_array;
    std::map<std::string, std::int32_t> string_int_map;
} atomic_service_mbsb_task_C_Request_st;
//Reply /* task_C 输出数据 */
typedef struct {
    std::string message;
    int32_t integer_reply;
    double double_reply;
    float float_reply;
    std::vector<int32_t> int_array_reply;
    std::map<std::string, std::int32_t> string_int_map_reply;
    /*error type*/
    int32_t error_type;   
} atomic_service_mbsb_task_C_Reply_st;
/************************************** 原子服务（atomic_service_mbsb） task_C / END*******************************************/


/************************************** 原子服务（atomic_service_mbsb） task_D / Begain*******************************************/
//Request /* task_D 输入数据 */
typedef struct {
    std::string name;
    int32_t integer_field;
    double double_field;
    float float_field;
    std::vector<int32_t> int_array;
    std::map<std::string, std::int32_t> string_int_map;
} atomic_service_mbsb_task_D_Request_st;
//Reply /* task_D 输出数据 */
typedef struct {
    std::string message;
    int32_t integer_reply;
    double double_reply;
    float float_reply;
    std::vector<int32_t> int_array_reply;
    std::map<std::string, std::int32_t> string_int_map_reply;
    /*error type*/
    int32_t error_type;   
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
