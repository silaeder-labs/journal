const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../.env') });

const authorization_token = process.env.BEARER_TOKEN;

const getSubjectIdsAndMarks = async () => {
  const url = "https://school.mos.ru/api/family/web/v1/subject_marks?student_id=31835076";

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

module.exports = { getSubjectIdsAndMarks };