const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = 5000;

// Use express.json() middleware to parse JSON requests
app.use(express.json());

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Serve the main index page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Serve the login page
app.get('/login.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Serve the dashboard page
app.get('/dashboard.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// Serve the employee data
app.get('/data/employees.json', (req, res) => {
    res.sendFile(path.join(__dirname, 'data', 'employees.json'));
});

// Route to handle login POST requests
app.post('/login', (req, res) => {
    const { email, password } = req.body;

    // Load employee data
    fs.readFile(path.join(__dirname, 'data', 'employees.json'), 'utf-8', (err, data) => {
        if (err) return res.status(500).send('Error reading employee data');

        const employees = JSON.parse(data).employees;
        const user = employees.find(emp => emp.email === email && emp.password === password);

        if (user) {
            return res.redirect('/dashboard.html');
        } else {
            return res.status(401).send('Invalid credentials');
        }
    });
});

// Handle 404 errors
app.use((req, res) => {
    res.status(404).send('Page not found');
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
