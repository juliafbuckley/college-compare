const CollegeName = require("../models/college-name.model.js");

// Create and Save 
exports.create = (req, res) => {
    // check if req is valid
    if (!req.body) {
        res.status(400).send({
            message: "Content cannot be empty"
        });
    }

    // Create college name object based on req
    const college_name = new CollegeName({
        name: req.body.name
    });

    // Make database command
    CollegeName.create(college_name, (err, data) => {
        if (err){
            res.status(500).send({
                message:
                    err.message || "Error while creating college name"
            });
        } else {
            res.send(data);
        }
    });
};

// Retrieve all 
exports.findAll = (req, res) => {
    // Make database command
    CollegeName.getAll((err, data) => {
        if (err)
            res.status(500).send({
                message:
                    err.message || "Error while retrieving college names"
            });
        else res.send(data);
    }); 
};

// Find a single
exports.findOne = (req, res) => {
    // Make database command
    CollegeName.findById(req.params.collegeId, (err, data) => {
        if (err){
            if (err.kind === "not_found") {
                res.status(404).send({
                    message: `Not found college with id ${req.params.collegeId}`
                });
            }
            else {
                res.status(500).send({
                    message:
                        err.message || "Error while retrieving college names"
                });
            }
        }
        else res.send(data);
    });  
};

// Update
exports.update = (req, res) => {
    // check if req is valid
    if (!req.body) {
        res.status(400).send({
            message: "Content cannot be empty"
        });
    }

    // Create college name object based on req
    const college_name = new CollegeName({
        name: req.body.name
    });

    // Make database command
    CollegeName.updateById(req.params.collegeId, college_name, (err, data) => {
        if (err){
            if (err.kind === "not_found") {
                res.status(404).send({
                    message: `Not found college with id ${req.params.collegeId}`
                });
            }
            else {
                res.status(500).send({
                    message:
                        err.message || "Error while updating college name"
                });
            }
        }
        else res.send(data);
    });
};

// Delete 
exports.delete = (req, res) => {
    // Make database command
    CollegeName.remove(req.params.collegeId, (err, data) => {
        if (err){
            if (err.kind === "not_found") {
                res.status(404).send({
                    message: `Not found college with id ${req.params.collegeId}`
                });
            }
            else {
                res.status(500).send({
                    message:
                        err.message || "Error while retrieving college names"
                });
            }
        }
        else res.send(data);
    });  
};

// Delete all 
exports.deleteAll = (req, res) => {
    // Make database command
    CollegeName.deleteAll((err, data) => {
        if (err)
            res.status(500).send({
                message:
                    err.message || "Error while deleting college names"
            });
        else res.send(data);
    }); 
};