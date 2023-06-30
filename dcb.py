import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import random

# Carregar o modelo treinado
model = tf.keras.models.load_model('dinobot_model')

# Carregar o arquivo com o mapeamento das palavras para índices
tokenizer = tf.keras.preprocessing.text.Tokenizer()

# Ajustar o word_index para conter apenas palavras até o índice 286121
tokenizer.word_index = {key: value for key, value in tokenizer.word_index.items() if value <= 286121}

# Ajustar o mapeamento de índices para palavras do tokenizer
tokenizer.index_word = {value: key for key, value in tokenizer.word_index.items()}

# Definir o valor de max_length
max_length = 286121

# Função para gerar resposta aleatória do chatbot
def generate_response(input_text, model, tokenizer, max_length):
    # Preprocessamento do texto de entrada
    input_sequence = tokenizer.texts_to_sequences([input_text])[0]
    input_sequence = np.array(pad_sequences([input_sequence], maxlen=max_length, padding='pre'))

    # Gerar a resposta do chatbot
    predicted_index = np.argmax(model.predict(input_sequence), axis=-1)[0]
    predicted_word = tokenizer.index_word.get(predicted_index)

    return predicted_word

# Obter respostas aleatórias do chatbot
def get_random_response():
    responses = ["Olá!", "Como posso ajudar?", "Estou aqui para responder suas perguntas."]
    return random.choice(responses)

# Exemplo de uso do chatbot
while True:
    user_input = input("Digite uma mensagem: ")
    
    # Verificar se o usuário digitou alguma mensagem
    if not user_input:
        print("Por favor, digite algo.")
        continue

    # Verificar se a mensagem é uma saída do usuário
    if user_input.lower() == "sair":
        print("Até mais!")
        break

    # Gerar a resposta do chatbot
    response = generate_response(user_input, model, tokenizer, max_length)

    # Se a resposta for vazia, gerar uma resposta aleatória
    if not response:
        response = get_random_response()

    print("Chatbot:", response)
