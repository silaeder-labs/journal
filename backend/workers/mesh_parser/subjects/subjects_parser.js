const { getSessions } = require('../ids/id_parser.js');
const path = require('path');
require('dotenv').config({
  path: path.join(__dirname, '../.env'),
  quiet: true
});


const authorization_token = process.env.BEARER_TOKEN;

const getSubjectIdsAndNames = async () => {
  let profile_id = null;

  const session = await getSessions();
  if(session && session.profile_id) {
      profile_id = session.profile_id;
  } else {
      console.error("Не удалось получить profile_id из сессии");
      return;
  }

  const url = `https://school.mos.ru/api/family/web/v1/subject_marks?student_id=${profile_id}`;

  let subjects_names = [];
  let subject_ids = [];

  const options = {
    method: "GET",
    headers: {
      "authorization": `Bearer ${authorization_token}`,
      "x-mes-subsystem": "familyweb"
    }
  };

  try {
    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`Ошибка: ${response.status}`);

    const data = await response.json();
    
    for (let item of data["payload"]) {
        subject_ids.push(item["subject_id"]);
        subjects_names.push(item["subject_name"]);
    }

    return { subject_ids, subjects_names }; 

  } catch (error) {
    console.error("Произошла ошибка:", error.message);
  }
};

module.exports = { getSubjectIdsAndNames };