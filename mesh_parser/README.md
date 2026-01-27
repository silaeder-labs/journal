# Парсер МЭШа
> программа которая позволяет парсить оценки учеников в МЭШе

---

<h2 id="quick-start">Как запустить?</h2>

1. настройка конфига
создайте файл `.env` в `/mesh_parser` <br>
напишите в него значение вашего токена
```
BEARER_TOKEN=<ваш токен>
```

2. клонирование и запуск логина
```bash 
git clone https://github.com/silaeder-labs/journal #клонирование репозитория
cd journal #переход в папку
npm install dotenv # установка библиотек
node mesh_parser/students_average_marks/mesh-parser.js
```
после завершения программы `.json` файлы будут в папке `/mesh_parser/students_average_marks/data`