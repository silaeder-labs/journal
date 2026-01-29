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

---

<h2 id="homework-parsing">Парсинг домашки</h2>
> Автоматическое получение домашней работы за указаный период

---

<h3 id="homework-parsing-quick-start">Как запустить?</h3>

1. добавьте токен в окружение

2. импортируйте функцию getHomeWork скрипт homeworks-parser
```javascript
const { getHomework } = require(<PATH>);
```

3. вызовите функцию указав аргуметы
```javascript
getHomework('2026-01-28', '2026-01-28', false); //1-стартовая дата, 2-конечная дата, 3-сохранять ли в json
```

> [!NOTE]
> сегодняшнюю дату можно получить с помощью
> ```
> const today = new Date().toISOString().split('T')[0];
> ```