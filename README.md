# 项目说明

一种嵌入式环境下的微服务框架



# 项目结构

```
.
├─ .gitignore
├─ README.md
├─ bak/
├─ db/
│   ├─ atomic_service/
│   ├─ dds/
│   └─ ...
├─ doc/
├─ example/
├─ src/
│   ├─ scripts/
│   │   ├─ AXService.py
│   │   ├─ AtomService.py
│   │   ├─ Client.py
│   │   ├─ GrpcMethod.py
│   │   ├─ Server.py
│   │   ├─ ServiceMethod.py
│   │   ├─ config/
│   │   ├─ entity/
│   │   └─ util/
│   └─ templates/
├─ test/
```

> `.gitignore` 文件：指定了在 Git 版本控制中被忽略的文件和目录。
>
> `.vscode/` 目录：包含了 Visual Studio Code 的相关配置文件。
>
> `bak/` 目录：存放了一些备份文件。
>
> `db/` 目录：包含了数据库相关的数据和文件。
>
> `doc/` 目录：包含了文档相关的资料。
>
> `example/` 目录：包含了一些示例代码和文件。
>
> `src/` 目录：包含了项目的主要源代码，如脚本、模板等。
>
> `test/` 目录：包含了测试相关的文件。



# 安装方式

### 容器构建

通过百度云链接下载或构建镜像。

**链接：**

> 通过网盘分享的文件：micro_service
> 链接: https://pan.baidu.com/s/1R1HqjzZ1BvkUrbclEE5WVQ?pwd=6pfm 提取码: 6pfm

### 项目下载

```shell
git clone https://gitee.com/SpidermanW/server_compiling.git
```



# 使用方法

### 安装成功测试

```shell
cd server_compiling/
python ./test/test_module.py
python ./test/run_idl_compile.py
```

> 若不报错，则说明安装成功