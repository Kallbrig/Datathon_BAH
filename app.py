from flask import Flask, render_template, jsonify, request
import random
import csv
import os
import glob

app = Flask(__name__)

# Data storage for demonstration purposes
restaurants = [{"id": 1, "image": "images/food1.jpeg"}, {"id": 2, "image": "images/food2.jpeg"}]  # Add more
ratings = {}

def save_rating_to_file(restaurant_id, rating):
    file_exists = os.path.isfile('ratings.csv')
    with open('ratings.csv', 'a', newline='') as csvfile:
        fieldnames = ['restaurant_id', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write the header if the file doesn't exist

        writer.writerow({'restaurant_id': restaurant_id, 'rating': rating})


@app.route('/rate', methods=['POST'])
def rate():
    data = request.json
    restaurant_id = data['restaurant_id']  # Keep it as a string
    rating = data['rating']

    # Store the rating and save to file
    ratings[restaurant_id] = rating  # Use string as the key
    save_rating_to_file(restaurant_id, rating)

    restaurants = get_restaurants()
    random.shuffle(restaurants)
    next_restaurant = restaurants[0]

    return jsonify(next_restaurant)


def get_restaurants():
    image_files = glob.glob('static/images/*.jpeg')  # Modify if other image formats are used
    return [{"id": os.path.basename(image), "image": "images/" + os.path.basename(image)} for image in image_files]

ratings = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/preferences')
def preferences():
    return render_template('pref.html')

@app.route('/explore')
def explore():
    restaurants = get_restaurants()
    random.shuffle(restaurants)
    return render_template('explore.html', restaurant=restaurants[0])


@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/map')
def map():
    return render_template('recommend.html')

if __name__ == '__main__':
    app.run(debug=True)
