import os
import glob
import json
import copy

import jsonschema

from contextlib import contextmanager

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QColorDialog, QFileDialog
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QCheckBox, QSpinBox

from PyQt5 import QtGui, uic

from config import CONFIG
from config import _msg
from config import _load_json
from config import _load_text

from data import TEXT
from data import CONFIG_SCHEMA

from typing import Tuple, Any


class ErrorMessage(QMessageBox):
    def __init__(self, **kwargs):
        error_text = kwargs.get('error', '{error}')
        window_title = kwargs.get('title', None)
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle(window_title if window_title else _msg('ui_error'))
        self.setText(error_text)


class InfoMessage(QMessageBox):
    def __init__(self, **kwargs):
        error_text = kwargs.get('info', '{error}')
        window_title = kwargs.get('title', None)
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(window_title if window_title else _msg('ui_info'))
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


class UserSettings(QWidget):
    def __init__(self, **kwargs):
        self._window_result = None
        super().__init__()
        ui_path = os.path.join('ui', 'settings.ui')
        uic.loadUi(ui_path, self)

        self.ui_text = copy.deepcopy(TEXT)

        self._load_settings_to_ui()
        self._reload_ui_text()

    def _local_text(self, text_type: str) -> str:
        return self.ui_text.get(text_type, 'NULL')

    @staticmethod
    @contextmanager
    def _block_signals(obj):
        obj.blockSignals(True)
        yield obj
        obj.blockSignals(False)

    @staticmethod
    def _enumerate_bunners():
        for raw_banner in os.listdir('banners'):
            banner_filename = os.path.splitext(raw_banner)[0]
            yield banner_filename

    @staticmethod
    def _enumerate_text_files(mask, ext):
        path = os.path.join('text', '%s_*.%s' % (mask, ext))
        for raw_text in glob.glob(path):
            text_file = os.path.basename(raw_text)
            text_filename = os.path.splitext(text_file)[0]
            yield text_filename

    def _load_settings_to_ui(self):
        fields_set = (
            self.edit_window_name,
            self.combo_banner,
            self.check_send_stats,
            self.check_test_mode,
            self.check_chatbot_enabled,
            self.edit_wish_command,
            self.edit_wish_command_prefix,
            self.spin_wish_global_timeout,
            self.spin_wish_timeout,
            self.combo_wish_timeout,
            self.check_send_notify,
            self.spin_wish_count,
            self.check_self_wish,
            self.spin_self_wish_every,
            self.check_enable_colors,
            self.check_eventbot_enabled,
            self.edit_default_color,
            self.combo_revards,
            self.edit_event_name,
            self.spin_event_bot_wish_count,
            self.check_sound_enabled,
            self.edit_sound_fall,
            self.edit_sound_3star,
            self.edit_sound_4star,
            self.edit_sound_5star,
            self.combo_commands,
            self.check_command_enabled,
            self.spin_command_permissions,
            self.combo_command_permisson,
            self.check_command_permission_available,
            self.combo_language_text,
            self.combo_language_wish_items,
            self.combo_language_messages,
            self.combo_language_html_template,
            self.check_history_enabled,
            self.check_history_3star_enabled,
            self.check_history_4star_enabled,
            self.check_history_5star_enabled,
            self.edit_history_path,
            self.edit_chroma_color,
            self.check_draw_usertext,
            self.check_draw_fall,
            self.check_draw_wishes,
            self.check_draw_user_background,
            self.combo_anim_type,
            self.edit_user_background_path,
            self.spin_start_delay,
            self.combo_end_delay,
            self.spin_end_delay,
            self.combo_end_delay_multi,
            self.spin_end_delay_multi,
            self.spin_user_uid_size,
            self.spin_wish_name_size,
            self.spin_fps,
            self.edit_font_path
        )

        config_main = CONFIG
        self.edit_window_name.setText(config_main['window_name'])

        for banner_name in self._enumerate_bunners():
            self.combo_banner.addItem(banner_name)
        cur_index = self.combo_banner.findText(config_main['banner'])
        self.combo_banner.setCurrentIndex(cur_index)

        self.check_send_stats.setChecked(config_main['send_dev_stats'])
        self.check_test_mode.setChecked(config_main['test_mode'])

        config_chatbot = config_main['chat_bot']
        self.check_chatbot_enabled.setChecked(config_chatbot['enabled'])
        self.edit_wish_command.setText(config_chatbot['wish_command'])
        self.edit_wish_command_prefix.setText(config_chatbot['wish_command_prefix'])
        self.spin_wish_global_timeout.setValue(config_chatbot['wish_global_timeout'])

        def _combo_wish_timeout_change():
            current_wish_timeout_usertype = self.combo_wish_timeout.currentText()
            user_wish_timeout_config = config_chatbot['wish_timeout']

            with self._block_signals(self.spin_wish_timeout):
                self.spin_wish_timeout.setValue(user_wish_timeout_config[current_wish_timeout_usertype])

        for wish_timeout_usertype in config_chatbot['wish_timeout']:
            self.combo_wish_timeout.addItem(wish_timeout_usertype)
        self.combo_wish_timeout.setCurrentIndex(0)
        self.combo_wish_timeout.currentIndexChanged.connect(_combo_wish_timeout_change)
        _combo_wish_timeout_change()

        self.check_send_notify.setChecked(config_chatbot['send_notify'])
        self.spin_wish_count.setValue(config_chatbot['wish_count'])
        self.check_self_wish.setChecked(config_chatbot['self_wish'])
        self.spin_self_wish_every.setValue(config_chatbot['self_wish_every'])
        self.check_enable_colors.setChecked(config_chatbot['enable_colors'])

        config_event_bot = config_main['event_bot']
        self.check_eventbot_enabled.setChecked(config_event_bot['enabled'])

        def _tool_color_click(field_to_change):
            def _color_pick():
                color = QColorDialog.getColor()
                color_name_html = color.name().upper()
                field_to_change.setText(color_name_html)
            return _color_pick

        self.edit_default_color.setText(config_event_bot['default_color'])
        self.tool_default_color.clicked.connect(_tool_color_click(self.edit_default_color))

        def _user_event_reward_change():
            user_event_rewards = config_event_bot['rewards']
            current_user_event_reward_index = self.combo_revards.currentIndex()
            user_event_reward = user_event_rewards[current_user_event_reward_index]

            with self._block_signals(self.edit_event_name), self._block_signals(self.spin_event_bot_wish_count):
                self.edit_event_name.setText(user_event_reward['event_name'])
                self.spin_event_bot_wish_count.setValue(user_event_reward['wish_count'])

        for i, event_reward in enumerate(config_event_bot['rewards']):
            self.combo_revards.addItem('Event#%d' % (i + 1))
        self.combo_revards.setCurrentIndex(0)
        self.combo_revards.currentIndexChanged.connect(_user_event_reward_change)
        _user_event_reward_change()

        config_sound = config_main['sound']
        self.check_sound_enabled.setChecked(config_sound['enabled'])

        def _file_click(field_to_change, file_type):
            def _file_pick():
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                filepath, _ = QFileDialog.getOpenFileName(self, 'Select %s file' % file_type, '', 'All Files (*)', options=options)
                if not filepath:
                    return
                filename = os.path.basename(filepath)
                field_to_change.setText(filename)
            return _file_pick

        self.tool_sound_fall.clicked.connect(_file_click(self.edit_sound_fall, 'Audio'))
        self.tool_sound_3star.clicked.connect(_file_click(self.edit_sound_3star, 'Audio'))
        self.tool_sound_4star.clicked.connect(_file_click(self.edit_sound_4star, 'Audio'))
        self.tool_sound_5star.clicked.connect(_file_click(self.edit_sound_5star, 'Audio'))
        self.edit_sound_fall.setText(config_sound['fall'])
        self.edit_sound_3star.setText(config_sound['3'])
        self.edit_sound_4star.setText(config_sound['4'])
        self.edit_sound_5star.setText(config_sound['5'])

        config_gbot = config_main['gbot_config']

        def _combo_gbot_command_permission():
            current_gbot_command = self.combo_commands.currentText()
            current_command_permissions = config_gbot[current_gbot_command]['permissions']
            current_gbot_permission = self.combo_command_permisson.currentText()

            if not current_gbot_permission:
                return

            is_permission_available = current_command_permissions[current_gbot_permission]

            with self._block_signals(self.check_command_permission_available):
                self.check_command_permission_available.setChecked(is_permission_available)

        def _combo_gbot_commands():
            current_gbot_command = self.combo_commands.currentText()
            gbot_command_config = config_gbot[current_gbot_command]

            with self._block_signals(self.check_command_enabled), self._block_signals(self.spin_command_permissions):
                self.check_command_enabled.setChecked(gbot_command_config['enabled'])
                self.spin_command_permissions.setValue(gbot_command_config['timeout'])

            self.combo_command_permisson.clear()
            for gbot_permission in gbot_command_config['permissions']:
                self.combo_command_permisson.addItem(gbot_permission)
            self.combo_command_permisson.setCurrentIndex(0)

        for gbot_command in config_gbot:
            self.combo_commands.addItem(gbot_command)
        self.combo_commands.setCurrentIndex(0)
        self.combo_commands.currentIndexChanged.connect(_combo_gbot_commands)
        self.combo_command_permisson.currentIndexChanged.connect(_combo_gbot_command_permission)
        _combo_gbot_commands()

        config_language = config_main['language']

        for text_file in self._enumerate_text_files('text', 'json'):
            self.combo_language_text.addItem(text_file)
        cur_index = self.combo_language_text.findText(config_language['text'])
        self.combo_language_text.setCurrentIndex(cur_index)

        for items_file in self._enumerate_text_files('items', 'json'):
            self.combo_language_wish_items.addItem(items_file)
        cur_index = self.combo_language_wish_items.findText(config_language['wish_items'])
        self.combo_language_wish_items.setCurrentIndex(cur_index)

        for messages_file in self._enumerate_text_files('messages', 'json'):
            self.combo_language_messages.addItem(messages_file)
        cur_index = self.combo_language_messages.findText(config_language['messages'])
        self.combo_language_messages.setCurrentIndex(cur_index)

        for html_file in self._enumerate_text_files('history', 'html'):
            self.combo_language_html_template.addItem(html_file)
        cur_index = self.combo_language_html_template.findText(config_language['html_template'])
        self.combo_language_html_template.setCurrentIndex(cur_index)

        config_history = config_main['history_file']
        self.check_history_enabled.setChecked(config_history['enabled'])
        self.check_history_3star_enabled.setChecked(config_history['3'])
        self.check_history_4star_enabled.setChecked(config_history['4'])
        self.check_history_5star_enabled.setChecked(config_history['5'])

        self.edit_history_path.setText(config_history['path'])
        self.tool_history_path.clicked.connect(_file_click(self.edit_history_path, 'History'))

        config_animations = config_main['animations']
        self.edit_chroma_color.setText(config_animations['chroma_color'])
        self.tool_chroma_color.clicked.connect(_tool_color_click(self.edit_chroma_color))

        config_animations_states = config_animations['draw_states']
        self.check_draw_usertext.setChecked(config_animations_states['draw_usertext'])
        self.check_draw_fall.setChecked(config_animations_states['draw_fall'])
        self.check_draw_wishes.setChecked(config_animations_states['draw_wishes'])

        config_animations_user_background = config_animations['user_background']
        self.check_draw_user_background.setChecked(config_animations_user_background['enabled'])

        for user_background_type in ('static', 'gif'):
            self.combo_anim_type.addItem(user_background_type)
        cur_index = self.combo_anim_type.findText(config_animations_user_background['type'])
        self.combo_anim_type.setCurrentIndex(cur_index)

        self.edit_user_background_path.setText(config_animations_user_background['path'])
        self.tool_user_background_path.clicked.connect(_file_click(self.edit_user_background_path, 'Background'))

        self.spin_start_delay.setValue(config_animations['start_delay'])
        self.spin_fps.setValue(config_animations['fps'])

        config_animations_end_delay = config_animations['end_delay']

        for end_delay in config_animations_end_delay:
            self.combo_end_delay.addItem(end_delay)
        self.combo_end_delay.setCurrentIndex(0)

        config_animations_end_delay_multi = config_animations['end_delay_multi']

        for end_delay_multi in config_animations_end_delay_multi:
            self.combo_end_delay_multi.addItem(end_delay_multi)
        self.combo_end_delay_multi.setCurrentIndex(0)

        def _combo_anim_delay_change(get_from, from_config, set_to):
            def _anim_delay_change():
                current_anim_delay = get_from.currentText()
                anim_delay_config = from_config[current_anim_delay]
                with self._block_signals(set_to):
                    set_to.setValue(anim_delay_config)
            return _anim_delay_change

        self.combo_end_delay.currentIndexChanged.connect(_combo_anim_delay_change(self.combo_end_delay, config_animations_end_delay, self.spin_end_delay))
        self.combo_end_delay_multi.currentIndexChanged.connect(_combo_anim_delay_change(self.combo_end_delay_multi, config_animations_end_delay_multi, self.spin_end_delay_multi))

        _combo_anim_delay_change(self.combo_end_delay, config_animations_end_delay, self.spin_end_delay)()
        _combo_anim_delay_change(self.combo_end_delay_multi, config_animations_end_delay_multi, self.spin_end_delay_multi)()

        config_animations_font = config_animations['font']
        self.spin_user_uid_size.setValue(config_animations_font['user_uid_size'])
        self.spin_wish_name_size.setValue(config_animations_font['wish_name_size'])

        self.edit_font_path.setText(config_animations_font['path'])
        self.tool_font_path.clicked.connect(_file_click(self.edit_font_path, 'Font'))

        for field in fields_set:
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self._update_settings_from_ui)
            if isinstance(field, QCheckBox):
                field.stateChanged.connect(self._update_settings_from_ui)
            if isinstance(field, QSpinBox):
                field.valueChanged.connect(self._update_settings_from_ui)

        self.combo_banner.currentIndexChanged.connect(self._update_settings_from_ui)
        self.combo_language_text.currentIndexChanged.connect(self._update_settings_from_ui)
        self.combo_language_wish_items.currentIndexChanged.connect(self._update_settings_from_ui)
        self.combo_language_messages.currentIndexChanged.connect(self._update_settings_from_ui)
        self.combo_language_html_template.currentIndexChanged.connect(self._update_settings_from_ui)
        self.combo_anim_type.currentIndexChanged.connect(self._update_settings_from_ui)

        self.combo_language_text.currentIndexChanged.connect(self._reload_ui_text)

        self.button_save_config.clicked.connect(self._save_settings_from_ui)
        self.button_reset_config.clicked.connect(self._restore_default_config)
        self.button_start.clicked.connect(self._start)

    def _reload_ui_text(self):
        current_text_config = self.combo_language_text.currentText()
        text_data = _load_text(current_text_config)
        self.ui_text.update(text_data['text'])

        self.button_reset_config.setText(self._local_text('ui_button_reset_config'))
        self.button_save_config.setText(self._local_text('ui_button_save_config'))
        self.button_start.setText(self._local_text('ui_button_start'))

        self.check_command_permission_available.setText(self._local_text('ui_check_command_permission_available'))

        self.tabWidget.setTabText(0, self._local_text('ui_tab_1'))
        self.tabWidget.setTabText(1, self._local_text('ui_tab_2'))
        self.tabWidget.setTabText(2, self._local_text('ui_tab_3'))

        self.setWindowTitle(self._local_text('ui_settings'))
        self.group_animations.setTitle(self._local_text('ui_group_animations'))
        self.group_chatbot.setTitle(self._local_text('ui_group_chatbot'))
        self.group_event_bot.setTitle(self._local_text('ui_group_event_bot'))
        self.group_gbot.setTitle(self._local_text('ui_group_gbot'))
        self.group_general.setTitle(self._local_text('ui_group_general'))
        self.group_history.setTitle(self._local_text('ui_group_history'))
        self.group_language.setTitle(self._local_text('ui_group_language'))
        self.group_sound.setTitle(self._local_text('ui_group_sound'))

        self.label.setText(self._local_text('ui_label'))
        self.label_2.setText(self._local_text('ui_label_2'))
        self.label_3.setText(self._local_text('ui_label_3'))
        self.text_banner.setText(self._local_text('ui_text_banner'))
        self.text_chatbot_enabled.setText(self._local_text('ui_text_chatbot_enabled'))
        self.text_chroma_color.setText(self._local_text('ui_text_chroma_color'))
        self.text_command.setText(self._local_text('ui_text_command'))
        self.text_command_enabled.setText(self._local_text('ui_text_command_enabled'))
        self.text_command_permissions.setText(self._local_text('ui_text_command_permissions'))
        self.text_command_timeout.setText(self._local_text('ui_text_command_timeout'))
        self.text_default_color.setText(self._local_text('ui_text_default_color'))
        self.text_draw_wishes.setText(self._local_text('ui_text_draw_wishes'))
        self.text_enable_colors.setText(self._local_text('ui_text_enable_colors'))
        self.text_end_delay.setText(self._local_text('ui_text_end_delay'))
        self.text_end_delay_multi.setText(self._local_text('ui_text_end_delay_multi'))
        self.text_event_name.setText(self._local_text('ui_text_event_name'))
        self.text_eventbot_enabled.setText(self._local_text('ui_text_eventbot_enabled'))
        self.text_font_path.setText(self._local_text('ui_text_font_path'))
        self.text_fps.setText(self._local_text('ui_text_fps'))
        self.text_history_3star.setText(self._local_text('ui_text_history_3star'))
        self.text_history_4star.setText(self._local_text('ui_text_history_4star'))
        self.text_history_5star.setText(self._local_text('ui_text_history_5star'))
        self.text_history_enabled.setText(self._local_text('ui_text_history_enabled'))
        self.text_history_path.setText(self._local_text('ui_text_history_path'))
        self.text_is_draw_fall.setText(self._local_text('ui_text_is_draw_fall'))
        self.text_is_draw_usertext.setText(self._local_text('ui_text_is_draw_usertext'))
        self.text_language_html_template.setText(self._local_text('ui_text_language_html_template'))
        self.text_language_messages.setText(self._local_text('ui_text_language_messages'))
        self.text_language_text.setText(self._local_text('ui_text_language_text'))
        self.text_language_wish_items.setText(self._local_text('ui_text_language_wish_items'))
        self.text_revards.setText(self._local_text('ui_text_revards'))
        self.text_self_wish.setText(self._local_text('ui_text_self_wish'))
        self.text_self_wish_every.setText(self._local_text('ui_text_self_wish_every'))
        self.text_send_notify.setText(self._local_text('ui_text_send_notify'))
        self.text_send_stats.setText(self._local_text('ui_text_send_stats'))
        self.text_sound_3star.setText(self._local_text('ui_text_sound_3star'))
        self.text_sound_4star.setText(self._local_text('ui_text_sound_4star'))
        self.text_sound_5star.setText(self._local_text('ui_text_sound_5star'))
        self.text_sound_enabled.setText(self._local_text('ui_text_sound_enabled'))
        self.text_sound_fall.setText(self._local_text('ui_text_sound_fall'))
        self.text_start_delay.setText(self._local_text('ui_text_start_delay'))
        self.text_test_mode.setText(self._local_text('ui_text_test_mode'))
        self.text_user_background_enabled.setText(self._local_text('ui_text_user_background_enabled'))
        self.text_user_background_path.setText(self._local_text('ui_text_user_background_path'))
        self.text_user_background_type.setText(self._local_text('ui_text_user_background_type'))
        self.text_user_uid_size.setText(self._local_text('ui_text_user_uid_size'))
        self.text_window_name.setText(self._local_text('ui_text_window_name'))
        self.text_wish_chatbot_count.setText(self._local_text('ui_text_wish_chatbot_count'))
        self.text_wish_command.setText(self._local_text('ui_text_wish_command'))
        self.text_wish_eventbot_count.setText(self._local_text('ui_text_wish_eventbot_count'))
        self.text_wish_global_timeout.setText(self._local_text('ui_text_wish_global_timeout'))
        self.text_wish_name_size.setText(self._local_text('ui_text_wish_name_size'))
        self.text_wish_prefix.setText(self._local_text('ui_text_wish_prefix'))
        self.text_wish_timeout.setText(self._local_text('ui_text_wish_timeout'))

    def _update_settings_from_ui(self):
        config_main = CONFIG
        config_chatbot = config_main['chat_bot']
        config_event_bot = config_main['event_bot']
        config_sound = config_main['sound']
        config_gbot = config_main['gbot_config']
        config_language = config_main['language']
        config_history = config_main['history_file']
        config_animations = config_main['animations']

        config_main['window_name'] = self.edit_window_name.text()

        config_chatbot['wish_command'] = self.edit_wish_command.text()
        config_chatbot['wish_command_prefix'] = self.edit_wish_command_prefix.text()

        config_event_bot['default_color'] = self.edit_default_color.text()

        reward_index = self.combo_revards.currentIndex()
        config_event_bot['rewards'][reward_index]['event_name'] = self.edit_event_name.text()
        config_event_bot['rewards'][reward_index]['wish_count'] = self.spin_event_bot_wish_count.value()

        config_sound['fall'] = self.edit_sound_fall.text()
        config_sound['3'] = self.edit_sound_3star.text()
        config_sound['4'] = self.edit_sound_4star.text()
        config_sound['5'] = self.edit_sound_5star.text()

        config_history['path'] = self.edit_history_path.text()
        config_animations['chroma_color'] = self.edit_chroma_color.text()
        config_animations['user_background']['path'] = self.edit_user_background_path.text()
        config_animations['font']['path'] = self.edit_font_path.text()

        config_main['banner'] = self.combo_banner.currentText()
        config_language['text'] = self.combo_language_text.currentText()
        config_language['wish_items'] = self.combo_language_wish_items.currentText()
        config_language['messages'] = self.combo_language_messages.currentText()
        config_language['html_template'] = self.combo_language_html_template.currentText()
        config_animations['user_background']['type'] = self.combo_anim_type.currentText()

        config_main['send_dev_stats'] = self.check_send_stats.isChecked()
        config_main['test_mode'] = self.check_test_mode.isChecked()
        config_chatbot['enabled'] = self.check_chatbot_enabled.isChecked()
        config_chatbot['send_notify'] = self.check_send_notify.isChecked()
        config_chatbot['self_wish'] = self.check_self_wish.isChecked()
        config_chatbot['enable_colors'] = self.check_enable_colors.isChecked()
        config_event_bot['enabled'] = self.check_eventbot_enabled.isChecked()
        config_sound['enabled'] = self.check_sound_enabled.isChecked()

        current_command = self.combo_commands.currentText()
        current_command_permission = self.combo_command_permisson.currentText()
        config_gbot[current_command]['enabled'] = self.check_command_enabled.isChecked()
        config_gbot[current_command]['timeout'] = self.spin_command_permissions.value()
        config_gbot[current_command]['permissions'][current_command_permission] = self.check_command_permission_available.isChecked()

        config_history['enabled'] = self.check_history_enabled.isChecked()
        config_history['3'] = self.check_history_3star_enabled.isChecked()
        config_history['4'] = self.check_history_4star_enabled.isChecked()
        config_history['5'] = self.check_history_5star_enabled.isChecked()
        config_animations['draw_states']['draw_usertext'] = self.check_draw_usertext.isChecked()
        config_animations['draw_states']['draw_fall'] = self.check_draw_fall.isChecked()
        config_animations['draw_states']['draw_wishes'] = self.check_draw_wishes.isChecked()
        config_animations['user_background']['enabled'] = self.check_draw_user_background.isChecked()

        current_usertype = self.combo_wish_timeout.currentText()
        config_chatbot['wish_timeout'][current_usertype] = self.spin_wish_timeout.value()

        config_chatbot['wish_global_timeout'] = self.spin_wish_global_timeout.value()
        config_chatbot['wish_count'] = self.spin_wish_count.value()
        config_chatbot['self_wish_every'] = self.spin_self_wish_every.value()
        config_animations['start_delay'] = self.spin_start_delay.value()
        config_animations['fps'] = self.spin_fps.value()
        config_animations['font']['user_uid_size'] = self.spin_user_uid_size.value()
        config_animations['font']['wish_name_size'] = self.spin_wish_name_size.value()

        current_end_delay = self.combo_end_delay.currentText()
        config_animations['end_delay'][current_end_delay] = self.spin_end_delay.value()

        current_end_delay_multi = self.combo_end_delay_multi.currentText()
        config_animations['end_delay_multi'][current_end_delay_multi] = self.spin_end_delay_multi.value()

    def _save_settings_from_ui(self):
        config_main = CONFIG
        json_file = 'config.json'

        try:
            jsonschema.validate(config_main, schema=CONFIG_SCHEMA)
        except jsonschema.ValidationError as json_error:
            show_ui_window(ErrorMessage, title=self._local_text('ui_error'), error=self._local_text('config_check_error_check') % (json_file, json_error))
            return

        json_config = json.dumps(CONFIG, indent=2)
        with open(json_file, 'w') as json_f:
            json_f.write(json_config)

        CONFIG.clear()
        CONFIG.update(_load_json(json_file))

        show_ui_window(InfoMessage, title=self._local_text('ui_info'), info=self._local_text('ui_settings_saved_success'))

    def _restore_default_config(self):
        json_bad = 'config.json'
        json_good = 'config_def.json'

        CONFIG.clear()
        CONFIG.update(_load_json(json_good))

        with open(json_bad, 'w') as fjbad, open(json_good, 'r') as fjgood:
            fjbad.write(fjgood.read())

        show_ui_window(InfoMessage, title=self._local_text('ui_info'), info=self._local_text('ui_settings_restored_success'))
        self.close()

    def _start(self):
        self._window_result = True
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
    window.setFixedSize(window.size())

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
    print(show_ui_window(UserSettings))
