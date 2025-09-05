const express = require('express');
const router = express.Router();
const User = require('../models/User'); // Adjust the path to your User model
const Song = require('../models/Song'); // Adjust the path to your Song model
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const protect = require('../misc/protect.js');
// Signup Route
router.post('/signup', async (req, res) => {
  try {
    const { name, email, password } = req.body;

    // Check if user already exists
    let user = await User.findOne({ email });
    if (user) {
      return res.status(400).json({ message: "User already exists" });
    }
    
    // Create new user
    user = new User({ name, email, password });
    await user.save();
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
      expiresIn: '1d',
    });
    res.cookie('Token', token, {
      httpOnly: true, // Prevent JavaScript access to the cookie
      secure: process.env.NODE_ENV === 'production', // Use secure cookies in production
      maxAge: 24 * 60 * 60 * 1000, // 1 day in milliseconds
      sameSite: 'strict', // Restrict cookie to same-site requests
    });
    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error registering user', error });
  }
});
router.get('/protected-route', protect, (req, res) => {
    res.json({ message: 'You are accessing a protected route', user: req.user });
  });
// Login Route
router.post('/login', async (req, res) => {
    try {
      const { email, password } = req.body;
  
      const user = await User.findOne({ email }).select('+password');
      if (!user) {
        return res.status(400).json({ message: 'Invalid email or password' });
      }
  
      const isMatch = await bcrypt.compare(password, user.password);
      if (!isMatch) {
        return res.status(400).json({ message: 'Invalid email or password' });
      }
  
      const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
        expiresIn: '1d',
      });
      
      res.cookie('Token', token, {
        httpOnly: false, // Prevent JavaScript access to the cookie
        
        maxAge: 24 * 60 * 60 * 1000, // 1 day in milliseconds
        
      });
      res.json({ token, message: 'Login successful' });
    } catch (error) {
      res.status(500).json({ message: 'Error logging in', error });
    }
  });
  

// Like Song Route

router.post('/like', protect, async (req, res) => {
  try {
      const { name } = req.body;
      const userId = req.user.id;

      // Find the song by name
      const song = await Song.findOne({ track_name : name });
      if (!song) {
          return res.status(404).json({ message: 'Song not found' });
      }

      // Find user
      const user = await User.findById(userId);
      if (!user) {
          return res.status(404).json({ message: 'User not found' });
      }

      // Like the song
      if (!user.liked_songs.includes(song._id)) {
          user.liked_songs.push(song._id);
          user.disliked_songs = user.disliked_songs.filter(id => id.toString() !== song._id.toString());
          await user.save();

          // Update song's likes and dislikes
          song.likes.addToSet(userId); // `addToSet` ensures unique values in an array
          song.dislikes = song.dislikes.filter(id => id.toString() !== userId.toString());
          await song.save();

          return res.json({ message: 'Song liked successfully' });
      } else {
          return res.status(400).json({ message: 'Song already liked' });
      }
  } catch (error) {
      console.error('Error liking song:', error);
      res.status(500).json({ message: 'Error liking song', error: error.message });
  }
});

