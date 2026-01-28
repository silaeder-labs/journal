const { getSessions } = require('../ids/id_parser.js');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../.env') });

const authorization_token = process.env.BEARER_TOKEN;

async function getHomework(from_date, to_date) {
    let profile_id = null;

    const result2 = await getSessions();
    if(result2 && result2.profile_id) {
        profile_id = result2.profile_id;
    } else {
        console.error("Не удалось получить profile_id из сессии");
        return;
    }

    const API_URL = "https://school.mos.ru/api/family/web/v1/homeworks";
    
    const params = new URLSearchParams({
        from: from_date,
        to: to_date,
        student_id: profile_id
    });

    const headers = {
        "authorization": `Bearer ${authorization_token}`,
        "x-mes-subsystem": "familyweb",
    };

    try {
        const response = await fetch(`${API_URL}?${params}`, {
            method: "GET",
            headers: headers
        });

        if (!response.ok) {
            throw new Error(`Ошибка: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
        
    } catch (error) {
        console.error("Произошла ошибка при запросе:", error.message);
    }
}

getHomework('2026-01-28', '2026-01-28');