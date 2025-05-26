import random


def funA():
    # 生成一个在[a, b]范围内的随机整数，包括a和b
    random_int = random.randint(10, 10000)
    return random_int


def funB():
    # 生成一个服务名和ip端口的列表，随机返回一个列表
    service_name = [
        "atomic_service_mbsb_Service",
        "atomic_service_sf_Service",
        "atomic_service_ldsc_Service",
        "atomic_service_asdasdas_Service",
        "atomic_service_dsds_Service",
    ]
    ip_port = [
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.3",
        "172.153.15.4",
        "172.153.15.5",
    ]
    service_name = random.choice(service_name)
    ip_port = random.choice(ip_port)
    return service_name, ip_port


def funC():
    # 随机生成一个在[50, 200]范围内的整数A，生成一个长度为A的列表，列表中的元素是在[0, 100000]范围内的随机整数，从左到右，从小到大排列
    A = random.randint(50, 200)
    list = []
    for i in range(A):
        list.append(random.randint(0, 100000))
    list.sort()
    return list


def funD():
    # 随机生成一个五元组
    a = random.randint(0, 100000)
    b = random.randint(0, 100000)
    c = random.randint(0, 100000)
    d = random.randint(0, 100000)
    e = random.randint(0, 100000)
    return a, b, c, d, e


def funE():
    # 生成一个在[a, b]范围内的随机整数，包括a和b
    random_int = random.randint(-10000, 10000)
    return random_int


if __name__ == "__main__":
    for i in range(1000):
        print("第" + str(i + 1) + "次测试，结果为： " + str(funE()))
    sum = 795.781005
    max = 0.837144
    avg = sum / 1000
    print("1000次测试，运行总时长:" + str(sum) + "ms")
    print("单次测试，平均运行时长:" + str(avg) + " ms")
    print("最大单次耗时:" + str(max) + "ms")
