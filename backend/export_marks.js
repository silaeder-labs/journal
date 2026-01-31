const { getAllMakrs } = require('../mesh_parser/marks/mesh-parser');

(async () => {
  try {
    const result = await getAllMakrs("2026-01-29", 2);
    if (!result) {
      process.exit(1);
    }

    console.log(JSON.stringify(result));
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
