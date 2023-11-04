import os

folder_path = 'Datasets'  # Укажите путь к папке, в которой находятся файлы

# Получить список файлов в папке
files = os.listdir(folder_path)

# Перебрать все файлы и переименовать их
for i, file_name in enumerate(files):
    src = os.path.join(folder_path, file_name)
    if os.path.isfile(src):
        # Создать новое имя файла в формате "image_N.jpg"
        new_name = f'video_{i + 1}.mp4'
        
        # Полный путь к исходному файлу
        src = os.path.join(folder_path, file_name)
        
        # Полный путь к новому файлу
        dst = os.path.join(folder_path, new_name)
        
        # Переименовать файл
        os.rename(src, dst)