router.post('/unlike', protect, async (req, res) => {
  try {
      const { name } = req.body;
      const userId = req.user.id;

      // Find the song by name
      const song = await Song.findOne({ track_name: name });
      if (!song) {
          return res.status(404).json({ message: 'Song not found' });
      }

      // Find user
      const user = await User.findById(userId);
      if (!user) {
          return res.status(404).json({ message: 'User not found' });
      }

      // Unlike the song
      if (user.liked_songs.includes(song._id)) {
          // Remove from liked_songs
          user.liked_songs = user.liked_songs.filter(id => id.toString() !== song._id.toString());
          await user.save();

          // Update song's likes
          song.likes = song.likes.filter(id => id.toString() !== userId.toString());
          await song.save();

          return res.json({ message: 'Song unliked successfully' });
      } else {
          return res.status(400).json({ message: 'Song is not liked yet' });
      }
  } catch (error) {
      console.error('Error unliking song:', error);
      res.status(500).json({ message: 'Error unliking song', error: error.message });
  }
});
router.post('/undislike', protect, async (req, res) => {
  try {
      const { name } = req.body;
      const userId = req.user.id;

      // Find the song by name
      const song = await Song.findOne({ track_name: name });
      if (!song) {
          return res.status(404).json({ message: 'Song not found' });
      }

      // Find user
      const user = await User.findById(userId);
      if (!user) {
          return res.status(404).json({ message: 'User not found' });
      }

      // Undislike the song
      if (user.disliked_songs.includes(song._id)) {
          // Remove from disliked_songs
          user.disliked_songs = user.disliked_songs.filter(id => id.toString() !== song._id.toString());
          await user.save();

          // Update song's dislikes
          song.dislikes = song.dislikes.filter(id => id.toString() !== userId.toString());
          await song.save();

          return res.json({ message: 'Song undisliked successfully' });
      } else {
          return res.status(400).json({ message: 'Song is not disliked yet' });
      }
  } catch (error) {
      console.error('Error undisliking song:', error);
      res.status(500).json({ message: 'Error undisliking song', error: error.message });
  }
});

  

// Dislike Song Route
router.post('/dislike', protect, async (req, res) => {
  try {
      const { name } = req.body;
      const userId = req.user.id;

      // Find the song by name
      const song = await Song.findOne({track_name : name });
      if (!song) {
          return res.status(404).json({ message: 'Song not found' });
      }

      // Find user
      const user = await User.findById(userId);
      if (!user) {
          return res.status(404).json({ message: 'User not found' });
      }

      // Dislike the song
      if (!user.disliked_songs.includes(song._id)) {
          user.disliked_songs.push(song._id);
          user.liked_songs = user.liked_songs.filter(id => id.toString() !== song._id.toString());
          await user.save();

          // Update song's dislikes and likes
          song.dislikes.addToSet(userId); // `addToSet` ensures unique values in an array
          song.likes = song.likes.filter(id => id.toString() !== userId.toString());
          await song.save();

          return res.json({ message: 'Song disliked successfully' });
      } else {
          return res.status(400).json({ message: 'Song already disliked' });
      }
  } catch (error) {
      console.error('Error disliking song:', error);
      res.status(500).json({ message: 'Error disliking song', error: error.message });
  }
});

  

// Get User Data (including liked and disliked songs)
router.get('/user',protect, async (req, res) => {
  try {
    const userId = req.user.id;

    const user = await User.findById(userId)
      .populate('liked_songs')
      .populate('disliked_songs');
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    res.json({
      name: user.name,
      email: user.email,
      liked_songs: user.liked_songs,
      disliked_songs: user.disliked_songs
    });
  } catch (error) {
    res.status(500).json({ message: 'Error fetching user data', error });
  }
});
// Route to fetch a song by track name
router.post('/song', protect, async (req, res) => {
  try {
    const { track_name } = req.body;

    // Find the song by track name
    const song = await Song.findOne({ track_name: track_name })
      .populate('artists') // Populate artist details if they are referenced in the Song schema
      .populate('dislikes') // Populate dislikes if needed
      .populate('likes');    // Populate likes if needed

    if (!song) {
      return res.status(404).json({ message: 'Song not found' });
    }

    // Respond with the song data in the specified format
    res.json({
      track_id: song.track_id,
      track_name: song.track_name,
      artists: song.artists,          // Assuming this is an array
      album: song.album,
      release_year: song.release_year,
      duration_ms: song.duration_ms,
      mood: song.mood,
      __v: song.__v,
      dislikes: song.dislikes,        // Assuming this is an array
      likes: song.likes               // Assuming this is an array
    });
  } catch (error) {
    res.status(500).json({ message: 'Error fetching song data', error });
  }
});


router.get('/search', async (req, res) => {
  try {
    const { query } = req.query;
    if (!query) {
      return res.status(400).json({ message: 'Query is required' });
    }

    // Create a case-insensitive regex to match partial names
    const regex = new RegExp(query, 'i');
    const songs = await Song.find({ track_name: { $regex: regex } });

    res.json(songs);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
});
module.exports = router;
