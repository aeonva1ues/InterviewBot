from datetime import datetime

from database.active_table import get_active_table_name
from database.psqlExecutor import insert_into, search_user, count
from interview_questions.questions import get_question
from keyboards.default_keyboards import (fifth_question_keyboard,
                                         first_question_keyboard,
                                         fourth_question_keyboard,
                                         hide_keyboard,
                                         second_more_question_keyboard,
                                         start_keyboard,
                                         third_question_keyboard)
from user.data import User

from . import bot


@bot.message_handler(commands=['start'])
def start_message(message):
    # Приветствующее сообщение. Пользователю предлагается две кнопки:
    # пройти тест или узнать подробности о проекте.
    bots_message = get_question('[START]')
    bot.send_message(
        message.chat.id,
        bots_message,
        reply_markup=start_keyboard
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    bots_message = get_question('[HELP]')
    return bot.send_message(
        message.chat.id,
        bots_message,
    )


@bot.message_handler(commands=['terms'])
def terms_command(message):
    file = open(r'media\Термины.txt', 'r', encoding='utf-8')
    bot.send_message(message.chat.id, file)
    file.close()


@bot.message_handler(commands=['links'])
def links_command(message):
    file = open(r'media\Ссылки.txt', 'r', encoding='utf-8')
    bot.send_message(message.chat.id, file)
    file.close()


@bot.message_handler(commands=['description'])
def description_command(message):
    bots_message = get_question('[DESCRIPTION]')
    return bot.send_message(
        message.chat.id,
        bots_message,
    )


@bot.message_handler(commands=['interview'])
def interview_command(message):
    file = open(r'media\Приложение 1.docx', 'rb')
    bot.send_message(message.chat.id, file)
    file.close()


@bot.message_handler(commands=['iresults'])
def iresults_command(message):
    db_notes_count = count(get_active_table_name())
    bots_message = get_question('[IRESULTS]') % str(db_notes_count)
    return bot.send_message(
        message.chat.id,
        bots_message,
    )


@bot.message_handler(commands=['pytpr'])
def pytpr_command(message):
    file = open(r'media\Приложение 2.docx', 'rb')
    bot.send_message(message.chat.id, file)
    file.close()


@bot.message_handler(commands=['theses'])
def theses_command(message):
    file = open(r'media\Тезисы.docx', 'rb')
    bot.send_message(message.chat.id, file)
    file.close()


@bot.message_handler(content_types=['text'])
def first_question(message):
    if message.text == '🟩 Пройти опрос 🟩':
        # Проверка на прохождение опроса ранее
        this_user_in_db = search_user(
            {
                'table_name': get_active_table_name(),
                'user_id': str(message.from_user.id)
            })
        if this_user_in_db:
            return bot.send_message(message.chat.id, (
                        'Похоже, вы уже прошли опрос. '
                        'Повторное прохождение недоступно!\n'
                        'Чтобы узнать больше о проекте используйте /help'
                    )
            )
        user = User(message.from_user.id)
        bots_message = get_question('[FIRST_QUESTION]')
        return bot.register_next_step_handler(
            bot.send_message(
                    message.chat.id,
                    bots_message,
                    reply_markup=first_question_keyboard),
            second_question,
            user)


def second_question(message, user):
    if message.text not in ['Не интересует',
                            (
                                'Когда давали задачи на уроках – решал, '
                                'но самостоятельно никогда не интересовался'),
                            (
                                'Немного заинтересован, любопытно следить '
                                'за новыми технологиями в IT-индустрии'),
                            (
                                'Заинтересован. Проходил/прохожу курсы, '
                                'читал/читаю книги и практикуюсь')
                            ]:
        return bot.register_next_step_handler(
            bot.send_message(
                message.chat.id,
                'Выберите вариант ответа из предложенных',
                reply_markup=first_question_keyboard),
            second_question,
            user)
    user.set_answer(1, message.text)
    bots_message = get_question('[SECOND_QUESTION]')
    return bot.register_next_step_handler(
        bot.send_message(
            message.chat.id,
            bots_message,
            reply_markup=hide_keyboard),
        check_second_answer,
        user)


def check_second_answer(message, user):
    user.set_answer(2, message.text)
    if message.text == '-':
        user.set_answer(21, '-')
        bots_message = get_question('[THIRD_QUESTION]')
        return bot.register_next_step_handler(
            bot.send_message(
                message.chat.id,
                bots_message,
                reply_markup=third_question_keyboard),
            third_question,
            user)
    bots_message = get_question('[SECOND+_QUESTION]')
    return bot.register_next_step_handler(
        bot.send_message(
            message.chat.id,
            bots_message,
            reply_markup=second_more_question_keyboard),
        second_more_question,
        user)


def second_more_question(message, user):
    if message.text not in [
        'Нет, только слышал название',
        'Перечислил несколько, но практиковался не на всех',
        'Да'
    ]:
        return bot.register_next_step_handler(
            bot.send_message(
                message.chat.id,
                'Выберите вариант ответа из предложенных',
                reply_markup=second_more_question_keyboard),
            second_more_question,
            user)
    user.set_answer(21, message.text)
    bots_message = get_question('[THIRD_QUESTION]')
    return bot.register_next_step_handler(
        bot.send_message(
            message.chat.id,
            bots_message,
            reply_markup=third_question_keyboard),
        third_question,
        user)


def third_question(message, user):
    if message.text not in [
        'Никак, их нет',
        'Очень слабые знания, не дотягиваю до базы',
        'Понимаю основы, так называемую базу',
        'Могу решать сложные задачи с уроков/олимпиад',
        (
            'Могу уверенно писать код для решения задач конкретного '
            'направления (backend, frontend, data science и др.)'
            )
    ]:
        return bot.register_next_step_handler(
            bot.send_message(
                message.chat.id,
                'Выберите вариант ответа из предложенных',
                reply_markup=third_question_keyboard),
            third_question,
            user)
    user.set_answer(3, message.text)
    bots_message = get_question('[FOURTH_QUESTION]')
    return bot.register_next_step_handler(
        bot.send_message(
            message.chat.id,
            bots_message,
            reply_markup=fourth_question_keyboard),
        fourth_question,
        user)


def fourth_question(message, user):
    if message.text in [
        (
            'Ничего не понимаю в этом. Информация из учебников / от '
            'учителя доходит до меня с трудом'),
        'Частичное понимание имею, но на уроках это скучно для меня',
        'Понимаю темы, которые мы изучаем. На уроках мне интересно'
    ]:
        # Переход на 5-ый вопрос
        user.set_answer(4, message.text)
        user.set_answer(41, '-')
        bots_message = get_question('[FIFTH_QUESTION]')
        bot.register_next_step_handler(
            bot.send_message(
                message.chat.id,
                bots_message,
                reply_markup=fifth_question_keyboard),
            fifth_question,
            user)
    elif message.text in [
        ('Мне интересны другие языки программирования. '
            'В школе мы их не изучали'),
        ('Мне интересна другая подача информации. Например, из книг, '
            'написанных программистами или из курсов'),
        'Мне интересны задачи для практики совершенно другого плана'
    ]:
        # Переход на 4.1 вопрос
        user.set_answer(4, message.text)
        bots_message = get_question('[FOURTH+_QUESTION]')
        bot.register_next_step_handler(
            bot.send_message(
                message.chat.id,
                bots_message,
                reply_markup=hide_keyboard),
            fourth_more_question,
            user)
    else:
        return bot.register_next_step_handler(
            bot.send_message(
                message.chat.id,
                'Выберите вариант ответа из предложенных',
                reply_markup=fourth_question_keyboard),
            fourth_question,
            user)


def fourth_more_question(message, user):
    user.set_answer(41, message.text)
    bots_message = get_question('[FIFTH_QUESTION]')
    bot.register_next_step_handler(
        bot.send_message(
            message.chat.id,
            bots_message,
            reply_markup=fifth_question_keyboard),
        fifth_question,
        user)


def fifth_question(message, user):
    user.set_answer(5, message.text)
    # Сохранение результата в бд
    insert_into({
            'table_name': get_active_table_name(),
            'tg_id': user.user_id,
            'a1': user.answers['a1'],
            'a2': user.answers['a2'],
            'a21': user.answers['a21'],
            'a3': user.answers['a3'],
            'a4': user.answers['a4'],
            'a41': user.answers['a41'],
            'a5': user.answers['a5'],
            'date': str(datetime.now())
        })
    bots_message = get_question('[LAST_MESSAGE]')
    bot.send_message(message.chat.id, bots_message, reply_markup=hide_keyboard)
