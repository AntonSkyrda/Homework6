import sys
import os
import shutil

# Список розширень для кожної категорії
CATEGORIES = {
    'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'videos': ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')
}


# Функція транслітерації та перейменування файлу
def normalize(filename):
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G',
        'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
        'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K',
        'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
        'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
        'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ь': '', 'Ю': 'Yu', 'Я': 'Ya'
    }
    normalized = ''
    for char in filename:
        if char.isalpha() and char.isascii():
            normalized += char
        elif char in translit_map:
            normalized += translit_map[char]
        else:
            normalized += '_'
    return normalized


# Функція сортування та перейменування папки
def sort_folder(folder):
    known_extensions = set()
    unknown_extensions = set()

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = file.split('.')[-1].upper()

            # Отримуємо категорію за розширенням файлу
            category = None
            for key, extensions in CATEGORIES.items():
                if file_extension in extensions:
                    category = key
                    break

            # Перейменовуємо файл з використанням normalize
            normalized_name = normalize(file.split('.')[0])
            new_filename = f'{normalized_name}.{file_extension}'

            if category:
                # Створюємо папку категорії, якщо її ще немає
                category_folder = os.path.join(folder, category)
                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)

                # Переміщуємо файл в папку категорії
                new_file_path = os.path.join(category_folder, new_filename)
                shutil.move(file_path, new_file_path)

                # Зберігаємо розширення у відповідному множині
                known_extensions.add(file_extension)
            else:
                # Зберігаємо розширення у множині невідомих розширень
                unknown_extensions.add(file_extension)

    # Видаляємо порожні папки
    for root, dirs, _ in os.walk(folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    return known_extensions, unknown_extensions


if __name__ == '__main__':
    # Перевіряємо, чи був переданий аргумент командного рядка
    if len(sys.argv) < 2:
        print('Потрібно вказати ім\'я папки!')
        sys.exit(1)

    folder_name = sys.argv[1]

    # Перевіряємо, чи існує папка з вказаним ім'ям
    if not os.path.exists(folder_name):
        print('Папку не знайдено!')
        sys.exit(1)

    # Викликаємо функцію сортування та перейменування папки
    known_ext, unknown_ext = sort_folder(folder_name)

    print('Сортування завершено.')
    print('Відомі розширення:', known_ext)
    print('Невідомі розширення:', unknown_ext)
