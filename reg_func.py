import sqlite3


def registration_rules(name, surname, login, password, email):
    result = ''
    if str(name).strip() == '' or len(name) <= 1:
        result += 'Неправильный формат имени.'
    if str(surname).strip() == '' or len(surname) <= 1:
        result += 'Неправильный формат фамилии.'
    if str(login).strip() == '' or len(login) <= 4:
        result += 'Неправильный формат логина.'
    if password == 'qwerty' or password == '12345' or len(password) <= 6:
        result += 'Неверный формат пароля.'
    if '@' not in email:
        result += 'Неверный формат электронной почты'
    return result


def get_teacher_stats(cursor, login):
    for row in cursor.execute('SELECT ppl_studying, tasks_completed, tasks_created FROM teacher_stats WHERE login=?', (login, )):
        return [row[0], row[1], row[2]]
