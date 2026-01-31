const path = require('path');
require('dotenv').config({
  path: path.join(__dirname, '../.env'),
  quiet: true
});

const authorization_token = process.env.BEARER_TOKEN;

const getSessions = async () => {
  const url = "https://school.mos.ru/api/ej/acl/v1/sessions";

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": `Bearer ${authorization_token}`,
        "Accept": "application/json, text/plain, */*",
        "X-Mes-Subsystem": "familyweb"
      },
      body: JSON.stringify({auth_token: authorization_token})
    });

    if (!response.ok) {
      throw new Error(`Ошибка сервера: ${response.status}`);
    }

    const data = await response.json();
    profile_id = data["profiles"][0]["id"];
    person_id = data["person_id"];

    return { profile_id, person_id };
    
  } catch (error) {
    console.error("Запрос не удался:", error.message);
  }
};

module.exports = { getSessions };