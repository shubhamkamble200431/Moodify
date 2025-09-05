import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
# Load the songs data
songs_df = pd.read_csv('Spotify_changed.csv')
# print("Original data preview:\n", songs_df.head())

# Initialize mood-to-genre mapping
expression_to_mood = {
    'happy': 'happy',
    'sad': 'sad',
    'angry': 'energetic',
    'surprise': 'energetic',
    'disgust': 'energetic',
    'neutral': 'calm',
    'fear': 'calm'
}

# Fill NaN values with 0 for any existing ratings
songs_df = songs_df.fillna(0)

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

def calculate_total_ratings():
    # Identify user rating columns dynamically
    user_rating_columns = songs_df.columns.difference(
        ['track_id', 'track_name', 'album', 'artists', 'release_year', 'duration_ms', 'mood']
    )
    # Calculate total ratings across all user columns
    songs_df['total_rating'] = songs_df[user_rating_columns].sum(axis=1)

def get_highest_rated_song():
    # Ensure total ratings are calculated before fetching the highest rated song
    highest_rated_song = songs_df.loc[songs_df['total_rating'].idxmax()]
    return highest_rated_song.to_dict()

def get_mood_based_recommendations(mood):
    genre = expression_to_mood.get(mood, None)
    if genre:
        # Filter by mood and return a random selection if there are more than 5
        recommended_songs = songs_df[songs_df['mood'] == genre]
        if not recommended_songs.empty:
            return recommended_songs.sample(n=min(9, len(recommended_songs))).to_dict(orient='records')
    return []

@app.route('/recommend', methods=['POST'])
def recommend():
    
    user_name = request.json['user_name']
    mood = request.json.get('mood', None)
    if user_name not in songs_df.columns:
            songs_df[user_name] = 0  # Initialize the user's column with 0
            songs_df.to_csv('Spotify_changed.csv', index=False)  # Save changes back to the original CSV
    # Calculate total ratings once to ensure accurate results before recommendation
    calculate_total_ratings()
    
    # Get the highest-rated song
    highest_rated_song = get_highest_rated_song()

    # Reset user rating back to 1 if the user has not liked or disliked any song
    current_user_rating = songs_df.loc[songs_df['track_id'] == highest_rated_song['track_id'], user_name].values[0]
    
    if current_user_rating == 0:
        songs_df.loc[songs_df['track_id'] == highest_rated_song['track_id'], user_name] = 0 # Reset to 1 if no interaction has occurred

    # Get mood-based recommendations if mood is provided
    mood_recommendations = []
    if mood:
        mood_recommendations = get_mood_based_recommendations(mood)

    # Recalculate total ratings after potential reset
    calculate_total_ratings()

    # Exclude 'total_rating' from the response
    highest_rated_song.pop('total_rating', None)  # Remove total_rating from the dict
   
    return jsonify({
        "highest_rated_song": highest_rated_song,
        "mood_based_recommendations": mood_recommendations
    })

def update_rating(track_id, action, user_name):
    global songs_df

    # Check if the track_id exists in the songs DataFrame
    if track_id in songs_df['track_id'].values:
        # Initialize user's column if it doesn't exist
        if user_name not in songs_df.columns:
            songs_df[user_name] = 0  # Initialize the user's column with 0

        current_rating = songs_df.loc[songs_df['track_id'] == track_id, user_name].values[0]

        # Log the current rating for debugging
        print(f"Current rating for {user_name} on track {track_id}: {current_rating}")

        # Update rating based on the action
        if action == 1:  # Like
            if current_rating == 1:
                songs_df.loc[songs_df['track_id'] == track_id, user_name] = 0  # Reset to 0 if already liked
            else:
                songs_df.loc[songs_df['track_id'] == track_id, user_name] = 1  # Set to like
        elif action == -1:  # Dislike
            if current_rating == -1:
                songs_df.loc[songs_df['track_id'] == track_id, user_name] = 0  # Reset to 0 if already disliked
            else:
                songs_df.loc[songs_df['track_id'] == track_id, user_name] = -1  # Set to dislike

        # Log the updated rating for debugging
        updated_rating = songs_df.loc[songs_df['track_id'] == track_id, user_name].values[0]
        print(f"Updated rating for {user_name} on track {track_id}: {updated_rating}")

        # Calculate total ratings only after updating
        calculate_total_ratings()
        
        # Log total ratings for debugging
        print(f"Total ratings after update for track {track_id}: {songs_df['total_rating'].loc[songs_df['track_id'] == track_id].values[0]}")

        # Save DataFrame to CSV excluding the 'total_rating' column
        songs_df.drop(columns=['total_rating'], inplace=True, errors='ignore')  # Remove total_rating column before saving
        songs_df.to_csv('Spotify_changed.csv', index=False)  # Save changes back to the original CSV

@app.route('/like', methods=['POST'])
def like():
    track_id = request.json['track_id']
    user_name = request.json['user_name']
    
    update_rating(track_id, 1, user_name)
    return jsonify({"message": "Liked!"})

@app.route('/dislike', methods=['POST'])
def dislike():
    track_id = request.json['track_id']
    user_name = request.json['user_name']
    print("fdvdvervv",track_id , user_name)
    update_rating(track_id, -1, user_name)
    return jsonify({"message": "Disliked!"})

@app.route('/reset_ratings', methods=['POST'])
def reset_ratings():
    user_name = request.json['user_name']
    
    # Reset all ratings for the specified user to 0
    if user_name in songs_df.columns:
        songs_df[user_name] = 0  # Set all ratings for this user to 0
        songs_df.drop(columns=['total_rating'], inplace=True, errors='ignore')  # Remove total_rating column before saving
        songs_df.to_csv('Spotify_changed.csv', index=False)  # Save changes back to the original CSV
        return jsonify({"message": f"All ratings for user {user_name} have been reset to 0."})
    else:
        return jsonify({"error": f"User {user_name} does not exist."}), 404

if __name__ == '__main__':
    app.run(port=9000, debug=True)
