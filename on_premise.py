import os
import sys
sys.path.insert(0,"./common")

from fabric_common import RemoteShell
from fabric.network import ssh
from fabric.context_managers import *
from datetime import datetime
from ConfigParser import SafeConfigParser

ssh.util.log_to_file("./logs/paramiko.log", 10)

class OnPremis():

    def __init__(self):
        kubeadm_join_command = ""

    def DoError (self,Error) :
       sys.exit(Error)

    def parser_and_execute(self,conf_file="on_premise.conf", force=False):
        """."""
        conf_file = os.path.abspath(conf_file)
        config = SafeConfigParser()
        if not os.path.isfile(conf_file):
            print(colored("No such file found : %s" % conf_file, "red"))
            sys.exit(1)
        try:
            config.read(conf_file)
        except configparser.DuplicateSectionError as e:
            print(e)
            sys.exit(1)
        except configparser.DuplicateOptionError as e:
            print(e)
            sys.exit(1)
        except configparser.ParsingError as e:
            print(colored('Parsing error in mini_ansible.conf', 'red'))
            print(e)
            sys.exit(1)
        sections = config.sections();
        for section in sections:
            username = None
            password = None
            command_list = None
            private_key = None
            local_path = None
            remote_path = None
            print("-----------------> " + section)
            for key,value in config.items(section):
                if key == "ip":
                    ip = value
                if key == "username":
                    username = value
                if key == "password":
                    password = value
                if key == "command":
                    command_list = value.split("\n")
                    if "slave" in section:
                        command_list.append("sudo " + self.kubeadm_join_command)
                if key == "private_key":
                    private_key = value
                if key == "local_path":
                    local_path = value
                if key == "remote_path":
                    remote_path = value
            if username and ip:
                if private_key:
                    if local_path and remote_path:
                        self.send_file_remote(local_path,remote_path,ip,username,private_key=private_key)
                        print("File sent succesfully : " + remote_path)
                    if command_list:
                        self.execute_command_list_remotely(command_list,ip,username,private_key=private_key)
                    elif not local_path and not remote_path:
                        print("local_path or remote_path or command_list field are not found for " + str(section))
                if password:
                    if local_path and remote_path:
                        self.send_file_remote(local_path,remote_path,ip,username,password=password)
                        print("File sent succesfully : " + remote_path)
                    if command_list:
                        self.execute_command_list_remotely(command_list,ip,username,password=password)
                    elif not local_path and not remote_path:
                        print("local_path or remote_path or command_list field are not found for " + str(section))
                if not private_key and not password:
                    print("private_key or password field are not found for " + str(section))
            else:
                print("username or ip field are not found for "+ str(section))


    def execute_command_list_remotely(self,command_list,ip,user,password=None,private_key=None):
        try:
            if private_key:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,private_key=private_key)
            else:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,password=password)
            for actual_command in command_list:
                print("IP / DNS : " + ip )
                print("Command : " + actual_command )
                f_obj = ssh_connect_remote.run(cmd=actual_command)
                status, res = ssh_connect_remote.return_status_message_fabric(f_obj)
                if status:
                    print("Output : " + str(res))
                    if "kubeadm init" in actual_command:
                        self.kubeadm_join_command = res.split("Then you can join any number of worker nodes by running the following on each as root:")[1].replace("\\","").replace("\r\n","").strip()
                else:
                    print("Output : Failed to execute the above command")
                    print("Error for your reference : " + str(res))
                print("\n")
            del ssh_connect_remote
        except Exception as e:
            self.DoError("Exception in execute_command :"+str(e) )

    def send_file_remote(self,local_path,remote_path,ip,user,password=None,private_key=None):
        try:
            if private_key:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,private_key=private_key)
            else:
                ssh_connect_remote = RemoteShell(hostname=ip,user=user,password=password)
            ssh_connect_remote.file_send(local_path,remote_path)
            del ssh_connect_remote
        except Exception as e:
            self.DoError("Exception in execute_command :"+str(e) )



def main():
    obj = OnPremis()
    try:
        obj.parser_and_execute()
    except Exception as e:
        obj.DoError(str(e))

if __name__ == "__main__":
    main()
