const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// صفحة البداية
app.get('/', (req, res) => {
  res.send(`
    <h1>Welcome to the CTF Challenge!</h1>
    <p>Can you find the hidden flag?</p>
    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
      <strong>Hint:</strong> Check the <code>_git</code> directory for clues.
    You’ve been granted access to a mysterious web portal developed by a secretive agency.
Rumor has it... some secrets were accidentally leaked and then “deleted.”
But in the world of version control, the past never really disappears.
Can you dig through the code’s history and retrieve what was once hidden?

<br>
<b>Hint:</b> 
What's the diffrence between "-" and "_" ?
</div>
<div>
</div>

  `);
});

// عرض ملف config فقط
app.get('/_git/config', (req, res) => {
  res.sendFile(path.join(__dirname, '_git', 'config'));
});

// منع أي طلبات تانية داخل _git/
app.use('/_git', (req, res) => {
  res.status(403).send('Forbidden');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
