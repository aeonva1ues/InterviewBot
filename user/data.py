class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.answers = {}

    def set_answer(self, question_number: int, answer: str):
        self.answers[f'a{question_number}'] = answer

    def set_ending_date(self, date):
        self.date = date

    def __repr__(self):
        return f'{self.user_id}: {self.answers}'

    