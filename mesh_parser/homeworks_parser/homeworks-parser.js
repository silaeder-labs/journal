const { getSessions } = require('../ids/id_parser.js');

const path = require('path');
const fs = require('fs');

require('dotenv').config({ path: path.join(__dirname, '../.env') });

const authorization_token = process.env.BEARER_TOKEN;

const jsonFilePath = path.join(__dirname, 'data/data.json');

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

        let result = {}

        const data = await response.json();

        for (let i = 0; i < data["payload"].length; i++) {
            let cur_res = {}
            cur_res["type"] = data["payload"][i]["type"]; //type
            cur_res["description"] = data["payload"][i]["description"]; //description
            cur_res["homework"] = data["payload"][i]["homework"]; //homework
            cur_res["subject_id"] = data["payload"][i]["subject_id"]; //subject id
            cur_res["subject_name"] = data["payload"][i]["subject_name"]; //subject name
            cur_res["date_prepared_for"] = data["payload"][i]["date_prepared_for"]; //date prepared for

            result[i] = cur_res;
        }

        const jsonString = JSON.stringify(result, null, 2);
        fs.writeFileSync(jsonFilePath, jsonString, 'utf8');        
        console.log("completed");
    } catch (error) {
        console.error("Произошла ошибка при запросе:", error.message);
    }
}

getHomework('2026-01-28', '2026-01-28');