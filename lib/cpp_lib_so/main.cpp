// main.cpp
#include <iostream>
#include <dlfcn.h> // 用于dlopen, dlsym等

int main() {
    void* handle = nullptr;
    int (*addFunc)(int, int);

    // 加载动态链接库
    handle = dlopen("./libdemo.so", RTLD_LAZY);
    if (!handle) {
        std::cerr << "Cannot open library: " << dlerror() << std::endl;
        return 1;
    }

    // 获取函数指针
    addFunc = (int (*)(int, int)) dlsym(handle, "add");
    const char* dlsym_error = dlerror();
    if (dlsym_error) {
        std::cerr << "Cannot load symbol 'add': " << dlsym_error << std::endl;
        dlclose(handle);
        return 1;
    }

    // 调用函数
    int result = addFunc(10, 20);
    std::cout << "The sum is: " << result << std::endl;

    // 关闭动态链接库
    dlclose(handle);

    return 0;
}
