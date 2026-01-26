import flask
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Global players data
players = []

def load_players():
    """Load players from JSON file into global players list"""
    global players
    try:
        with open('players.json', 'r') as f:
            players = json.load(f)
    except FileNotFoundError:
        print("Error: players.json not found.")

# Initialize players data on startup
load_players()

# ---------------- Root Route ----------------
@app.route("/")
def index():
    return render_template('index.html')

# ---------------- API Routes ----------------

@app.route("/api/players", methods=['GET'])
def get_players():
    return jsonify(players)

@app.route("/api/players/<int:id>", methods=['GET'])
def get_player_by_id(id):
    # Looking for 'playerid' key from your JSON
    player = next((p for p in players if p['playerid'] == id), None)
    if player:
        return jsonify(player)
    return jsonify({"error": "Player not found"}), 404

@app.route("/api/players/save", methods=['POST'])
def save_player():
    data = request.get_json()
    
    # Ensure the incoming data has the correct ID
    try:
        target_id = int(data.get('playerid'))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid playerid provided"}), 400

    for i, player in enumerate(players):
        if player['playerid'] == target_id:
            # Update using your JSON keys: 'title' and 'highest score'
            players[i]['title'] = data.get('title', player['title'])
            players[i]['highest score'] = data.get('highest score', player['highest score'])
            
            # Optional: Write back to file to make changes permanent
            # with open('players.json', 'w') as f:
            #     json.dump(players, f, indent=2)
            
            return jsonify({"message": "Player updated successfully"}), 200 
            
    return jsonify({"error": "Player not found"}), 404

@app.route("/api/players/search", methods=['POST'])
def search_players(): # Fixed typo: serarch -> search
    criteria = request.get_json()
    query = criteria.get('query', '').lower() # Changed key to 'query' for generic search
    
    # Searches across both Title (Name/Country) and the ID
    filtered_players = [
        p for p in players 
        if query in p['title'].lower() or query == str(p['playerid'])
    ]
    
    return jsonify(filtered_players)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)