import os


# Функція перезапису конфігурації
def save_cfg(settings):
    cfg = open('settings.cfg', "w+")

    for line in settings:
        if line == "Files":
            break
        cfg.write(f"{line} = {settings[line]}\n")

    cfg.write("[Files]\n")
    for files in settings["Files"]:
        cfg.write(f"{files}\n")

    cfg.close()


# Функція перевірки конфігурації
def check_cfg():
    settings = {}

    # Перевірка чи існує файл конфігурації
    if os.path.exists('settings.cfg'):
        cfg = open('settings.cfg')

        # Записуємо всі конфігурації крім файлів
        line = cfg.readline()
        while not ('Keyboard_shortcut' in line):
            settings[line.replace("\n", "").split(" = ")[0]] = line.replace("\n", "").split(" = ")[1] == "True"
            line = cfg.readline()

        while not ('Files' in line):
            settings[line.replace("\n", "").split(" = ")[0]] = line.replace("\n", "").split(" = ")[1]
            line = cfg.readline()

        settings["Files"] = []

        # Записуємо всі файли
        line = cfg.readline()
        while line and line != '\n':
            settings["Files"].append(line.replace("\n", ""))
            line = cfg.readline()

        cfg.close()
    else:
        # Налаштування за замовчуванням
        settings = {'Browsers_clear': False, 'Logs_clear': False, 'Crypto': False, 'Lock_screen': False,
                    'MBR_clear': False, 'Msg_clear': False, 'mac_change': False, 'net_data_clear': False,
                    'Keyboard_shortcut': '', 'bot_token': '', 'ids': '', 'msg': '', 'Files': []}

        # Записуємо в конфіг
        save_cfg(settings)

    return settings
