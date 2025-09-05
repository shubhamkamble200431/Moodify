const express = require('express');
const cookieParser = require('cookie-parser');
const connectDB = require('./db.js');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config({ path: './.env' }); // Configure dotenv once

const app = express();
app.use(cookieParser());
connectDB();

app.use(cors({
    origin: 'http://localhost:3000', // Your frontend origin
    credentials: true, // Allow cookies
  }));
app.use(express.json());

// Routes
app.use('/api/auth', require('./routes/auth.js'));

const PORT = process.env.PORT || 8001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
