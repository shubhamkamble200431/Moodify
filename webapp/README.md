# Webapp

A **web app utilizing the FER model** built with **React**.  
It captures a user’s **image or video**, predicts their **mood** via backend ML models, and recommends personalized songs.  
Users can also **like/dislike songs**, manage their **library**, and **sign up / log in** securely.  

---

## 🚀 Features

- 📷 **Mood Detection**  
  - Upload an image or record a short video.  
  - ML backend (`/predict`) analyzes mood.  
  - Mood-based recommendations are fetched from `/recommend`.  

- 🎶 **Personalized Song Recommendations**  
  - Recommendations adapt based on detected mood.  
  - Highest-rated song and recommendations stored in localStorage.  

- ❤️ **Library Management**  
  - Like/Dislike songs.  
  - View categorized lists of liked and disliked songs.  

- 👤 **Authentication**  
  - **Signup/Login** system with JWT (stored in localStorage).  
  - Secure cookie handling with `withCredentials`.  

- 📚 **Clean Layout & Sidebar Navigation**  
  - Navigate easily between **Home**, **Search**, and **Library**.  

---

## 🛠️ Tech Stack

- **Frontend:** React, React Router, Axios  
- **Backend 1 (Authentication & DB):** Node.js, Express, MongoDB  
- **Backend 2 (ML Services):** Flask + TensorFlow/Keras, OpenCV  
 
- **Styling:** CSS (custom + component-specific)  
- **Icons:** react-icons, PNG assets  
- **CSV Handling:** papaparse (used in Home)  
- **Backend important endpoints:** Flask/Node.js APIs for  
  - Authentication (`/api/auth/*`)  
  - Mood Prediction (`/predict`)  
  - Recommendations (`/recommend`)  

---

## 📂 Project Structure

```
emotion-detector/src/
│── Home.js        # Mood detection + recommendation logic
│── Layout.js      # Base layout with sidebar + content area
│── Library.js     # Displays liked/disliked songs
│── Login.js       # User login form
│── SignUp.js      # User signup form
│── SongCard.js    # UI for each song with like/dislike buttons
│── assets/        # Images (like/dislike icons, camera.png, etc.)
│── styles/        # CSS files (Sidebar.css, Library.css, SongCard.css)
```

server/
│── server.js       # Node.js Express server (Auth API)
│── db.js           # Database connection (MongoDB)
│── routes/
│    └── auth.js    # Auth routes (login, signup, user info)

Moodify/
│── FER_image.py    # Flask service for image-based mood detection
│── FER_video.py    # Flask service for video-based mood detection
│── CNN.h5          # Pre-trained emotion recognition model
│── haarcascade_frontalface_default.xml # Face detection cascade

---

## ⚡ Getting Started

## Frontend

```
cd emotion-detector
npm install
npm start
```

## Backend 1 (Node.js)

```
cd server
npm install
node server.js
```

## Backend 2 (Flask)

```
cd Moodify
pip install -r requirements.txt
python FER_image.py
python FER_video.py
```

---


## 📌 Features

- **Image-based mood detection**: Upload an image to predict mood and get song recommendations.
- **Video-based mood detection**: Capture a video to predict mood and get song recommendations.
- **Personalized library**: Like or dislike songs to create a personalized library.
- **User authentication**: Signup and login to create an account and access personalized recommendations.

---

## 📌 Usage

1. **Signup/Login** to create an account.  
2. On the **Home page**, upload an image or capture a video.  
3. Mood is predicted → recommendations fetched.  
4. Like/Dislike songs to personalize your **Library**.  
5. Navigate via **Sidebar** between Home, Search, and Library.  


  
