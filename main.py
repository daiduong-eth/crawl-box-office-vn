import os
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}

with open('vietnam_movies.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['page', 'film_name', 'link', 'short-name', 'release-date'])
    page = 1
    while True:
        url = f'https://boxofficevietnam.com/movie/page/{page}/'
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Không thể truy cập trang {page}")
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.find_all('div', class_='movie-box-1 mb30')
        if not movies:
            print(f"Không còn phim ở trang {page}, dừng lại.")
            break
        for movie in movies:
            title_tag = movie.find('h4', class_='movie-title')
            title = title_tag.text.strip() if title_tag else 'N/A'
            link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else 'N/A'
            short_name = link.split('/movie/')[-1].strip('/') if link != 'N/A' else 'N/A'
            release_date_tag = movie.find('span', class_='released')
            release_date = release_date_tag.text.strip() if release_date_tag else 'N/A'
            writer.writerow([page, title, link, short_name, release_date])
            print(f"Trang {page} - Tên phim: {title}")
            print(f"Link chi tiết: {link}")
            print(f"Tên rút gọn: {short_name}")
            print(f"Ngày phát hành: {release_date}")
            print("---")
        page += 1

print("Dữ liệu đã được lưu vào file vietnam_movies.csv")

folder_name = 'films'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
with open('vietnam_movies.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    movies = [row for row in reader]
with open('cookies.json', 'r') as cookie_file:
    cookies = json.load(cookie_file)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie': cookies['cookie'],
}
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

df_movies = pd.read_csv('vietnam_movies.csv')
total_movies = len(df_movies)
df_movies['film_id'] = [100000 - i for i in range(total_movies)]
df_movies.to_csv('vietnam_movies.csv', index=False, encoding='utf-8-sig')
print("Đã thêm cột 'film_id' vào file vietnam_movies.csv.")


folder_path = 'films'
output_folder_path = 'film_csv'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
vietnam_movies_df = pd.read_csv('vietnam_movies.csv')
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    short_name = file.split('.')[0]  
    film_info = vietnam_movies_df[vietnam_movies_df['short-name'] == short_name]
    if film_info.empty:
        print(f"Không tìm thấy thông tin film_id cho file {file}")
        continue
    film_id = film_info['film_id'].values[0]
    try:
        df = pd.read_excel(file_path, header=2)
        df['film_id'] = film_id
        df.rename(columns={
            'Cụm rạp': 'cum_rap',
            'Mã rạp': 'ma_rap',
            'Tên rạp': 'ten_rap',
            'Phòng chiếu': 'phong_chieu',
            'Format': 'format',
            'Doanh thu': 'doanh_thu',
            'Số vé': 'so_ve',
            'Số ghế': 'so_ghe',
            'Giờ chiếu': 'gio_chieu',
            'Ca chiếu': 'ca_chieu'
        }, inplace=True)
        columns = ['film_id'] + [col for col in df.columns if col != 'film_id']
        df = df[columns]
        csv_file_path = os.path.join(output_folder_path, f"{short_name}.csv")
        df.to_csv(csv_file_path, index=False, encoding='utf-8')
        print(f"Đã lưu dữ liệu từ file {file} thành CSV: {csv_file_path}")
    except Exception as e:
        print(f"Lỗi khi đọc file {file}: {e}")

folder_path = 'film_csv'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
combined_df = pd.DataFrame()
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path) 
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    except Exception as e:
        print(f'Lỗi khi đọc file {file}: {e}')
output_path = 'bovn.csv'
combined_df.to_csv(output_path, index=False, encoding='utf-8')

print(f'Tất cả các file CSV đã được gộp và lưu vào: {output_path}')
