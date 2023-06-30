from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_random_response
from chatterbot.filters import get_recent_repeated_responses

app = Flask(__name__)

# Criando uma instância do ChatBot
chatbot = ChatBot(
    'Meu Chatbot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': LevenshteinDistance,
            'response_selection_method': get_random_response,
        }
    ],
    filters=[get_recent_repeated_responses],
    language='pt'
)

# Treinando o chatbot
def train_chatbot(file_path):
    trainer = ListTrainer(chatbot, show_training_progress=False)

    with open(file_path, 'r', encoding='utf-8') as file:
        conversations = file.readlines()

    num_blocks = len(conversations) // 5
    remaining_lines = len(conversations) % 5

    for i in range(num_blocks):
        conversation = [
            conversations[i*5].strip(),
            conversations[i*5+1].strip(),
            conversations[i*5+2].strip(),
            conversations[i*5+3].strip(),
            conversations[i*5+4].strip()
        ]

        trainer.train(conversation)
        print(f"Treinando bot... {i+1}/{num_blocks}")

    if remaining_lines > 0:
        start_index = num_blocks * 5
        remaining_conversation = [line.strip() for line in conversations[start_index:]]
        trainer.train(remaining_conversation)
        print(f"Treinando bot... {num_blocks+1}/{num_blocks+1}")

# Caminho para o arquivo de texto contendo as conversas
file_path = 'cleandino.txt'

# Verificar se o chatbot já foi treinado
if not chatbot.storage.count():
    # Treinando o chatbot com base no arquivo de texto
    train_chatbot(file_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('user_input')
    response = chatbot.get_response(user_input)
    return str(response.text)

def process_feedback(user_input, response, feedback):
    #print(feedback)
    if feedback.lower() in ['s', 'sim']:        
        train_chatbot_with_positive_feedback(user_input, response)
    else:
        remove_inconsistent_response(user_input, response)


def train_chatbot_with_positive_feedback(user_input, response):
    trainer = ListTrainer(chatbot, show_training_progress=False)
    trainer.train([user_input, response])


def remove_inconsistent_response(user_input, response):
    chatbot.storage.remove(response)


if __name__ == '__main__':
    app.run()
