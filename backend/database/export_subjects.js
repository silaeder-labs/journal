const { getSubjectIdsAndNames } = require('../workers/mesh_parser/subjects/subjects_parser');

(async () => {
  try {
    const result = await getSubjectIdsAndNames();
    if (!result) {
      process.exit(1);
    }

    console.log(JSON.stringify(result));
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
