const jwt = require('jsonwebtoken');
const User = require('../models/User'); // Adjust the path as necessary

const protect = async (req, res, next) => {
  let token;
  console.log("protect",req.cookies)
  // Retrieve token from cookies
  if (req.cookies && req.cookies.Token) {
    token = req.cookies.Token;
  }

  if (!token) {
    return res.status(401).json({ message: 'Not authorized, no token' });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(decoded.id).select('-password'); // Get user info excluding password
    next();
  } catch (error) {
    res.status(401).json({ message: 'Not authorized, token failed' });
  }
};


module.exports = protect;
