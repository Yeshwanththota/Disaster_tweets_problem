from flask import Flask, request, redirect, url_for, render_template
import pickle
import joblib
import os

# Create an instance of the Flask class
# With the name of the application’s modules
# This way Flask knows where to look for templates, static files, etc.
app = Flask(__name__, template_folder='templates')

# Create the / API route and render the root HTML page
@app.route('/', methods=['GET'])
def main():
    return(render_template('main.html'))

# Create the /predict API route
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Use pickle to load in vectorizer.
    # with open() is a Python function that opens a file object
    # rb means read in binary
    # Learn more: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files

    current_dir = os.path.dirname(__file__)

    # Construct the paths to the files
    vectorizer_path = os.path.join(current_dir, 'model', 'tfidf_vectorizer.pkl')
    model_path = os.path.join(current_dir, 'model', 'classifier.pkl')

    # Use joblib to load in the vectorizer and model
    with open(vectorizer_path, 'rb') as f:
        vectorizer = joblib.load(f)
    with open(model_path, 'rb') as f:
        model = joblib.load(f)
    # Get the form responses from the API request
    if request.method == 'POST':
        
        message = request.form['Tweet']
        if message:
        # A Python dictionary to store the 2 types of tweets
        # Based on the encoded values in the dataset
            tweet_types = {
                0: "Not a real Disaster",
                1: "Real Disaster",
                }
        
        # Vectorize the passed messaage and make prediction
            prediction = model.predict(vectorizer.transform([message]))

        # The result is an array containing the predicted tweet type 
        # Get the prediction text using the tweet_types dictionary above
        # You can do this automatically by inverting the result
        # Like we did in the notebook using LabelEncoder().inverse_transform()
        # But you will need to fit the encoder first
        # To avoid working with the dataset again here, the tweet_types dictionary above will suffice
            result = tweet_types[prediction[0]]
        else:
            return "Bad Request", 400  # Return an error if message is empty

    # If the request method is not a POST request
    # E.g, accessing the /predict route manually (GET)
    # Redirect back to the main page
    else:
        return(redirect(url_for('main')))

    # Render the result page
    # Return the resulting data to the result page
    # This data will be handled in the result page
    return(render_template('result.html', result=result))
    

# Catch 404 errors and render the 404 error page
@app.errorhandler(404)
def notFound(error):
    return render_template('404.html'), 404

# Run the app
if __name__ == '__main__':
    app.run()