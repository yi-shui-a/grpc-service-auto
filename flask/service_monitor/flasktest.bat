REM @echo off：关闭命令行窗口中命令的回显，让窗口只显示命令执行结果。
REM echo Running Python script...：在命令行窗口输出 Running Python script...，提示用户即将运行 Python 脚本。
REM call activate sdw：调用 activate 命令激活名为 sdw 的虚拟环境。call 确保执行完激活命令后能继续执行后续命令。
REM python "D:\chongqing\deployfile\deployfile\sdw\run\sdwqz\flasktest.py"：在激活的虚拟环境中运行指定路径下的 flasktest.py 脚本。
REM echo Python script completed.：脚本执行结束后，在命令行窗口输出 Python script completed.。
REM pause：暂停命令行窗口，等待用户按任意键后关闭窗口。

@echo off
echo Running Python script...
call activate sdw
python "D:\chongqing\deployfile\deployfile\sdw\run\sdwqz\flasktest.py"
echo Python script completed.

pause