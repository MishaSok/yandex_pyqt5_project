import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sqlite3
from reg_func import *
import time
import os
import student_classes
import teacher_classes

# Подключение к базе данных
data_base = sqlite3.connect('data_base.db', timeout=10)
cursor = data_base.cursor()


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.teacher_class = TeacherForm()
        self.student_form = StudentForm()
        self.register_form = RegisterForm()
        self.register_btn = QPushButton()
        self.join_btn = QPushButton()
        self.error_label = QLabel()
        self.login_line = QLineEdit()
        self.password_line = QLineEdit()
        self.initUI()
        self.setWindowTitle('test')
        uic.loadUi('ui_folder\\login_form.ui', self)
        self.register_btn.clicked.connect(self.on_register_btn)
        self.join_btn.clicked.connect(self.on_join_btn)

    def initUI(self):
        self.setGeometry(300, 400, 300, 400)
        self.setFixedSize(300, 300)

    def on_register_btn(self):
        self.register_form.show()

    def on_join_btn(self):
        login = self.login_line.text()
        if login == '':
            self.error_label.setText('Введите логин')
        else:
            password = self.password_line.text()
            if password == '':
                self.error_label.setText('Введите пароль')
            else:
                cursor.execute('SELECT password FROM users WHERE login=?', (login,))
                if cursor.fetchone() is None:
                    self.error_label.setText('Такого логина не существует')
                else:
                    for row in cursor.execute('SELECT password, role FROM users WHERE login=?', (login,)):
                        if row[0] == password:
                            if row[1] == 'Преподаватель':
                                self.teacher_class.add_login(login)
                                self.teacher_class.show()
                                self.close()
                            else:
                                self.student_form.add_login(login)
                                self.student_form.show()
                                self.close()
                        else:
                            self.error_label.setText('Неверный пароль. Попробуйте снова')


class RegisterForm(QDialog):
    def __init__(self):
        super().__init__()
        self.register_button = QPushButton()
        self.cancel_button = QPushButton()
        self.req_btn = QPushButton()
        self.initUI()
        self.reqregform = ReqRegForm()
        uic.loadUi('ui_folder\\register_form.ui', self)

        # Регистрация нажатий
        self.register_button.clicked.connect(self.on_reg_btn)
        self.cancel_button.clicked.connect(self.on_cancel_btn)
        self.req_btn.clicked.connect(self.on_req_btn)

    def initUI(self):
        self.setGeometry(800, 500, 300, 300)
        self.setFixedSize(300, 330)

    def on_reg_btn(self):
        name = self.lineEdit.text()
        surname = self.lineEdit_2.text()
        login = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        email = self.lineEdit_5.text()
        role = self.comboBox.currentText()
        errors = registration_rules(name, surname, login, password, email)
        if errors == '':
            cursor.execute(f'SELECT login from users where login="{login}"')
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO users VALUES ('{name}', '{surname}', '{login}', '{password}', '{email}', '{role}', 0)")
                data_base.commit()
                if role == "Преподаватель":
                    cursor.execute(f"INSERT INTO teacher_stats VALUES ('{login}', 0, 0, 0)")
                    data_base.commit()
                elif role == 'Ученик':
                    cursor.execute(f"INSERT INTO student_stats VALUES ('{login}', 0, 0, 0, 0)")
                    data_base.commit()
                self.close()
            else:
                print('Такой логин уже существует')
        else:
            self.reqregform.show()
            print('Ошибка регистрации:', errors)

    def on_cancel_btn(self):
        self.close()

    def on_req_btn(self):
        self.reqregform.show()


class ReqRegForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ok_btn = QPushButton()
        uic.loadUi('ui_folder\\req_form.ui', self)
        self.ok_btn.clicked.connect(self.on_ok_btn)

    def initUI(self):
        self.setGeometry(800, 500, 300, 300)
        self.setFixedSize(300, 330)

    def on_ok_btn(self):
        self.close()


class TeacherForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_student_form = AddStudentForm()
        self.add_student_btn = QPushButton()
        self.checking_task_form = CheckingTaskForm()
        self.create_task_form = CreateTaskForm()
        self.kick_student_btn = QPushButton()
        self.create_kick_form = KickStudentForm()
        self.login_label = QLabel()
        self.look_res_btn = QPushButton()
        self.label_2 = QLabel()
        self.label_3 = QLabel()
        self.label_5 = QLabel()
        self.label_6 = QLabel()
        self.label_7 = QLabel()
        self.create_task_btn = QPushButton()
        self.initUI()
        uic.loadUi('ui_folder\\teacher_form.ui', self)
        self.label = QLabel()
        self.add_student_btn.clicked.connect(self.on_add_student_btn)
        self.create_task_btn.clicked.connect(self.on_create_task_btn)
        self.kick_student_btn.clicked.connect(self.on_kick_student_btn)
        self.look_res_btn.clicked.connect(self.on_checking_task_form)

    def initUI(self):
        self.setGeometry(300, 400, 500, 500)
        self.setFixedSize(600, 300)

    def add_login(self, login):
        for row in cursor.execute('SELECT name, surname, password, email, role FROM users where login=?', (login,)):
            self.name, self.surname, self.login, self.password, \
            self.email, self.role = row[0], row[1], login, row[2], row[3], row[4]
        self.login_label.setText(self.login)
        self.label_2.setText(f'{self.name} {self.surname}')
        self.label_3.setText(f'{self.role}')
        self.update_teacher_stats()

    def update_teacher_stats(self):
        A = get_teacher_stats(cursor, self.login)
        self.label_5.setText(f'Учеников учится: {A[0]}')
        self.label_6.setText(f'Заданий выполнено: {A[1]}')
        self.label_7.setText(f'Заданий задано: {A[2]}')

    def on_add_student_btn(self):
        self.update_teacher_stats()
        self.add_student_form.initialization(self.login)
        self.add_student_form.show()

    def on_create_task_btn(self):
        self.update_teacher_stats()
        self.create_task_form.show()
        self.create_task_form.initialization(self.login)

    def on_kick_student_btn(self):
        self.update_teacher_stats()
        self.create_kick_form.show()
        self.create_kick_form.initialization(self.login)

    def on_checking_task_form(self):
        self.update_teacher_stats()
        self.checking_task_form.initialization(self.login)
        self.checking_task_form.show()

class AddStudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.listWidget = QListWidget()
        self.add_btn = QPushButton()
        self.close_btn = QPushButton()
        uic.loadUi('ui_folder\\add_student_form.ui', self)
        self.initUI()
        self.close_btn.clicked.connect(self.on_close_btn)
        self.add_btn.clicked.connect(self.on_add_btn)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(340, 300)

    def initialization(self, login):
        self.login = login
        for row in cursor.execute("SELECT name, surname, login FROM users WHERE role='Ученик' AND have_teacher=0"):
            self.listWidget.addItem(f"{row[0]} {row[1]} ({row[2]})")
            print(row)

    def on_close_btn(self):
        self.listWidget.clear()
        self.close()

    def on_add_btn(self):
        try:
            self.student = self.listWidget.currentItem().text()
            res = str(self.student).split()[2].replace(')', '').replace('(', '')
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS teacher_{self.login}(
            student_login TEXT,
            student_name TEXT,
            student_surname TEXT);
            ''')
            data_base.commit()
            cursor.execute(f"INSERT INTO teacher_{self.login} VALUES ('{res}', '{str(self.student).split()[0]}', "
                           f"'{str(self.student).split()[1]}')")
            data_base.commit()
            cursor.execute(f"UPDATE users SET have_teacher=1, teacher_login='{self.login}' WHERE login='{res}'")
            data_base.commit()
            for row in cursor.execute(f"SELECT ppl_studying FROM teacher_stats WHERE login='{self.login}'"):
                stat = int(row[0])
            cursor.execute(f"UPDATE teacher_stats SET ppl_studying={int(stat) + 1} WHERE login='{self.login}'")
            data_base.commit()
            self.listWidget.clear()
            self.initialization(self.login)
        except Exception as Error:
            print(Error)


class CreateTaskForm(QDialog):
    def __init__(self):
        super().__init__()
        self.task_text_edit = QPlainTextEdit()
        self.delete_file_btn = QPushButton()
        self.choose_file_btn = QPushButton()
        self.lineEdit = QLineEdit()
        self.errors_label = QLabel()
        self.add_task_btn = QPushButton()
        self.close_btn = QPushButton()
        self.comboBox = QComboBox()
        self.fname = 'fname'
        self.initUI()
        uic.loadUi('ui_folder\\create_task_form.ui', self)
        self.choose_file_btn.clicked.connect(self.on_choose_file_btn)
        self.delete_file_btn.clicked.connect(self.on_delete_file_btn)
        self.close_btn.clicked.connect(self.on_close_btn)
        self.add_task_btn.clicked.connect(self.on_create_task_btn)

    def initUI(self):
        self.setGeometry(300, 400, 500, 500)
        self.setFixedSize(270, 355)

    def initialization(self, login):
        self.login = login

    def on_choose_file_btn(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        self.fname = fname
        if str(fname).strip() == '':
            self.errors_label.setText('Файл не был выбран')
        else:
            self.errors_label.setText(f'Выбран файл: {str(fname)}')

    def on_delete_file_btn(self):
        if self.fname == 'fname':
            self.errors_label.setText('Файл не был выбран.')
        else:
            self.fname = 'fname'
            self.errors_label.setText('Файл был удален.')

    def on_close_btn(self):
        self.close()

    def on_create_task_btn(self):
        try:
            if self.fname == 'fname':
                fname = None
            else:
                fname = self.fname
            diff = self.comboBox.currentText()
            if self.fname == 'fname' and self.task_text_edit.toPlainText() == '':
                self.errors_label.setText('Задание не может быть пустым.')
            elif self.lineEdit.text() == '':
                self.errors_label.setText('Укажите название для задания.')
            else:
                cursor.execute(f"SELECT task_text FROM tasks WHERE task_name='{self.lineEdit.text()}'")
                if cursor.fetchone() is None:
                    cursor.execute(
                        f"INSERT INTO tasks VALUES ('{self.login}', '{self.lineEdit.text()}', '{self.task_text_edit.toPlainText()}', '{fname}', "
                        f"'{diff}', 0, NULL)")
                    data_base.commit()
                    for row in cursor.execute(f"SELECT tasks_created FROM teacher_stats WHERE login='{self.login}'"):
                        stat = int(row[0])
                    cursor.execute(f"UPDATE teacher_stats SET tasks_created={stat + 1} WHERE login='{self.login}'")
                    data_base.commit()
                    self.task_text_edit.setPlainText('')
                    self.fname = 'fname'
                    self.errors_label.setText('Ошибок не обнаружено.')
                    self.close()
                else:
                    self.errors_label.setText('Название для задания занято.')
        except Exception as Error:
            self.errors_label.setText(f'Ошибка {Error}')
            print(f'Method error: {Error}')


class KickStudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.close_btn = QPushButton()
        self.kick_btn = QPushButton()
        self.listWidget = QListWidget()
        uic.loadUi('ui_folder\\kick_student_form.ui', self)
        self.initUI()
        self.close_btn.clicked.connect(self.on_close_btn)
        self.kick_btn.clicked.connect(self.on_kick_btn)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(340, 300)

    def initialization(self, login):
        self.login = login
        for row in cursor.execute(f"SELECT student_login, student_name, student_surname FROM teacher_{self.login}"):
            self.listWidget.addItem(f"{row[1]} {row[2]} ({row[0]})")
            print(row)

    def on_close_btn(self):
        self.listWidget.clear()
        self.close()

    def on_kick_btn(self):
        self.student = self.listWidget.currentItem().text()
        res = str(self.student).split()[2].replace(')', '').replace('(', '')
        cursor.execute(f"DELETE FROM teacher_{self.login} WHERE student_login='{res}'")
        for row in cursor.execute(f"SELECT ppl_studying FROM teacher_stats WHERE login='{self.login}'"):
            stat = int(row[0])
        cursor.execute(f"UPDATE teacher_stats SET ppl_studying={stat - 1} WHERE login='{self.login}'")
        data_base.commit()
        cursor.execute(f"UPDATE users SET have_teacher=0, teacher_login=NULL WHERE login='{res}'")
        data_base.commit()
        self.listWidget.clear()
        self.initialization(self.login)


class StudentForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.choose_task_form = ChooseTaskForm()
        self.look_tasks_btn = QPushButton()
        self.completed_tasks_btn = QPushButton()
        self.label_2 = QLabel()
        self.label_3 = QLabel()
        self.login_label = QLabel()
        self.label_5 = QLabel()
        self.label_6 = QLabel()
        self.label_7 = QLabel()
        self.label_8 = QLabel()
        self.initUI()
        uic.loadUi('ui_folder\\student_form.ui', self)
        self.look_tasks_btn.clicked.connect(self.on_choose_task_form)

    def initUI(self):
        self.setGeometry(300, 400, 500, 500)
        self.setFixedSize(600, 300)

    def add_login(self, login):
        for row in cursor.execute('SELECT name, surname, password, email, role FROM users where login=?', (login,)):
            self.name, self.surname, self.login, self.password, \
            self.email, self.role = row[0], row[1], login, row[2], row[3], row[4]
        self.login_label.setText(self.login)
        self.label_2.setText(f'{self.name} {self.surname}')
        self.label_3.setText(f'{self.role}')
        self.update_student_stats()

    def update_student_stats(self):
        A = get_student_stats(cursor, self.login)
        self.label_5.setText(f'Всего заданий выполнено: {A[3]}')
        self.label_8.setText(f'Легких заданий выполнено: {A[0]}')
        self.label_7.setText(f'Средних заданий выполнено: {A[1]}')
        self.label_6.setText(f'Сложных заданий выполнено: {A[2]}')

    def on_choose_task_form(self):
        self.update_student_stats()
        self.choose_task_form.listWidget.clear()
        self.choose_task_form.initialization(self.login)
        self.choose_task_form.show()


class ChooseTaskForm(QWidget):
    def __init__(self):
        super().__init__()
        self.task_form = Task()
        self.close_btn = QPushButton()
        self.open_task_btn = QPushButton()
        self.update_btn = QPushButton()
        self.listWidget = QListWidget()
        self.comboBox = QComboBox()
        uic.loadUi('ui_folder\\choose_task_form.ui', self)
        self.initUI()
        self.close_btn.clicked.connect(self.on_close_btn)
        self.update_btn.clicked.connect(self.on_update_btn)
        self.open_task_btn.clicked.connect(self.on_open_task_btn)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(275, 340)

    def initialization(self, login):
        self.login = login
        for row in cursor.execute(f"SELECT teacher_login FROM users WHERE login='{login}'"):
            self.teacher_login = row[0]
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS student_{login}(
                    task_id INTEGER,
                    teacher_login TEXT,
                    is_completed INTEGER,
                    task_text TEXT,
                    file_path TEXT,
                    task_name TEXT);
                    ''')
        data_base.commit()
        for task in cursor.execute(
                f"SELECT task_name, task_diff FROM tasks WHERE teacher_login='{self.teacher_login}' AND task_closed=0"):
            self.listWidget.addItem(f'{task[0]} ({task[1]})')

    def on_close_btn(self):
        self.listWidget.clear()
        self.close()

    def on_update_btn(self):
        self.listWidget.clear()
        if 'Все' in str(self.comboBox.currentText()):
            for task in cursor.execute(
                    f"SELECT task_name, task_diff FROM tasks WHERE teacher_login='{self.teacher_login}' AND task_closed=0"):
                self.listWidget.addItem(f'{task[0]} ({task[1]})')
        elif 'легкие' in str(self.comboBox.currentText()):
            for task in cursor.execute(
                    f"SELECT task_name, task_diff FROM tasks WHERE teacher_login='{self.teacher_login}' AND task_closed=0 AND task_diff='Легкий'"):
                self.listWidget.addItem(f'{task[0]} ({task[1]})')
        elif 'средние' in str(self.comboBox.currentText()):
            for task in cursor.execute(
                    f"SELECT task_name, task_diff FROM tasks WHERE teacher_login='{self.teacher_login}' AND task_closed=0 AND task_diff='Средний'"):
                self.listWidget.addItem(f'{task[0]} ({task[1]})')
        elif 'сложные' in str(self.comboBox.currentText()):
            for task in cursor.execute(
                    f"SELECT task_name, task_diff FROM tasks WHERE teacher_login='{self.teacher_login}' AND task_closed=0 AND task_diff='Сложный'"):
                self.listWidget.addItem(f'{task[0]} ({task[1]})')
        else:
            pass

    def on_open_task_btn(self):
        self.text = self.listWidget.currentItem().text()
        self.залупiвка = str(self.text).split()[0]
        for row in cursor.execute(f"SELECT id FROM tasks WHERE task_name='{self.залупiвка}'"):
            task_id = row[0]

        self.task_form.initialization(self.login, task_id, self.залупiвка)
        self.task_form.show()


