import paramiko, json, argparse, threading
from colorama import Fore, Style

arg_parser = argparse.ArgumentParser()
print_lock = threading.Lock()
arg_parser.add_argument("-c", "--command", help="Command to execute on remote servers")
args = arg_parser.parse_args()


with open ("servers.json", "r") as servers_file:
    servers_data = json.load(servers_file)

def execute_command(hostname, command, sudo_pass=""):
    ssh_client = paramiko.SSHClient()
    ssh_client.get_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname)
    full_command = command
    if command.startswith("sudo"):
        modified_command = full_command.replace('sudo', f'echo "{sudo_pass}" | sudo -S')
        stdin, stdout, stderr = ssh_client.exec_command(modified_command)
        with print_lock:
            output = stdout.read().decode()
            print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}\n{Fore.CYAN}{output}{Style.RESET_ALL}")
            if output == "":
                print(f"{Fore.CYAN}Sudo password is incorrect or was not provided.{Style.RESET_ALL}")
    else:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        with print_lock:
            output = stdout.read().decode()
            print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}\n{Fore.CYAN}{output}{Style.RESET_ALL}")
    ssh_client.close()

threads = []

for server in servers_data["servers"]:
    hostname = server["hostname"]
    sudo_pass = server["sudo_pass"]
    ssh_thread = threading.Thread(target=execute_command, args=(hostname, args.command, sudo_pass))
    threads.append(ssh_thread)
    ssh_thread.start()
for thread in threads:
    thread.join()