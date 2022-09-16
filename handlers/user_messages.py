from . import bot
from interview_questions.questions import get_question
from keyboards.default_keyboards import start_keyboard, first_question_keyboard
from user.data import User


@bot.message_handler(commands=['start'])
def start_message(message):
    # Приветствующее сообщение. Пользователю предлагается две кнопки: пройти тест или узнать подробности о проекте. 
    bots_message = get_question('[START]')
    bot.send_message(message.chat.id, bots_message, reply_markup=start_keyboard)


@bot.message_handler(content_types=['text'])
def first_question(message):
    if message.text == '🟩 Пройти опрос 🟩':
        user = User(message.from_user.id)
        bots_message = get_question('[FIRST_QUESTION]')
        bot.register_next_step_handler(bot.send_message(message.chat.id, bots_message, reply_markup=first_question_keyboard), second_question, user)

def second_question(message, user):
    user.set_answer(1, message.text)
    print(user.answers)