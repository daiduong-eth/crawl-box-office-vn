# Crawl Box Office Vn 
Github Crawl data phim trên box office Việt Nam
daiduong.eth@gmail.comn

## Cài Đặt
1. Cài các package
```bash
pip install -r requirements.txt
```
2. Tạo file cookies.json
 - Đăng nhập: https://boxofficevietnam.com/ bằng tài khoản VIP (Có quyền Download)
 - Lấy Cookies đăng nhập
 - Tạo file cookies.json theo mẫu cookies.example.json

3. Chạy file main.py
 - Sau khi chạy sẽ tạo ra:
 + folder films: Chứa data raw thông tin đặt vé, doanh số, số ghế, số vé dạng excel của từng phim
 + folder films_csv: Chứa data raw thông tin đặt vé, doanh số, số ghế, số vé dạng csv của từng phim
 + file vietnam_movies.csv: Chứa tổng hợp các film chiếu ở Việt Nam
 + file bovn.csv: Chứa data raw thông tin đặt vé, doanh số, số ghế, số vé dạng ở tất cả các phim
