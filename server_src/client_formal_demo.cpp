#include <iostream>
#include <memory>
#include <string>

#include <vector>
#include <map>

#include <grpcpp/grpcpp.h>

#include "../rpc_client_inc/atomic_service_mbsb_client.h"
#include "../rpc_client_inc/atomic_service_sf_client.h"

#include "../atom_inc/atomic_service_mbsb.h"
#include "../atom_inc/atomic_service_sf.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

typedef struct
{
    int number1;
    int number2;
    int number3;
    int number4;
} input_demo;

input_demo receiveData()
{
    // 通过DDS获取数据
    input_demo data;
    data.number1 = 99;
    data.number2 = 88;
    data.number1 = 99;
    data.number1 = 99;
    // 返回数据
    return data;
}

void sendInfo()
{
}

int main(int argc, char **argv)
{
    //===============================================================================
    //                             init :初始化程序
    //===============================================================================

    // 创建ip和端口，此处为服务所在服务器的ip和端口号
    std::string server_addr = "localhost:50051";
    // 创建与服务器的通信通道
    auto channel = grpc::CreateChannel(server_addr, grpc::InsecureChannelCredentials());

    // 创建调用服务的类
    atomic_service_mbsb_Service_Client mbsb(channel);
    atomic_service_sf_Service_Client sf(channel);

    //===============================================================================
    //                             receiveData :接收输入数据
    //===============================================================================

    input_demo data = receiveData();

    //===============================================================================
    //                             sendData :向前端发送信号
    //===============================================================================

    sendInfo();

    //===============================================================================
    //                             setParam :设置结构体变量值
    //===============================================================================

    // 声明变量并赋值
    atomic_service_mbsb_task_A_Request_st request_a;
    request_a.number1 = data.number1;
    request_a.number2 = data.number2;
    atomic_service_mbsb_task_B_Request_st request_b;
    request_b.number1 = data.number3;
    request_b.number2 = data.number4;

    // 声明变量
    atomic_service_sf_task_C_Request_st request_c;
    atomic_service_sf_task_D_Request_st request_d;

    //===============================================================================
    //                                 调用服务流程
    //===============================================================================

    //调用第一层服务
    atomic_service_mbsb_task_A_Reply_st reply_a = mbsb.atomic_service_fun_task_A(request_a);
    atomic_service_mbsb_task_B_Reply_st reply_b = mbsb.atomic_service_fun_task_B(request_b);

    //使用上一个服务的运行结果，构造下一个服务的入参
    request_d.int_array.push_back(reply_a.sum_result);
    request_d.int_array.push_back(reply_b.sub_result);
    //调用第二层服务
    atomic_service_sf_task_D_Reply_st reply_d = sf.atomic_service_fun_task_D(request_d);

    //调用第三层服务
    atomic_service_sf_task_C_Reply_st reply_c = sf.atomic_service_fun_task_C(request_c);
    

    std::cout << "Greeter received: " << reply_a.sum_result << "     return_type: " << reply_a.return_type << std::endl;
    std::cout << "Greeter received: " << reply_b.sub_result << "     return_type: " << reply_b.return_type << std::endl;
    std::cout << "Greeter received: " << reply_c.result << "     return_type: " << reply_c.return_type << std::endl;
    // std::cout << "Greeter received: " << reply_d.string_int_map_reply << "     return_type: " << reply_d.return_type << std::endl;

    return 0;
}