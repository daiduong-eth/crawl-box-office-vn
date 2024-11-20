import requests
import csv
from bs4 import BeautifulSoup

def crawl_movies_and_save_to_csv(csv_file, headers):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
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
