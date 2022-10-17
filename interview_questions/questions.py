# Каждая строка, используемая для отправки ботом имеет в начале УНИКАЛЬНЫЙ тэг
# в формате [TAG]::::.
from . import interview_txt_path


# Функция get_question возвращает строку по заданному тэгу.
def get_question(tag: str) -> str:
    assert tag[0].strip() == '[' and tag[-1].strip() == ']', \
                    'Тэг должен быть заключен в скобки'
    with open(interview_txt_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    for line in content:
        if line.startswith(f'{tag}'):
            return line.split('::::')[1].replace('\\n', '\n')
    raise ValueError(f'Вопрос с данным тэгом не найден: {tag}')