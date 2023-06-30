import re
import emoji

def sanitize_text_file(input_file, output_file):
    # Abrir o arquivo de entrada e criar o arquivo de saída
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    sanitized_lines = []
    
    # Iterar sobre as linhas e verificar se contêm apenas um caractere, "The media is missing" ou emojis completos
    for line in lines:
        sanitized_line = emoji.replace_emoji(line, '')
        line = sanitized_line.strip()        
        
        # Verificar se a linha contém apenas um caractere, "The media is missing" ou emojis completos
        if len(line) > 1 and line != "The media is missing":
            sanitized_lines.append(sanitized_line.strip())
    
    # Escrever as linhas sanitizadas no arquivo de saída
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(sanitized_lines))

# Definir o caminho do arquivo de entrada e de saída
input_file_path = 'dino.txt'
output_file_path = 'cleandino.txt'

# Chamar a função para sanitizar o arquivo de texto
sanitize_text_file(input_file_path, output_file_path)
