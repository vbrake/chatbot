import ruamel.yaml
import os

def create_yaml(category, keywords):
    output_file = category + '.yml'

    # Verificar se o arquivo já existe e limpá-lo, se necessário
    if os.path.exists(output_file):
        with open(output_file, 'w', encoding='utf-8'):
            pass

    with open('cleandino.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    conversations = []

    for i in range(len(lines)):
        line = lines[i].strip()
        for keyword in keywords:
            if keyword in line:
                conversation = [line]
                for j in range(i+1, i+4):
                    if j < len(lines):
                        conversation.append(lines[j].strip())
                    else:
                        break
                conversations.append(conversation)
                break

    yml_data = {
        'categories': [category],
        'conversations': conversations
    }

    yaml = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=2, offset=0)

    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(yml_data, file)

# Example usage
category = input("Digite o nome da categoria: ")
keywords = input("Digite as palavras-chave separadas por vírgula: ").split(",")
create_yaml(category, keywords)
