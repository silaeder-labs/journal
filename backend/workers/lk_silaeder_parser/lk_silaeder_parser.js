const API_URL = 'https://lk.silaeder.ru/api/objects';
const path = require('path');

require('dotenv').config({
  path: path.join(__dirname, '.env'),
  quiet: true
});

const TOKEN = process.env.BEARER_TOKEN;

async function getStudents() {
  try {
    const response = await fetch(API_URL, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${TOKEN}`
      }
    });

    if (!response.ok) {
      throw new Error(`Ошибка: ${response.status}`);
    }

    const data = await response.json();

    return data
  } catch (error) {
    console.error('Ошибка при запросе:', error.message);
  }
}

async function parseResult(data) {
    result = []
    for(let i = 0; i < data.length; i++) {
        student = []

        student.push(Number(data[i]["attributes"]["grade"]));
        student = [...student, ...data[i]["name"].split(' ')];

        result.push(student)
    }

    return result
}

async function deleteInvalidInformation(data, grade) {
    result = []
    for(let i = 0; i < data.length; i++) {
        if(!Number.isNaN(data[i][0]) && data[i][0] <= grade) {
            result.push(data[i])
            console.log(data[i])
        }
    }

    return result
}

async function main() {
    const data = await getStudents();
    const result = await parseResult(data);
    const cleared_result = await deleteInvalidInformation(result, 11);
    // console.log(cleared_result);
}
main();