# Парсер МЭШа
> программа которая позволяет парсить оценки учеников в МЭШе

---

<h2 id="quick-start">Как запустить?</h2>

```bash 
git clone https://github.com/silaeder-labs/journal #клонирование репозитория
cd journal/mesh-parser #переход в папку
pip install -r requirements.txt #установка библиотек
python mesh-login.py #запуск программы для логина
```

после этого у вас откроется страница логина МЭШа, 
вам нужно будет войти в аккаунт и программа сохранит данные входа в auth.json

```bash
python mesh-get-json.py #основной скрипт
```

после завершения программы `.json` файлы будут в папку `/data`