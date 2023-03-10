const path = require('path');
// helps parse the request and create req.body
const bodyParser = require('body-parser');
// for building REST APIs
const express = require("express");

const PORT = process.env.PORT || 3001;

const app = express();

// Have Node serve the files for our built React app
//app.use(express.static(path.resolve(__dirname, '../client/build')));

// parse requests of content-type: application/json
app.use(bodyParser.json());

// parse requests of content-type: application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));


// GET reqs to the /api route
app.get("/", (req, res) => {
    res.json({ message: "Hello from server!" });
});

// Handle all other GET requests - responds with React app
// app.get('*', (req, res) => {
//     res.sendFile(path.resolve(__dirname, '../client/build', 'index.html'));
// });

require("./routes/college-name.routes.js")(app);

// listen for requests
app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});