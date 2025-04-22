# ssh-small-client
### ssh-small-client is used to run a command or multiple commands on multiple servers
**NOTE:** sudo password does not need to be provided but then you wont be able to run sudo commands
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
python ssh_client.py --command "whoami"
```
