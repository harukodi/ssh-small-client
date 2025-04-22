import paramiko, json, argparse
from colorama import Fore, Style

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-c", "--command", help="Command to execute on remote servers")
args = arg_parser.parse_args()

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.get_host_keys()
with open ("servers.json", "r") as servers_file:
    servers_data = json.load(servers_file)

def execute_command(command):
    for server in servers_data["servers"]:
        hostname = server["hostname"]
        username = server["username"]
        sudo_pass = server["sudo_pass"]
        ssh_client.connect(hostname=hostname, username=username)
        full_command = command
        if command.startswith("sudo"):
            modified_command = full_command.replace('sudo', f'echo "{sudo_pass}" | sudo -S')
            stdin, stdout, stderr = ssh_client.exec_command(modified_command)
            output = stdout.read().decode()
            print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}\n{Fore.CYAN}{output}{Style.RESET_ALL}")
            if output == "":
                print(f"{Fore.CYAN}Sudo password is incorrect or was not provided.{Style.RESET_ALL}")
        else:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode()
            print(f"{Fore.GREEN}Hostname:{Style.RESET_ALL} {Fore.YELLOW}{hostname}{Style.RESET_ALL}\n{Fore.CYAN}{output}{Style.RESET_ALL}")

execute_command(args.command)