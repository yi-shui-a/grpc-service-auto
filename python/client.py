import grpc
import my_service_pb2
import my_service_pb2_grpc

def run(num):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = my_service_pb2_grpc.MyServiceStub(channel)
        response = stub.SayHello(my_service_pb2.MyRequest(name='Spiderman'+str(num)))
        print("Client received:{} num={} ".format(response.greeting, num))

if __name__ == '__main__':
    num = 0
    while(True):
        run(num)
        num+=1
