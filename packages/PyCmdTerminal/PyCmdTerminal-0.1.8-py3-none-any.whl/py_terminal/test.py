from py_terminal.RemoteTerminal import RemoteTerminal

if __name__ == '__main__':
    def call(out, err):
        print("Calling1", [out], [err])


    def call2(out, err):
        print("Calling2", [out], [err])


    with RemoteTerminal('10.22.0.71',
                        username="user",
                        password="1234",
                        port=22
                        ) as ssh_client:
        pass
        print(ssh_client.makedirs("/home/user/test/dong", exist_ok=True))
        # 推送文件
        # print(ssh_client.push(f"/mnt/c/Users/BX3MDyy/WorkSpaces/Code/new_filback/t2.py", "/home/user"))
        # 推送目录
        # print(ssh_client.push(f"/mnt/c/Users/BX3MDyy/WorkSpaces/Code/new_filback/test", "/home/user"))
        # 拉文件
        # ssh_client.pull("/home/user/docker.sh", "./")
        # 删除
        # print(ssh_client.delete("/home/user/test"))
        # 杀死进程
        # print(ssh_client.kill('my_custom_proce'))
        # 杀死找到的所有PID
        # print(ssh_client.kill("my_custom_proce", kill_all=True))
        # 读取文件
        # print(ssh_client.read(r"/home/user/t2.py"))
        # 异步执行命令
        # p = ssh_client.async_execute_command("ls ~/")
        # print(p)
        # 通过PID获取异步执行命令的输出
        # t1 = ssh_client.get_sync_process_output(p, call)
        # t2 = ssh_client.get_sync_process_output(p, call2, wait=False)
        # time.sleep(2)
        # t1.stop()
        # t2.stop()
        # print(ssh_client.kill(p))

        # for i in ssh_client.read(r"/home/user/t3.py", chunk_size=20):
        #     print(i)
        # ssh_client.open_sftp()
        # print(ssh_client.delete(r"/home/user/t2.py"))

        # print(ssh_client.execute_command("sudo ls /home/user"))
        # print(ssh_client.get_os())
        # print(ssh_client.pid_exists(1017986))
        # print(ssh_client.get_pname_by_pid(1017986))
        # print(ssh_client.get_pids_by_pname('kworker/18:0-mm_percpu_wq'))
        # print(ssh_client.command_exists("ls"))
