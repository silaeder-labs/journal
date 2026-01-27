const getSubjectMarks = async () => {
  const url = "https://school.mos.ru/api/family/web/v1/subject_marks?student_id=31835076";

  let subjects_names = []
  let subject_ids = []

  const options = {
    method: "GET",
    headers: {
      
      "profile-id": "31835076",
      "x-mes-subsystem": "familyweb"
    }
  };

  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      throw new Error(`Ошибка: ${response.status}`);
    }

    const data = await response.json();
    for (let i = 0; i < data["payload"].length; i++) {
        subject_ids.push(data["payload"][i]["subject_id"]);
        subjects_names.push(data["payload"][i]["subject_name"]);
    }
    // console.log(data["payload"]);
    // console.log(data["payload"].length);
    console.log(subject_ids);
    console.log(subjects_names);

  } catch (error) {
    console.error("Произошла ошибка при запросе:", error.message);
  }
};

getSubjectMarks();



