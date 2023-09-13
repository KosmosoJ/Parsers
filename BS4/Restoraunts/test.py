from fake_useragent import UserAgent

def get_headers():
    ua = UserAgent()
    headers = {
    'User-Agent': ua.random,
    'From': 'youremail@domain.example'  # This is another valid field
    }    
    return headers




for _ in range(5):
    print(get_headers())