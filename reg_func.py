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
    for row in cursor.execute('SELECT ppl_studying, tasks_completed, tasks_created FROM teacher_stats WHERE login=?',
                              (login,)):
        return [row[0], row[1], row[2]]


def get_student_stats(cursor, login):
    for row in cursor.execute(
            f"SELECT easy_tasks, medium_tasks, hard_tasks, tasks_completed FROM student_stats WHERE login=?", (login,)):
        return [row[0], row[1], row[2], row[3]]


def handler_file_path(path):
    if path == 'None':
        return 'К этому заданию файл не прилагается'
    else:
        mass_path = str(path).split('/')
        return [f"Файл: {mass_path[-1]}", mass_path]
