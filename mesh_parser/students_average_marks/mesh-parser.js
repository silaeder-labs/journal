const path = require('path');
const fs = require('fs');

require('dotenv').config({ path: path.join(__dirname, '.env') });

const today = new Date().toISOString().split('T')[0];

const authorization_token = process.env.BEARER_TOKEN;
const subject_names = process.env.SUBJECT_NAMES.split(',');
const subject_ids = process.env.SUBJECT_IDS.split(',');
const person_id = process.env.PERSON_ID;
const URL_BASE = "https://school.mos.ru/api/ej/rating/v1/rank/class";

const jsonFilePath = path.join(__dirname, 'data/data.json');

function addDays(dateString, days) {
  const date = new Date(dateString);
  date.setDate(date.getDate() + days);
  return date.toISOString().split('T')[0];
}

async function getRank(url) {
    let users_marks = {};
    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${authorization_token}`,
                "x-mes-subsystem": "familyweb"
            }
        });
        if (!response.ok) throw new Error(`Ошибка: ${response.status}`);
        const data = await response.json();
        for (let i = 0; i < data.length; i++) {
            users_marks[data[i]["personId"]] = data[i]["rank"]["averageMarkFive"];
        }
    } catch (err) {
        console.error(`Сбой на URL ${url}:`, err.message);
    }
    return users_marks;
}

async function get_days_marks(curr_day, subject_id, n) {
    let overall_marks = {};
    const tasks = [];
    for (let j = 0; j <= n; j++) {
        const day = curr_day;
        const curr_url = `${URL_BASE}?personId=${person_id}&subjectId=${subject_id}&date=${day}`;
        const task = getRank(curr_url).then(marks => {
            overall_marks[day] = marks;
        });
        tasks.push(task);
        curr_day = addDays(curr_day, 1);
    }
    await Promise.all(tasks);
    return overall_marks;
}

async function main() {
    const final_marks = {};
    console.log(today)

    for (let v = 0; v < subject_ids.length; v++) {
        console.log(`working on: ${subject_names[v]}...`);
        const marks_final = await get_days_marks(addDays(today, -36), subject_ids[v].toString(), 36);
        
        const sortedDates = Object.keys(marks_final).sort((a, b) => new Date(a) - new Date(b));
        const sortedMarks = {};
        sortedDates.forEach(date => {
            sortedMarks[date] = marks_final[date];
        });
        
        final_marks[subject_names[v]] = sortedMarks;
    }

    const jsonString = JSON.stringify(final_marks, null, 2);
    fs.writeFileSync(jsonFilePath, jsonString, 'utf8');
    console.log("completed");
}

main();