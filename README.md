# ssh-small-client
This is used to run a command or multiple commands on multiple servers
## Install preqs
```bash
pip install -r requirements.txt
```
## Create the needed json server file
```bash
touch servers.json
```
Paste this to the servers.json file
```json
{
    "servers": [
        {
            "hostname": "",
            "sudo_pass": ""
        },
        {
            "hostname": "",
            "sudo_pass": ""
        }
    ]
}
```
## Run the program with threading
```bash
python ssh_client_multithreaded.py --command "whoami"
```
