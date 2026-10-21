from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

URL = "https://sarhne.sarahah.pro/MalakAbdulrahman"

@app.route('/')
def home():
    last_seen = "جاري جلب البيانات..."
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            small_tags = soup.find_all('small')
            for tag in small_tags:
                if 'أخر ظهور' in tag.text or 'آخر ظهور' in tag.text:
                    last_seen = tag.text.strip()
                    break
            else:
                last_seen = "لم يتم العثور على حقل آخر ظهور"
        else:
            last_seen = f"خطأ في الاتصال بالموقع: {response.status_code}"
    except Exception as e:
        last_seen = "حدث خطأ أثناء جلب البيانات"

    return render_template('index.html', last_seen=last_seen)

if __name__ == '__main__':
    app.run(debug=True)
