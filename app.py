from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'secret_key'
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://skrnitc1999:saurabh12345@cluster0.8ark0.mongodb.net")
db = client['job_portal']
jobs_collection = db['jobs']

# ---------------- Home Page (Display Jobs) ---------------- #
@app.route('/')
def index():
    current_year = datetime.now().year
    jobs = jobs_collection.find().sort('_id', -1)  # Show latest jobs first
    return render_template('index.html', jobs=jobs, current_year = current_year)







# ---------------- Admin Panel - View/Add/Delete ---------------- #
@app.route('/update_jobs', methods=['GET'])
def update_jobs():
    jobs = list(jobs_collection.find().sort('_id', -1))
    for job in jobs:
        job['_id'] = str(job['_id'])  # convert ObjectId to string for HTML
    return render_template("update.html", jobs=jobs)








@app.route('/add_job', methods=['POST'])
def add_job():
    try:
        job_data = {
        'role': request.form['role'],
        'company': request.form['company'],
        'package': request.form['package'],
        'experience': request.form['experience'],
        'location': request.form['location'],
        'skills': request.form['skills'],
        'education': request.form['education'],
        'link': request.form['link']
    }
        jobs_collection.insert_one(job_data)
        flash("Job added successfully!", "success")
    except:
        flash("Failed to add job.", "error")
    return redirect('/update_jobs')

@app.route('/delete_job/<job_id>', methods=['POST'])
def delete_job(job_id):
    jobs_collection.delete_one({'_id': ObjectId(job_id)})
    return redirect(url_for('update_jobs'))








# ---------------- View Job Details ---------------- #
# @app.route("/jobs/<job_id>", methods=['GET'])
# def job_details(job_id):
#     job = jobs_collection.find_one({'_id': ObjectId(job_id)})
#     if not job:
#         return "Job does not exist."
#     return render_template("job_cards.html", **job)


@app.route("/jobs/<job_id>", methods=['GET'])
def job_details(job_id):
    job = jobs_collection.find_one({'_id': ObjectId(job_id)})
    if not job:
        flash("Job not found. It may have been removed.", "error")
        return redirect(url_for('index'))  # Replace 'index' with your home route function name
    return render_template("job_cards.html", **job)




# ---------------- Optional: Admin Quick Entry ---------------- #
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.form.to_dict()
        jobs_collection.insert_one(data)
        return "Job Created."
    return redirect(url_for('update_jobs'))

# ---------------- Optional: API for Deletion ---------------- #
@app.route("/jobs/delete/<job_id>", methods=['DELETE'])
def delete_job_api(job_id):
    result = jobs_collection.delete_one({'_id': ObjectId(job_id)})
    if result.deleted_count == 0:
        return "Job ID does not exist."
    return "Job deleted."







@app.route('/about')
def about():
    return render_template('about.html')







@app.route('/privacy')
def privacy():
    return render_template('privacy.html')





@app.route('/contact')
def contact():
    return render_template('contact.html')






@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic (store user, validate, etc.)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic (authentication, session, etc.)
        return redirect(url_for('index'))
    return render_template('login.html')





# ---------------- Run Server ---------------- #
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
