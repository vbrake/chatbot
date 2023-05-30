import ruamel.yaml
import os

def create_yaml(output_file):
    # Verificar se o arquivo já existe e limpá-lo, se necessário
    if os.path.exists(output_file):
        with open(output_file, 'w', encoding='utf-8'):
            pass

    with open('cleandino.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    conversations = []

    for line in lines:
        line = line.strip()
        if len(line) >= 30:
            conversations.append(line)

    yml_data = {
        'frases': {
            'categories': ['frases'],
            'conversations': [
                ['- - Qual é o ensinamento do dino de hoje?']
            ] + conversations
        }
    }

    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=2, offset=0)

    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(yml_data, file)

# Example usage
output_file = input("Digite o nome do arquivo YAML de saída: ")
create_yaml(output_file)