class Task(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = 'fname'

        self.label = QLabel()
        self.choose_file_btn = QPushButton()
        self.close_btn = QPushButton()
        self.complete_task_btn = QPushButton()
        self.delete_file_btn = QPushButton()
        self.plainTextEdit = QPlainTextEdit()
        self.task_name_label = QLabel()
        self.task_text = QPlainTextEdit()
        self.teacher_label = QLabel()
        self.diff_label = QLabel()
        self.download_file_btn = QPushButton()

        self.initUI()
        self.download_file_btn.clicked.connect(self.on_download_file_btn)
        self.choose_file_btn.clicked.connect(self.on_choose_file_btn)
        self.delete_file_btn.clicked.connect(self.on_delete_file_btn)
        self.close_btn.clicked.connect(self.on_close_btn)
        self.complete_task_btn.clicked.connect(self.on_completed_task_btn)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(590, 410)
        uic.loadUi('ui_folder\\task.ui', self)
        self.task_text.setReadOnly(True)

    def initialization(self, login, task_id, task_name):
        self.login = login
        self.task_id = task_id
        self.task_name = task_name
        self.task_name_label.setText(f'Задание: "{self.task_name}"')
        for row in cursor.execute(f"SELECT task_diff FROM tasks WHERE task_name='{self.task_name}'"):
            self.task_diff = row[0]
        self.diff_label.setText(f'Уровень сложности: {self.task_diff}')
        for row in cursor.execute(f"SELECT teacher_login FROM users WHERE login='{self.login}'"):
            self.teacher_login = row[0]
            for stat in cursor.execute(f"SELECT name, surname FROM users WHERE login='{self.teacher_login}'"):
                self.teacher_name = stat[0]
                self.teacher_surname = stat[1]
            self.teacher_label.setText(f"Преподаватель: {self.teacher_name} {self.teacher_surname}")
        for row in cursor.execute(f"SELECT task_text FROM tasks WHERE task_name='{self.task_name}'"):
            self.task_text_obj = row[0]
            self.task_text.setPlainText(self.task_text_obj)
        for row in cursor.execute(f"SELECT task_file FROM tasks WHERE task_name='{self.task_name}'"):
            self.file_path = row[0]

    def on_download_file_btn(self):
        res = handler_file_path(self.file_path)[0]
        self.label.setText(res)
        print('test')
        path = '\\'.join((handler_file_path(self.file_path)[1])[0:-1])
        print(path)
        path = os.path.realpath(path)
        os.startfile(path)

    def on_choose_file_btn(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        self.file_path = fname
        res = str(self.file_path).split('/')[-1]
        print(str(self.file_path).strip())
        if str(fname).strip() == '':
            self.label.setText('Файл не был выбран')
        else:
            self.label.setText(f'Прикреплен файл: {res}')

    def on_delete_file_btn(self):
        if self.file_path == 'fname':
            self.label.setText('Файл не был выбран.')
        else:
            self.file_path = 'fname'
            self.label.setText('Файл был удален.')

    def on_close_btn(self):
        self.plainTextEdit.clear()
        self.task_text.clear()
        self.file_path = 'fname'
        self.label.setText('Ошибок не обнаружено.')
        self.close()

    def on_completed_task_btn(self):
        try:
            if self.plainTextEdit.toPlainText() == '' and self.file_path == 'fname':
                self.label.setText('Вы не можете сдать пустое задание.')
            else:
                cursor.execute(f"SELECT task_id FROM student_{self.login} WHERE task_id={self.task_id}")
                if cursor.fetchone() is None:
                    cursor.execute(
                        f"INSERT INTO student_{self.login} VALUES ({self.task_id}, '{self.teacher_login}', 0, '{self.plainTextEdit.toPlainText()}', '{self.file_path}')")
                    data_base.commit()
                    self.plainTextEdit.clear()
                    self.task_text.clear()
                    self.file_path = 'fname'
                    self.label.setText('Ошибок не обнаружено.')
                    self.close()
                else:
                    self.label.setText('Вы уже выполнили это задание.')
        except Exception as Error:
            print(Error)


class CheckingTaskForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.comboBox = QComboBox()
        self.update_btn = QPushButton()
        self.listWidget = QListWidget()
        self.check_task_btn = QPushButton()
        self.close_btn = QPushButton()
        self.initUI()

    def initUI(self):
        uic.loadUi('ui_folder\\checking_tasks_form.ui', self)
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(280, 340)

    def initialization(self, login):
        try:
            self.login = login
            cursor.execute(f"SELECT login FROM users WHERE teacher_login='{self.login}'")
            if cursor.fetchone() is None:
                pass
            else:
                mass = []
                for row in cursor.execute(f"SELECT login FROM users WHERE teacher_login='{self.login}'"):
                    mass.append(row[0])

        except Exception as Error:
            print(Error)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginForm()
    ex.show()
    sys.exit(app.exec())
