# Tạo header giả lập trình duyệt (bao gồm cookie đã đăng nhập)
def create_headers(cookies):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Cookie': cookies['cookie'],
    }