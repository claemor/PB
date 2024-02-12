import os
import sys
import easygui
import keyboard
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QSystemTrayIcon, QAction, QMenu
from PyQt5.uic import loadUi
import cfg_use
import functional

settings = cfg_use.check_cfg()
passes = 3


def panic():
    if settings['Browsers_clear']:
        functional.clear_browsers(passes)

    if settings['Logs_clear']:
        functional.delete_logs(passes)

    if settings['Crypto']:
        functional.demount()

    if settings['MBR_clear']:
        functional.MBR_unichtoshalyty(passes)

    if settings['Msg_clear']:
        functional.clear_msgers(passes)

    if settings['mac_change']:
        pass  # !!!!!!!!!!

    if settings['net_data_clear']:
        functional.clear_networks(passes)

    for i in settings['Files']:
        if os.path.isdir(i):
            functional.secure_delete_folder(i, passes)
        else:
            functional.secure_delete_file(i, passes)

    functional.send_messeges_TG(settings['bot_token'], map(int, settings['ids'].replace(" ", "").split(",")),
                                settings['msg'])

    if settings['Lock_screen']:
        functional.lock_and_restart()

    functional.secure_delete_file("settings.cfg", passes)
    window.tray_icon.setVisible(False)
    app.quit()


if settings['Keyboard_shortcut']:
    keyboard.add_hotkey(settings['Keyboard_shortcut'], panic)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.settingsButton.clicked.connect(self.open_settings_window)
        self.punicButton.clicked.connect(panic)
        self.settings_window = None
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setVisible(True)

        show_action = QAction("Показать", self)
        show_action.triggered.connect(self.showNormal)

        panic_action = QAction("Паника", self)
        panic_action.triggered.connect(panic)

        quit_action = QAction("Выйти", self)
        quit_action.triggered.connect(self.close)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(panic_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

    def open_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def close(self):
        self.tray_icon.setVisible(False)
        sys.exit(0)


class SettingsWindow(QDialog):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        loadUi('settings.ui', self)

        # Прив'язуємо кнопку до відкриття вікна налаштування повідомлення
        self.pushButton.clicked.connect(self.open_bot_window)
        self.buttonBox.accepted.connect(self.save)
        self.pushButton_add.clicked.connect(self.addFile)
        self.pushButton_add_folder.clicked.connect(self.addFolder)
        self.pushButton_delet.clicked.connect(self.deleteFile)
        self.pushButton_clear.clicked.connect(self.clearFiles)

        # Установка галочок налаштувань
        self.checkBox_Browser_clear.setChecked(settings['Browsers_clear'])
        self.checkBox_Logs_clear.setChecked(settings['Logs_clear'])
        self.checkBox_Crypto.setChecked(settings['Crypto'])
        self.checkBox_screen.setChecked(settings['Lock_screen'])
        self.checkBox_MBR_clear.setChecked(settings['MBR_clear'])
        self.checkBox_msg_clear.setChecked(settings['Msg_clear'])
        self.checkBox_mac_clear.setChecked(settings['mac_change'])
        self.checkBox_networks.setChecked(settings['net_data_clear'])

        # Встановлення комбінації клавіш
        self.lineEdit.setText(settings['Keyboard_shortcut'])

        self.bot_window = None

        self.listWidget.addItems(settings["Files"])

    def open_bot_window(self):
        self.bot_window = BotWindow()
        self.bot_window.show()

    def save(self):
        global settings
        settings = {'Browsers_clear': self.checkBox_Browser_clear.isChecked(),
                    'Logs_clear': self.checkBox_Logs_clear.isChecked(),
                    'Crypto': self.checkBox_Crypto.isChecked(),
                    'Lock_screen': self.checkBox_screen.isChecked(),
                    'MBR_clear': self.checkBox_MBR_clear.isChecked(),
                    'Msg_clear': self.checkBox_msg_clear.isChecked(),
                    'mac_change': self.checkBox_mac_clear.isChecked(),
                    'net_data_clear': self.checkBox_networks.isChecked(),
                    'Keyboard_shortcut': self.lineEdit.text(),
                    'bot_token': settings['bot_token'],
                    'ids': settings['ids'],
                    'msg': settings['msg'],
                    'Files': settings['Files']}

        if settings['Keyboard_shortcut']:
            keyboard.unhook_all()
            keyboard.add_hotkey(settings['Keyboard_shortcut'], panic)

        cfg_use.save_cfg(settings)

    def addFile(self):
        global settings
        file = easygui.fileopenbox()
        if file not in settings['Files']:
            settings['Files'].append(file)
            self.listWidget.addItem(file)

    def addFolder(self):
        global settings
        dir = easygui.diropenbox()
        if dir not in settings['Files']:
            settings['Files'].append(dir)
            self.listWidget.addItem(dir)

    def deleteFile(self):
        selectedItem = self.listWidget.selectedItems()
        if selectedItem:
            settings['Files'].remove(selectedItem[0].text())
            self.listWidget.clear()
            self.listWidget.addItems(settings["Files"])

    def clearFiles(self):
        self.listWidget.clear()
        settings['Files'] = []


class BotWindow(QDialog):
    def __init__(self):
        super(BotWindow, self).__init__()
        loadUi('tgbot.ui', self)
        self.token.setText(settings['bot_token'])
        self.ids.setText(settings['ids'])
        self.message.setText(settings['msg'])
        self.buttonBox.accepted.connect(self.save)

    def save(self):
        settings['bot_token'] = self.token.text()
        settings['ids'] = self.ids.text()
        settings['msg'] = self.message.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
