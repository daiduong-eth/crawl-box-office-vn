# Tải file Excel từ danh sách phim
def download_movie_excels(movies, headers, folder_name):
    create_films_folder(folder_name)
    for movie in movies:
        short_name = movie['short-name']
        url = f'https://boxofficevietnam.com/movie/{short_name}/?download=1'
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_name = f'{short_name}.xlsx'
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Đã tải và lưu thành công: {file_name}")
            else:
                print(f"Không thể tải dữ liệu từ URL: {url} (Status code: {response.status_code})")
        except Exception as e:
            print(f"Lỗi khi tải hoặc lưu file từ {url}: {e}")
    print("Quá trình tải file hoàn tất.")
