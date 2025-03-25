from flask import Flask, request, render_template, make_response
import requests
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Функция для получения содержимого файла через raw.githubusercontent.com
def get_github_file_content(repo_url, file_path, branch='main'):
    raw_url = f"https://raw.githubusercontent.com/{repo_url}/refs/heads/{branch}/{file_path}"
    print(raw_url)
    response = requests.get(raw_url)
    if response.status_code == 200:
        return response.text
    return None

# Главная страница с документацией
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Страница 1: Получение файла через GET-запрос
@app.route('/get', methods=['GET'])
def page1():
    # Параметры из GET-запроса
    repo_url = request.args.get('repo_url')
    file_path = request.args.get('file_path')
    branch = request.args.get('branch', 'main')  # По умолчанию ветка 'main'

    if repo_url and file_path:
        content = get_github_file_content(repo_url, file_path, branch)
        if content:
            response = make_response(content)
            response.mimetype = "text/plain"

            return response
        else:
            return render_template('page.html', error="Failed to fetch file content.")
    else:
        return render_template('page.html', error="Missing parameters: repo_url and file_path are required.")

# Страница 2: Получение файла через POST-запрос
@app.route('/post', methods=['GET', 'POST'])
def page2():
    # Параметры из POST-запроса
    repo_url = request.json['repo_url']
    file_path = request.json['file_path']
    branch = request.json['branch'] or 'main'

    if repo_url and file_path:
        content = get_github_file_content(repo_url, file_path, branch)
        if content:
            response = make_response(content)
            response.mimetype = "text/plain"

            return response
        else:
            return render_template('page.html', error="Failed to fetch file content.")
    else:
        return render_template('page.html', error="Missing parameters: repo_url and file_path are required.")

if __name__ == '__main__':
    app.run(debug=True)