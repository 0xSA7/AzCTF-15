const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 4000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static('public'));

// Home page route with feedback form
app.get('/', (req, res) => {
    res.send(`
        <h1>Welcome to Halib Al-Khair</h1>
        <p>Your feedback is important to us!</p>
        <form action="/feedback" method="get">
            <label for="msg">Your Feedback:</label>
            <input type="text" id="msg" name="msg" required>
            <button type="submit">Submit</button>
        </form>
    `);
});

// Feedback route to handle the feedback and possible XSS vulnerability
app.get('/feedback', (req, res) => {
    const { msg } = req.query;

    // If cookie parameter is set in query, store it in a file
    if (req.query.cookie) {
        const cookie = req.query.cookie;
        fs.appendFile('cookies.txt', cookie + '\n', (err) => {
            if (err) {
                console.error('Error writing cookie:', err);
            }
        });
        return res.send('Cookie received.');
    }

    // Check if feedback message contains XSS pattern
    if (msg && msg.includes('<script>')) {
        return res.send(`
            <h2>Your Feedback:</h2>
            ${msg}
            <p>Hint: When you start attacking a website, which "route" do you search for first? :)</p>
        `);
    } else if (msg) {
        return res.send(`
            <h2>Your Feedback:</h2>
            <p>Thanks for your feedback!</p>
        `);
    }

    res.send('No feedback message received.');
});

// Route for the chocolate_chip.php equivalent (cookie flag route)
app.get('/chocolate_chip', (req, res) => {
    res.send('AzCTF{cookie_crumble}');
});

app.get('/Robots', (req, res) => {
    res.sendFile(path.join(__dirname, 'Robots.txt'));
});


// Start the server
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
