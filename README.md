### 🎶 Moodify: Emotion-Aware Song Recommendation System

Moodify is a custom **CNN-based song recommendation system** that links human facial emotions with music genres to recommend songs that match the user’s mood. The project includes both deep learning models for facial emotion recognition and a **React.js-based website** for real-time deployment and interaction.

---

### 📂 Repository Structure

The repository is organized to clearly separate the deep learning, inference, and web application components.

* `cnn/` 🎵: Contains Jupyter notebooks for training and evaluating different CNN models, including a custom architecture and transfer learning with pre-trained models.
* `inference/` 🧠: Includes notebooks for performing real-time song recommendations based on detected emotions and analyzing various mapping strategies.
* `model/` ✨: Stores the final, trained `CNN.h5` model file.
* `results/` 📈: Houses all the evaluation metrics, graphs, and CSV files generated from the models and recommendation systems, providing a comprehensive overview of performance.
* `sampling/` 📊: Demonstrates different data balancing and oversampling strategies.
* `spotify_data/` 🎶: Contains the `spotify_changed.csv` dataset and an EDA notebook for exploring its features.
* `requirements.txt`
* `README.md`

---

### 🚀 Features

#### Facial Emotion Recognition
* **Custom CNN model** trained on the FER2013 dataset.
* **Transfer learning** with **MobileNetV2**, **ResNet50**, and **VGG19** for benchmarking.

#### Song Recommendation Engine
* Multiple algorithms implemented:
    * Content-Based Filtering
    * Collaborative Filtering
    * Emotion-to-Genre Mapping
    * Graph-Based Recommendation

#### Real-Time Inference
* Maps facial expressions (e.g., happy, disgust, surprise) to corresponding music recommendations.

#### Spotify Integration
* Dataset preprocessed with the Spotify API, including genre, artist, and mood-based analysis.

#### Visualization & Evaluation
* Detailed visualizations for model performance, including **Confusion Matrix**, **ROC and PR Curves**, and **Classwise metrics**. 

#### Web Application (React.js)
* User-friendly website for interacting with the system.
* Real-time recommendations are deployed seamlessly.

---

### ⚙️ Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Moodify.git](https://github.com/your-username/Moodify.git)
    cd Moodify
    ```
2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv moodify_env
    # For Linux/Mac
    source moodify_env/bin/activate
    # For Windows
    moodify_env\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

### 📊 Training & Inference

#### Train Models
Run any of the training notebooks in the `cnn/` directory to train your models:
```bash
jupyter notebook cnn/CUSTOM_CNN.ipynb
