from flask import Flask
import os

app = Flask(__name__)

# Секретный ключ лучше хранить в переменных окружения
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

@app.route('/')
def home():
    return "<h1>Мой сайт теперь виден всему миру!</h1><p>Работает через No-IP или ngrok.</p>"

if __name__ == '__main__':
    # ВАЖНО: host='0.0.0.0' открывает доступ для внешних запросов.
    # port=5000 — стандартный порт Flask.
    # debug=False — ОБЯЗАТЕЛЬНО для публичного доступа (в целях безопасности).
    app.run(host='0.0.0.0', port=5000, debug=False)

#NoIP
#iceberg_officially@internet.ru
#up6O%iSxmQJt*V
#iceberg.hopto.org
#178.206.226.157