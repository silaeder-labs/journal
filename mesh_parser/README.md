# Парсер МЭШа
> программа которая позволяет парсить оценки учеников в МЭШе

---

## Как запустить?

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
```
после выполнения этих комманд вы сможете использовать все библиотеки

---

## Библиотеки

---

### homework parser

#### описание:
эта библиотека позволяет получать данные по домашке за выбранный временной период

#### импорт:
```javascript
const { getHomework } = require('<LIBRARY PATH>');
```

#### функции
- ```getHomework(start_date, end_date)``` 

> [!NOTE]
> формат даты: "yyyy-mm-dd"

---

### marks parser

#### описание:
эта библиотека позволяет получать средние оценки по классу за выбраный период

#### импорт:
```javascript
const { getAllMakrs } = require('<LIBRARY PATH>');
```

#### функции
- ```getAllMakrs(end_date, count)``` 

> [!NOTE]
> формат даты: "yyyy-mm-dd"

> [!NOTE]
> сегодняшнюю дату можно получить с помощью
> ```
> const today = new Date().toISOString().split('T')[0];
> ```