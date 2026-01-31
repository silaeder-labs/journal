const { getAllMakrs } = require('../workers/mesh_parser/marks/mesh-parser');
const today = new Date().toISOString().split('T')[0];

(async () => {
  try {
    const result = await getAllMakrs(today, 0);
    if (!result) {
      process.exit(1);
    }

    console.log(JSON.stringify(result));
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
