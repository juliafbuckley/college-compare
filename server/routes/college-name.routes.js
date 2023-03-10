module.exports = app => {
    const college_names = require("../controllers/college-name.controller.js");

    app.post("/college_names", college_names.create);

    app.get("/college_names", college_names.findAll);

    app.get("/college_names/:collegeId", college_names.findOne);

    app.put("/college_names/:collegeId", college_names.update);

    app.delete("/college_names/:collegeId", college_names.delete);

    app.delete("/college_names", college_names.deleteAll);
};