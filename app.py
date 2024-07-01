from flask import Flask, render_template, request, jsonify, abort
import json
from gensim.models.fasttext import FastText
import pickle
import os
import numpy as np
from process import preprocess as preprocess
import uuid

app = Flask(__name__)

DATA_PATH = os.path.join("data", "data.json")


def generate_webindex():
    """Generate a random uuid4 as webindex"""
    return str(uuid.uuid4())


def read_job(path):
    """Read JSON file from path"""
    try:
        with open(path, 'r') as file:
            job_listings_data = json.load(file)
        return job_listings_data
    except FileNotFoundError:
        print(f"File not found: {path}")
        return []


# save extracted JSON data as job_listings
job_listings = read_job(DATA_PATH)
# get all categories in the data
categories = set(job['Category'] for job in job_listings)


def fetch_job_by_id(job_id):
    """Fetch a job using the webindex"""
    for job_listing in job_listings:
        if job_listing['Webindex'] == job_id:
            return job_listing


def fetch_jobs_by_category(category):
    """Fetch all jobs in the category"""
    jobs = []
    for job_listing in job_listings:
        if job_listing['Category'] == category:
            jobs.append(job_listing)
    return jobs


def add_job(title, company, description, category):
    """Add a job to the collection"""
    webindex = generate_webindex()
    new_job = {
        'Webindex': webindex,
        'Title': title,
        'Company': company,
        'Description': description,
        'Category': category
    }
    job_listings.append(new_job)

    if new_job in job_listings:
        # add the job to JSON
        with open('data/data.json', 'w') as file:
            json.dump(job_listings, file)
        return True
    else:
        return False


def docvecs(embeddings, docs):
    """Calculate weighted embeddings"""
    vecs = np.zeros((len(docs), embeddings.vector_size))
    for i, doc in enumerate(docs):
        valid_keys = [term for term in doc if term in embeddings.key_to_index]
        if valid_keys:
            docvec = np.vstack([embeddings[term] for term in valid_keys])
            docvec = np.sum(docvec, axis=0)
            vecs[i, :] = docvec
        else:
            vecs[i, :] = np.zeros(embeddings.vector_size)
    return vecs


@app.route('/')
def index():
    """Index page"""
    return render_template('index.html', job_listings=job_listings, categories=categories)


@app.route('/switch_category/<category>')
def load_category(category):
    """Loads jobs by category"""
    if category in categories:
        job_by_category = fetch_jobs_by_category(category=category)
        return render_template('index.html', job_listings=job_by_category, categories=categories)
    else:
        abort(404)


@app.route('/allJobs')
def load_all_jobs():
    """Loads all jobs"""
    return render_template('index.html', job_listings=job_listings, categories=categories)


@app.route('/job/<category>/<job_id>')
def job_details(job_id, category):
    """Show more info on jobs"""
    # Find the job details based on the job index
    job = fetch_job_by_id(job_id)

    if job:
        return render_template('jobDetails.html', job=job)
    else:
        abort(404)


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    """Classifies the job"""
    if request.method == 'POST':
        # Read the content
        title = request.form['title']
        content = request.form['description']

        # Concatenate the content
        content_concat = title + " " + content

        # Process the content
        tokenized_data = preprocess.preprocess(content_concat)

        # Load the FastText model
        bbcFT = FastText.load("model/desc_FT.model")
        bbcFT_wv = bbcFT.wv

        # Generate vector representation of the tokenized data
        bbcFT_dvs = docvecs(bbcFT_wv, [tokenized_data])

        # Load the classification model
        pkl_filename = "model/descFT_LR.pkl"
        with open(pkl_filename, 'rb') as file:
            model = pickle.load(file)

        # Predict the label of tokenized_data
        y_pred = model.predict(bbcFT_dvs)
        y_pred = y_pred[0]

        if y_pred == "Accounting_Finance":
            y_pred = "accounting"
        elif y_pred == "Healthcare_Nursing":
            y_pred = "healthcare"

        # Set the predicted message
        predicted_message = y_pred

        # save response
        response_data = {'classifiedJobType': predicted_message}

        # release response
        return json.dumps(response_data)


@app.route('/addJob', methods=['GET', 'POST'])
def addJob():
    """Add a job to collection"""
    if request.method == 'POST':
        # extract info
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        category = request.form['category']

        # invokes method to add to collection
        success = add_job(title, company, description, category)

        # on success returns response as success
        if success:
            response_data = {'message': 'Job added successfully'}
        else:
            response_data = {'message': 'Failure'}

        # Return the response as JSON
        return jsonify(response_data)


@app.errorhandler(404)
def page_not_found(e):
    """returns error page on error"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """returns error page on error"""
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run()
    
# ### References

# - [1]Gallagher, L 20230, 'ex1_movie_preprocess.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.
# - [2]Gallagher, L 20230, 'w08_ex1_solution.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.
# - [3]Gallagher, L 20230, 'w09_act1_term_embedding.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.
# - [4]Gallagher, L 20230, 'w09_act2_embedding_classification.ipynb', Lab Material, COSC2820, RMIT University, Melbourne.
