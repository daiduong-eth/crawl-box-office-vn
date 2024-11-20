# Đọc danh sách các phim từ file CSV
def read_movies_from_csv(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]