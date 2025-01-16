#include <iostream>
#include <stdio.h>
#include <memory>
#include <string>
#include <time.h>

#include <grpcpp/grpcpp.h>

#include "../rpc_client_inc/atomic_service_mbsb_client.h"

#include "../atom_service/atomic_service_mbsb/atomic_service_mbsb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

int main(int argc, char **argv)
{
    //===============================================================================
    //                             init :初始化程序
    //===============================================================================
    struct timespec start, end;
    std::string server_addr = "localhost:50051";
    auto channel = grpc::CreateChannel(server_addr, grpc::InsecureChannelCredentials());
    atomic_service_mbsb_Service_Client mbsb(channel);

    //===============================================================================
    //                             setParam :设置请求值
    //===============================================================================
    atomic_service_mbsb_task_A_Request_st request_a;
    request_a.number1 = 50;
    request_a.number2 = 49;

    //===============================================================================
    //                             调用微服务 :循环调用1000次微服务
    //===============================================================================
    // 获取开始时间
    clock_gettime(CLOCK_MONOTONIC, &start);
    //循环调用函数
    for (int i = 0;i < 1000 ; i++)
    {
        atomic_service_mbsb_task_A_Reply_st reply_a = mbsb.atomic_service_fun_task_A(request_a);
        std::cout << "Greeter received: " << reply_a.sum_result << "     return_type: " << reply_a.return_type << std::endl;
    }
    // 获取结束时间
    clock_gettime(CLOCK_MONOTONIC, &end);
    // 计算经过的时间（以秒为单位），然后转换为毫秒
    double elapsed = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;
    printf("1000次测试，运行总时长：%f ms\n", elapsed);
    printf("单次测试，平均运行时长：%f ms\n", elapsed/1000);
    
    return 0;
}