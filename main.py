import json
from pathlib import Path
import urllib.parse
import pathlib
import mimetypes
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader

# 📁 шлях до файлу з повідомленнями (JSON база даних)
FILE_PATH = Path("storage") / "data.json"
FILE_PATH.parent.mkdir(exist_ok=True)


class HttpHandler(BaseHTTPRequestHandler):

    # ОБРОБКА GET ЗАПИТІВ
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)

        # головна сторінка
        if pr_url.path == "/":
            self.send_html_file("index.html")

        # форма відправки повідомлення
        elif pr_url.path == "/message":
            self.send_html_file("message.html")

        # сторінка перегляду повідомлень (рендер через Jinja)
        elif pr_url.path == "/read":
            self.prepare_read_page()

        # статичні файли (css, images, js)
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                # якщо сторінка не знайдена
                self.send_html_file("error.html", 404)

    # відправка статичних файлів (css, js, img)
    def send_static(self):
        self.send_response(200)

        # визначаємо MIME-type файлу
        mt = mimetypes.guess_type(self.path)

        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")

        self.end_headers()

        # читаємо файл у байтах і відправляємо в браузер
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    # відправка HTML сторінки
    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    # ОБРОБКА POST (отримання форми)
    def do_POST(self):
        # читаємо тіло запиту
        data = self.rfile.read(int(self.headers["Content-Length"]))

        # парсимо URL encoded дані (split ДО unquote, інакше = чи & в тексті ламають парсинг)
        parsed = urllib.parse.parse_qs(data.decode(), keep_blank_values=True)
        data_dict = {key: values[0] for key, values in parsed.items()}

        # Зберігаємо повідомлення в JSON файл
        HttpHandler.save_message(data_dict)

        # редирект назад на головну сторінку
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    # ЗБЕРЕЖЕННЯ ПОВІДОМЛЕННЯ В JSON
    @staticmethod
    def save_message(data_dict):
        # timestamp як ключ
        current_time = str(datetime.now())

        # читаємо існуючу базу
        if FILE_PATH.exists():
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    storage = json.load(f)
                except json.JSONDecodeError:
                    storage = {}
        else:
            storage = {}

        # додаємо нове повідомлення
        storage[current_time] = {
            "username": data_dict.get("username"),
            "message": data_dict.get("message"),
        }

        # записуємо назад у файл
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)

    # ЗЧИТУВАННЯ ПОВІДОМЛЕНЬ З JSON
    @staticmethod
    def load_messages():
        if FILE_PATH.exists():
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    # РЕНДЕР СТОРІНКИ READ З ПОВІДОМЛЕННЯМИ (JINJA2)
    def prepare_read_page(self):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("read.html")

        messages = self.load_messages()

        persons = [
            {"time": time, "username": data["username"], "message": data["message"]}
            for time, data in messages.items()
        ]

        output = template.render(persons=persons)

        self.send_html(output)

    # Відправка зрендереної html сторінки
    def send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


# запуск HTTP сервера
def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)

    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
