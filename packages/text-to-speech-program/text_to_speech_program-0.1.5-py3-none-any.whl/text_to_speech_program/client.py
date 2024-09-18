#!/usr/bin/python3
import requests
import json
import sys
import os

from . import config

def send_json_from_dict(server_url,data):
    # Enviar solicitação POST ao servidor
    response = requests.post(f'{server_url}/add_task', json=data)

    if response.status_code == 200:
        print(f"Task sent successfully! ID: {response.json()['id']}")
        return response.json()['id'];
    else:
        print("Error submitting task.")
        return None

def send_json_from_file(server_url,filepath):
    # Verificar se o arquivo existe
    if not os.path.isfile(filepath):
        print(f"File {filepath} not found.")
        return None

    # Carregar o conteúdo do arquivo JSON
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error reading JSON file {filepath}.")
        return None

    return send_json_from_dict(server_url,data);


def remove_task(server_url,task_id):
    # Enviar solicitação DELETE ao servidor
    response = requests.delete(f'{server_url}/remove_task/{task_id}')

    if response.status_code == 200:
        print(response.json()["message"])
        return response.json()["message"]
    else:
        print("Error removing task:",task_id)
        return None


help_string = '''
Use: tts-program-client <command> <arguments>

Commands without argument:
    port
    
        Returns the port of server.
    
    host
    
        Returns the host of server.

    config
        
        Returns the config file path.
        
    help
    
        Returns this help.

Commands with argument:
    
    send <path_of_json_file>
        
        Sent to server the information of json file <path_of_json_file>.
    
    senddict \"{dict_python_code}\"
        
        Sent to server the information of dict \"{dict_python_code}\".
    
    remove <ID>
    
        Removes of server the task with the indentifier <ID>.

examples
    
    tts-program-client host
    tts-program-client port
    tts-program-client config
    tts-program-client senddict '{\"text\":\"Hi! How are you?\",\"language\": \"en\",\"split_pattern\": [\"\\n\\n\"],\"speed\":1.25}'
    tts-program-client remove 'd9b17a60-4370-4d13-86a8-f258a37fdbf6'
'''


def main():
    Config = config.load_config();
    host = Config['host'];
    port = Config['port'];
    
    # URL do servidor
    SERVER_URL = 'http://'+host+':'+str(port);

    # Verificar o comando recebido
    if len(sys.argv) < 2:
        print(help_string);
        sys.exit(1)

    command = sys.argv[1]

    if command == "send":
        if len(sys.argv) != 3:
            print("Use: tts-program-client send <path_arquive_json>")
            sys.exit(1)

        filepath = sys.argv[2]
        send_json_from_file(SERVER_URL,filepath)

    elif command == "senddict":
        if len(sys.argv) != 3:
            print("Use: tts-program-client senddict \"{dict_code}\"")
            sys.exit(1)
        
        data_dict = json.loads(sys.argv[2])
        send_json_from_dict(SERVER_URL,data_dict)

    elif command == "remove":
        if len(sys.argv) != 3:
            print("Use: tts-program-client remove <ID>");
            sys.exit(1);

        task_id = sys.argv[2];
        remove_task(SERVER_URL,task_id);

    elif command == "host":
        print(host);
        sys.exit(1);
        
    elif command == "port":
        print(port);
        sys.exit(1);

    elif command == "config":
        config_path, _ = config.get_config_path();
        print(config_path);
        
    elif command == "help":
        print(help_string);
        
    else:
        print(help_string);

# Iniciar o servidor Flask
if __name__ == "__main__":
    main();
 
