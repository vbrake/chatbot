from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_random_response
from chatterbot.filters import get_recent_repeated_responses
import pickle

def get_feedback():
    text = input()
    if 's' in text.lower():
        return True
    elif 'n' in text.lower():
        return False
    else:
        print('Digite \"s\" or \"n\"')
        return get_feedback()

# Cria um chatbot
chatbot = ChatBot('Meu Chatbot',
                  logic_adapters=[
                      {
                          "import_path": "chatterbot.logic.BestMatch",
                          'statement_comparison_function': LevenshteinDistance,
                          'response_selection_method': get_random_response,
                      }
                  ],
                  filters=[get_recent_repeated_responses],
                  language='PT'
                  )

# Carrega o arquivo de texto com as mensagens
with open('cleandino.txt', 'r', encoding='utf-8') as file:
    conversas = file.readlines()

# Treina o chatbot com as mensagens
trainer = ListTrainer(chatbot)
trainer.train("chatterbot.corpus.dino")

# Salva o modelo treinado
with open('chatbot_model.pkl', 'wb') as file:
    pickle.dump(chatbot, file)

# Testa o chatbot
while True:
    pergunta = input('Eu: ')
    resposta = chatbot.get_response(pergunta)
    print('Dino: ', resposta)
    print('Dino: Foi uma boa resposta?')
    feedback = get_feedback()
    if feedback:
        print('Dino: Obrigado por me ajudar a melhorar!')
        trainer.train([pergunta, resposta])
