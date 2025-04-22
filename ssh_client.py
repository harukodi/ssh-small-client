import paramiko, json, argparse, threading
from colorama import Fore, Style

arg_parser = argparse.ArgumentParser()
print_lock = threading.Lock()
arg_parser.add_argument("-c", "--command", help="Command to execute on remote servers")
args = arg_parser.parse_args()

with open ("servers.json", "r") as servers_file:
    servers_data = json.load(servers_file)

def execute_command(hostname, username, command, sudo_pass=""):
    def is_reboot_command(command):
        power_suffixes = ["shutdown", "reboot", "poweroff", "halt"]
        if any(power_suffix in command.lower() for power_suffix in power_suffixes):
            return True
        else:
            return False
        
    ssh_client = paramiko.SSHClient()
    ssh_client.get_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username)
    full_command = command
    if command.startswith("sudo"):
        modified_command = full_command.replace('sudo', f'echo "{sudo_pass}" | sudo -S')
        stdin, stdout, stderr = ssh_client.exec_command(modified_command)
        with print_lock:
            output = stdout.read().decode()
            err_output = stderr.read().decode()
            if output:
                print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}\n{Fore.CYAN}{output}{Style.RESET_ALL}")
            elif err_output:
                if is_reboot_command(modified_command) == False:
                    print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}\n{Fore.CYAN}{err_output}{Style.RESET_ALL}")
            if is_reboot_command(modified_command) == True:
                print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}")
                print("Connection closed!")
    else:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        with print_lock:
            output = stdout.read().decode()
            print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}\n{Fore.CYAN}{output}{Style.RESET_ALL}")
    ssh_client.close()

def start_threads():
    threads = []
    for server in servers_data["servers"]:
        hostname = server["hostname"]
        username = server["username"]
        sudo_pass = server["sudo_pass"]
        ssh_thread = threading.Thread(target=execute_command, args=(hostname, username, args.command, sudo_pass))
        threads.append(ssh_thread)
        ssh_thread.start()
    for thread in threads:
        thread.join()
        
def count_total_servers():
    total_servers = 0    
    for _ in servers_data["servers"]:
        total_servers += 1
    print(f"{Fore.GREEN}Total servers:{Style.RESET_ALL} {Fore.YELLOW}{total_servers}{Style.RESET_ALL}")
    
start_threads()
count_total_servers()