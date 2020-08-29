from flask import Flask, jsonify

# Dictionary of Justice League
# justice_league_members = [
#     {"superhero": "Aquaman", "real_name": "Arthur Curry"},
#     {"superhero": "Batman", "real_name": "Bruce Wayne"},
#     {"superhero": "Cyborg", "real_name": "Victor Stone"},
#     {"superhero": "Flash", "real_name": "Barry Allen"},
#     {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
#     {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
#     {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
# ]

#################################################
# Flask Setup
#################################################
# @TODO: Initialize your Flask app here
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# @TODO: Complete the routes for your app here

@app.route("/")
def home():
    return ("Climate App Home Page")

@app.route("/api/v1.0/precipitation")
def precip():
    """Return as json"""
    return jsonify(justice_league_members)

#not quite working yet, did it not work because above was not quite done?
@app.route("/api/v1.0/justice-league/<name>")
def justice_league_name(name):
    """Return the name of super hero"""
    for x in justice_league_members:
        if x['superhero'] == name:
            superhero = x
            print(superhero)
    return (superhero)

#she entered /api/v1.0/justice-league/Flash and it returned Flash's real name

if __name__ == "__main__":
    # @TODO: Create your app.run statement here
    # YOUR CODE GOES HERE
        app.run(debug=True)

