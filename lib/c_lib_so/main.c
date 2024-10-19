#include <stdio.h>
#include <dlfcn.h>

int main() {
    void *handle;
    int (*add)(int, int);

    // 打开动态链接库
    handle = dlopen("./libshared.so", RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "%s\n", dlerror());
        return 1;
    }

    // 获取函数指针
    add = (int (*)(int, int)) dlsym(handle, "add");
    const char *dlsym_error = dlerror();
    if (dlsym_error) {
        fprintf(stderr, "%s\n", dlsym_error);
        dlclose(handle);
        return 1;
    }

    // 调用函数
    int result = add(5, 7);
    printf("The sum is: %d\n", result);

    // 关闭动态链接库
    dlclose(handle);

    return 0;
}
