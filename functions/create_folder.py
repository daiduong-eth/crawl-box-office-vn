# Tạo thư mục 'films' nếu chưa tồn tại
def create_films_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)