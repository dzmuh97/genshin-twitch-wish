import os

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel

from PyQt5 import QtGui, uic

from config import _msg

from typing import Tuple, Any


class ErrorMessage(QMessageBox):
    def __init__(self, **kwargs):
        error_text = kwargs.get('error', '{error}')
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(_msg('ui_error'))
        self.setText(error_text)


class InfoMessage(QMessageBox):
    def __init__(self, **kwargs):
        error_text = kwargs.get('info', '{error}')
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_msg('ui_info'))
        self.setText(error_text)


class QuestionMessage(QMessageBox):
    def __init__(self, **kwargs):
        title_text = kwargs.get('title', '{error}')
        window_text = kwargs.get('text', '{error}')

        super().__init__()

        self.setIcon(QMessageBox.Question)
        self.setWindowTitle(title_text)
        self.setText(window_text)

        yes_button = QPushButton(_msg('ui_yes'))
        no_button = QPushButton(_msg('ui_no'))

        self.addButton(yes_button, QMessageBox.YesRole)
        self.addButton(no_button, QMessageBox.NoRole)


class UpdateMessage(QMessageBox):
    def __init__(self, **kwargs):
        cur_version = kwargs.get('cur', '{error}')
        new_version = kwargs.get('new', '{error}')

        super().__init__()

        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(_msg('ui_update_title'))
        self.setText(_msg('ui_update_message'))
        self.setInformativeText(_msg('ui_update_message_version') % (cur_version, new_version))


class TwitchUsernameRequest(QWidget):
    def __init__(self, **kwargs):
        self._window_result = None
        super().__init__()
        ui_path = os.path.join('ui', 'twitch_username_request.ui')
        uic.loadUi(ui_path, self)
        self.setWindowTitle(_msg('ui_twitch_auth'))

        self.ok_button: QPushButton
        self.channel_name_hint: QLabel

        self.channel_name_hint.setText(_msg('auth_channel_promt'))
        self.ok_button.clicked.connect(self._submit)

    def _submit(self):
        self.channel_name_text: QLineEdit
        twitch_username = self.channel_name_text.text()

        if '/' in twitch_username:
            show_ui_window(ErrorMessage, error=_msg('auth_channel_error_name'))
            return

        self._window_result = twitch_username
        self.close()


def show_ui_window(wcls, **kwargs) -> Tuple[bool, Any]:
    is_first = False
    app = QApplication.instance()
    if app is None:
        is_first = True
        app = QApplication([])

    window = wcls(**kwargs)
    if (not is_first) and (not isinstance(window, QMessageBox)):
        raise NotImplementedError

    window.setWindowIcon(QtGui.QIcon('icon.png'))

    window.show()
    if isinstance(window, QMessageBox):
        window_result = window.exec()

        if window_result in (QMessageBox.AcceptRole, QMessageBox.Yes, QMessageBox.Ok):
            app_result = True
        else:
            app_result = False
    else:
        app.exec()
        app_result = True

    window_data = getattr(window, '_window_result', None)

    if is_first:
        app.quit()

    return app_result, window_data


if __name__ == '__main__':
    print(show_ui_window(ErrorMessage, error='CRITICAL ERROR'))
