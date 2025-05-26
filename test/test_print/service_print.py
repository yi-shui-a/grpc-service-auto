import random


def funA():
    print(
        "This is Method = atomic service fun task A    ServiceName = atomic service mbsb Service"
    )


def funB():
    print(
        "This is Method = query_service_data    ServiceName = atomic_service_data_query_Service"
    )


def funC():
    # 排序算法
    print(
        "This is Method = des_sort_service    ServiceName = atomic_service_data_sort_Service"
    )


def funD():
    # 检测算法
    print(
        "This is Method = detect_service    ServiceName = atomic_service_data_detect_Service"
    )


def funE():
    # 组合算法
    # 一个算法列表
    fun_list = [
        "atomic_service_func_plus",
        "atomic_service_func_minus",
        "atomic_service_func_multiply",
        "atomic_service_func_divide",
    ]
    service_list = [
        "atomic_service_func_plus_Service",
        "atomic_service_func_minus_Service",
        "atomic_service_func_multiply_Service",
        "atomic_service_func_divide_Service",
    ]
    # 随机打印一个
    print(
        "This is Method = "
        + random.choice(fun_list)
        + "    ServiceName = "
        + random.choice(service_list)
    )


if __name__ == "__main__":
    for i in range(1000):
        funE()
