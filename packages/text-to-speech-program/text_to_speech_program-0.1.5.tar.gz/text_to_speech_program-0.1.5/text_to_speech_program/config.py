import os
import json

CONFIG_DEFAULT = {
    "host": "0.0.0.0",
    "port": 5000
}


def get_config_path():
    home_directory = os.path.expanduser('~');
    config_directory = os.path.join(home_directory, '.config', 'text_to_speech_program');
    config_path = os.path.join(config_directory, 'config.json');
    
    return config_path, config_directory;
    
def load_config():
    """Carrega a configuração do arquivo JSON, criando-o com valores padrão se não existir."""
    
    config_path, config_directory = get_config_path();

    # Cria o diretório de configuração se não existir
    os.makedirs(config_directory, exist_ok=True);

    if not os.path.exists(config_path):
        # Cria o arquivo com valores padrão se não existir
        with open(config_path, 'w') as file:
            json.dump(CONFIG_DEFAULT, file, indent=4);
    
    # Carrega a configuração do arquivo
    with open(config_path, 'r') as file:
        config = json.load(file);
    
    # verifica se estao todos os keys
    for key, default_value in CONFIG_DEFAULT.items():
        if key not in config:
            config[key] = default_value  # Adiciona a chave se estiver ausente
        elif not isinstance(config[key], type(default_value)):
            config[key] = default_value  #
    
    
    return config
