//imports
const { getSubjectIdsAndNames } = require('../subjects/subjects_parser.js');
const { getSessions } = require('../ids/id_parser.js');

//token from .env
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../.env') });
const authorization_token = process.env.BEARER_TOKEN;

const URL_BASE = "https://school.mos.ru/api/ej/rating/v1/rank/class";

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

async function getDaysMarks(curr_day, subject_id, n) {
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

async function getAllMakrs(curr_day, count) {
    const ids = await getSubjectIdsAndNames();
    if (ids) {
        subject_ids = ids.subject_ids;
        subject_names = ids.subjects_names;
    }

    const session = await getSessions();
    if(session) {
        person_id = session.person_id;
    }

    const final_marks = {};

    for (let v = 0; v < subject_ids.length; v++) {
        console.log(`working on: ${subject_names[v]}...`);
        const marks_final = await getDaysMarks(addDays(curr_day, -count), subject_ids[v].toString(), count);
        
        const sortedDates = Object.keys(marks_final).sort((a, b) => new Date(a) - new Date(b));
        const sortedMarks = {};
        sortedDates.forEach(date => {
            sortedMarks[date] = marks_final[date];
        });
        
        final_marks[subject_names[v]] = sortedMarks;
    }
    console.log("completed");
    return final_marks;
}

module.exports = { getAllMakrs };