import subprocess

"""
这只是一个用于在MCDR获得服务器进程PID的测试插件
(仅适用于Linux)
使用：!!pid
"""


def on_info(server, info):
    if info.content.startswith('!!pid'):
        # 从MCDR获得内部启动shell时的PID，但不是服务器运行进程的PID，不过却有父子进程的关系
        ppid = server._ServerInterface__server.process.pid
        server.reply(info, f"Server ppid: {ppid}")
        cmd = subprocess.Popen(["ps", "--ppid", str(ppid), "-o", "pid"], stdout=subprocess.PIPE)
        pid = cmd.stdout.read().split()[1].decode('utf-8')
        server.reply(info, f"Server pid: {pid}")
