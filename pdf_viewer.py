import os
import json
from flask import Flask, send_from_directory, abort, jsonify, render_template_string
import logging
from functools import lru_cache
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)
# Отключаем логи watchdog
logging.getLogger('watchdog').setLevel(logging.WARNING)
# Настраиваем логирование только для нашего приложения
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

with open("links_.json", "r", encoding="utf-8") as f:
    links = json.load(f)

@lru_cache(maxsize=1)
def get_pdf_files(directory):
    """Рекурсивно находит все PDF файлы в указанной директории и поддиректориях."""
    pdf_files = []
    
    try:
        if not os.path.exists(directory):
            logger.error(f"Директория не существует: {directory}")
            return []
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, directory)
                    pdf_files.append(relative_path)
        
        return sorted(pdf_files)
    except Exception as e:
        logger.error(f"Ошибка при сканировании директории: {str(e)}")
        return []

def build_file_tree(pdf_files):
    """Строит дерево файлов из списка PDF файлов."""
    file_tree = {'files': [], 'folders': {}, 'total_files': 0}
    
    for pdf_file in pdf_files:
        parts = pdf_file.split('/')
        if len(parts) > 1:
            current = file_tree
            for i in range(len(parts) - 1):
                if parts[i] not in current['folders']:
                    current['folders'][parts[i]] = {'files': [], 'folders': {}, 'total_files': 0}
                current = current['folders'][parts[i]]
            current['files'].append(parts[-1])
            current['total_files'] += 1  # Увеличиваем счетчик только один раз при добавлении файла
        else:
            file_tree['files'].append(pdf_file)
            file_tree['total_files'] += 1
    
    return file_tree

@app.route('/')
def index():
    """Отдает статический HTML файл."""
    return send_from_directory('static', 'index.html')

@app.route('/api/files')
def get_files():
    """Отдает JSON с деревом файлов."""
    pdf_directory = os.getenv('PDF_DIRECTORY')
    if not pdf_directory:
        logger.error("PDF_DIRECTORY не установлен в .env файле")
        abort(500)
    pdf_files = get_pdf_files(pdf_directory)
    logger.info(f"DEBUG: Всего найдено файлов: {len(pdf_files)}")
    
    file_tree = build_file_tree(pdf_files)
    logger.info(f"DEBUG: Количество файлов в корне: {len(file_tree['files'])}")
    logger.info(f"DEBUG: Количество папок в корне: {len(file_tree['folders'])}")
    
    response = jsonify(file_tree)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response

@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    """Отдает PDF файл для просмотра."""
    pdf_directory = os.getenv('PDF_DIRECTORY')
    if not pdf_directory:
        logger.error("PDF_DIRECTORY не установлен в .env файле")
        abort(500)
    
    try:
        return send_from_directory(pdf_directory, filename)
    except Exception as e:
        logger.error(f"Error serving PDF: {str(e)}")
        abort(404)

@app.route('/view/<path:filename>')
def view_pdf(filename):
    """Страница для просмотра PDF с использованием PDF.js."""
    global links
    with open('static/viewer.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    base_url = os.getenv('BASE_URL')
    original_url_base = os.getenv('ORIGINAL_URL_BASE')
    
    if not base_url or not original_url_base:
        logger.error("BASE_URL или ORIGINAL_URL_BASE не установлены в .env файле")
        abort(500)
        
    return render_template_string(
        template,
        base_url=base_url,
        filename=filename,
        full_url=f"{base_url}pdf/{filename}",
        original_url=f"{original_url_base}{filename}",
        meta_data = links.get(filename, "")
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 