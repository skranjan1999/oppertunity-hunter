from flask import Flask, jsonify, request, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'

# Sample user data (replace with database integration)
users = {
    'admin': {'password': generate_password_hash('admin123'), 'role': 'admin'},
    'user': {'password': generate_password_hash('user123'), 'role': 'user'}
}

# Sample job data (replace with database queries later)
jobs = {
    1 : {
        "id":1,
    "role": "Software Engineer",
    "company": "Tech Corp",
    "package": "12 LPA",
    "experience": "2+ years",
    "location": "Bangalore",
    "description": "Develop and maintain web applications.",
    "responsibilities": "Write clean code, collaborate with teams.",
    "skills": "Python, Flask, React",
    "education": "B.Tech in Computer Science",
    "link" : "https://jobs.smartrecruiters.com/AbstrabitTechnologiesPvtLtd/744000052023820-full-stack-engineer-0-to-2-years-remote-opportunity"
}

}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users and check_password_hash(users[username]['password'], password):
        session['username'] = username
        session['role'] = users[username]['role']
        return jsonify({'message': 'Login successful', 'role': users[username]['role']})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'})




@app.route('/update_job', methods=['GET'])
def update_job():
    return render_template("update.html")





@app.route('/')
def index():
    return render_template('index.html', jobs = jobs)





@app.route("/jobs/<index>", methods=['GET'])
def lwstudentinfo(index):
    if int(index) <= 0:
        return "Not Exists"
    elif int(index) in jobs:
        return render_template(
                        "job_cards.html",
                        id = jobs[int(index)]['id'],
                        role = jobs[int(index)]['role'],
                        company = jobs[int(index)]['company'],
                        package = jobs[int(index)]['package'],
                        experience = jobs[int(index)]["experience" ],
                        location = jobs[int(index)]["location" ],
                        description = jobs[int(index)]["description" ],
                        responsibilities = jobs[int(index)]["responsibilities" ],
                        skills = jobs[int(index)]["skills" ],
                        education = jobs[int(index)]["education" ],
                        link = jobs[int(index)]["link" ],
                       
                        )
    else:
        return "Not Exists"





@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form:
            id = request.form['id']
            role =  request.form['role'],
            company = request.form['company'],
            package = request.form['package'],
            experience = request.form['experience'],
            location =  request.form['location'],
            description = request.form['description'],
            responsibilities =  request.form['responsibilities'],
            skills = request.form['skills'],
            education = request.form['education']
            link = request.form['link']



            nextId =  list ( jobs.keys( ) ) [ -1 ]  + 1 

            jobs[nextId] = {
                'id' : id,
                'role': request.form['role'],
                'company': company,
                'package': request.form['package'],
                'experience': request.form['experience'],
                'location': request.form['location'],
                'description': request.form['description'],
                'responsibilities': request.form['responsibilities'],
                'skills': request.form['skills'],
                'education': request.form['education'],
                'link': link
            }

            print(request.form)

        elif request.json:
            jobs[list ( jobs.keys( ) ) [ -1 ]  + 1 ]  =  request.json

        else:
            print("not supported")
            return 'not supported'
    return "Job Created.."




@app.route("/jobs/delete/<index>", methods=['DELETE'])
def lwstudentdelete(index):
    if int(index) in jobs:
        del jobs[int(index)]

    else:
        return "ID not Exist"

    return "record deleted..."






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')