import sys
import os
import requests
import ctypes
import psutil
from PyQt5 import QtWidgets, QtCore

FILE_ATTRIBUTE_HIDDEN = 0x2

def set_file_hidden(file_path):
    ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)

class InjectorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('(NameYourCheat) | Injector Coded By DevSound')
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(500, 400)

        self.init_ui()

    def init_ui(self):
        button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
            padding: 8px 18px;
        }
        """

        self.download_button = QtWidgets.QPushButton('Скачать DLL', self)
        self.download_button.setStyleSheet(button_style)
        self.download_button.clicked.connect(self.download_dll)

        self.inject_button = QtWidgets.QPushButton('Инжект', self)
        self.inject_button.setStyleSheet(button_style)
        self.inject_button.clicked.connect(self.inject_dll)

        self.reset_button = QtWidgets.QPushButton('Сброс DLL', self)
        self.reset_button.setStyleSheet("""
        QPushButton {
            background-color: red;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: darkred;
        }
        QPushButton:pressed {
            background-color: maroon;
            padding: 8px 18px;
        }
        """)
        self.reset_button.clicked.connect(self.reset_dll)

        self.process_list = QtWidgets.QComboBox(self)
        self.process_list.setStyleSheet("""
        QComboBox {
            padding: 5px;
            font-size: 16px;
        }
        """)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.download_button)
        vbox.addWidget(QtWidgets.QLabel('Выберите процесс для Инжекта:', self))
        vbox.addWidget(self.process_list)
        vbox.addWidget(self.inject_button)
        vbox.addWidget(self.reset_button)
        vbox.addStretch()

        self.setLayout(vbox)
        self.update_process_list()

    def update_process_list(self):
        self.process_list.clear()
        for proc in psutil.process_iter(['pid', 'name']):
            self.process_list.addItem(f"{proc.info['name']} (PID: {proc.info['pid']})", proc.info['pid'])

    def download_dll(self):
        url = "Ваша Юрл Ссылка Для Скачки dll"
        response = requests.get(url)
        documents_path = os.path.join(os.getenv('USERPROFILE'), 'Documents')
        dll_path = os.path.join(documents_path, 'CheatProcess.dll')

        try:
            with open(dll_path, 'wb') as file:
                file.write(response.content)
            set_file_hidden(dll_path)
            QtWidgets.QMessageBox.information(self, 'Успех', 'DLL успешно Установлена.')
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Нет прав.')

    def inject_dll(self):
        documents_path = os.path.join(os.getenv('USERPROFILE'), 'Documents')
        dll_path = os.path.join(documents_path, 'CheatProcess.dll')

        if not os.path.isfile(dll_path):
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'DLL не найдена. Сначала Установите DLL.')
            return

        selected_pid = self.process_list.currentData()
        if not selected_pid:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Выберите процесс для Инжекта.')
            return

        try:
            process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, selected_pid)
            if not process_handle:
                raise Exception("Не удалось получить дескриптор процесса.")

            ctypes.windll.kernel32.CloseHandle(process_handle)
            QtWidgets.QMessageBox.information(self, 'Инжект', 'DLL успешно инжектирована.')
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', f'Не удалось выполнить инжекцию: {str(e)}')

    def reset_dll(self):
        documents_path = os.path.join(os.getenv('USERPROFILE'), 'Documents')
        dll_path = os.path.join(documents_path, 'CheatProcess.dll')

        if os.path.isfile(dll_path):
            try:
                os.remove(dll_path)
                QtWidgets.QMessageBox.information(self, 'Сброс', 'DLL успешно удалена.')
            except PermissionError:
                QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Нет прав для удаления DLL.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Ошибка', 'DLL не найдена.')

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InjectorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
