// basic crud functions for the college-name table
const sql = require("./db.js");

// constructor
const CollegeName = function(college_name) {
    this.name = college_name.name;
};

// Create
CollegeName.create = (newCollegeName, result) => {
    sql.query("INSERT INTO college_name SET ?", newCollegeName, (err, res) => {
        if (err) {
            console.log("error: ", err);
            result(err, null);
            return;
        }

        console.log("created college name: ", { id: res.insertId, ...newCollegeName });
        result(null, { id: res.insertId, ...newCollegeName });
    });
};

// Read
CollegeName.findById = (collegeNameId, result) => {
    sql.query(`SELECT * FROM college_name WHERE id = ${collegeNameId}`, (err, res) => {
        if (err) {
            console.log("error: ", err);
            result(err, null);
            return;
        }
        if (res.length) {
            console.log("found college name: ", res[0]);
            result(null, res[0]);
            return;
        }
        
        // not found
        result({ kind: "not_found" }, null);
    });
};

CollegeName.getAll = result => {
    sql.query("SELECT * FROM college_name", (err, res) => {
        if (err) {
            console.log("error: ", err);
            result(err, null);
            return;
        }

        console.log("college names: ", res);
        result(null, res)
    });
};

CollegeName.updateById = (id, college_name, result) => {
    sql.query("UPDATE college_name SET name=? WHERE id=?", [college_name.name, id], (err, res) => {
        if (err) {
            console.log("error: ", err);
            result(null, err);
            return;
        }
        if (res.affectedRows == 0) {
            // could not find college with id
            result({ kind: "not_found" }, null);
            return;
        }
        console.log("updated college name: ", { id: id, ...college_name });
        result(null, { id: id, ...college_name });
    }
    );
};

CollegeName.remove = (id, result) => {
    sql.query("DELETE FROM college_name WHERE id=?", id, (err, res) => {
        if (err) {
            console.log("error: ", err);
            result(null, err);
            return;
        }
        if (res.affectedRows == 0) {
            result({ kind: "not_found" }, null);
            return;
        }

        console.log("deleted college name with id: ", id);
        result(null, res);
    });
};

CollegeName.removeAll = result => {
    sql.query("DELETE FROM college_name", (err, res) => {
        if (err) {
            console.log("error: ", err);
            result(null, err);
            return;
        }
        console.log(`deleted ${res.affectedRows} college_name`);
        result(null, res);
    });
};

module.exports = CollegeName;