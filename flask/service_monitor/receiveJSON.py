import socket
import json

# 创建套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.0.129', 8023)
sock.bind(server_address)

print("Waiting for data...")

while True:
    header, _ = sock.recvfrom(1024)  # 
    data, _ = sock.recvfrom(65535)  # 
    # print("header:{} ".format(header))
    # print("data:{}".format(data))

    header_Info = json.loads(header.decode('utf-8'))
    Data_Info = json.loads(data.decode('utf-8'))
    header_type = header_Info['type']
    if header_type == 1:
        print("system_version: {}".format(Data_Info['system_version']))
        print("kernel_version: {}".format(Data_Info['kernel_version']))
        print("cpu_usage: {}".format(Data_Info['cpu_usage']))
        print("memory_usage: {}".format(Data_Info['memory_usage']))
    if header_type == 2:
        print("cardNum: {}".format(Data_Info['cardNum']))
        print("total_containers: {}".format(Data_Info['total_containers']))
        print("image_count: {}".format(Data_Info['image_count']))
        print("running_containers: {}".format(Data_Info['running_containers']))
        print("docker_version: {}".format(Data_Info['docker_version']))
        for i in range(15):
            print("container_info.container_id{}: {}".format(i, Data_Info['container_info'][i]['container_id']))
            print("ContainerInspect.container_id{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_id']))
            print("container_info.container_created{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_created']))
            print("container_info.container_path{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_path']))
            print("container_info.container_args{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_args']))
            print("container_info.status{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['status']))
            print("container_info.running{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['running']))
            print("container_info.paused{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['paused']))
            print("container_info.restarting{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['restarting']))
            print("container_info.oomkilled{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['oomkilled']))
            print("container_info.dead{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['dead']))
            print("container_info.pid{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['pid']))
            print("\n")
    print("================================== \n")
    # print(f"Docker Info: ID={student_data['dockerInfo']['id']},\
    #         Name='{student_data['dockerInfo']['name']}', \
    #         Usage={student_data['dockerInfo']['usage']}")
