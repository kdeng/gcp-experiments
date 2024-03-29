const express = require('express');
const app = express();

app.get('/', (req, res) => {
  const name = process.env.NAME || 'World';
  res.send(`Hello ${name}!`);
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`helloworld: listening on port ${port}`);
});

process.on('SIGTERM', function () {
  console.log('helloworld: received SIGTERM, exiting gracefully');
  process.exit(0);
});
