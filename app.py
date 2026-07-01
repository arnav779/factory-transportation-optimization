from flask import Flask, render_template

app = Flask(_name_)

@app.route('/')
def home():
    return """
    <h1>🍬 Nassau Candy Distributor Project</h1>
    <p>Welcome to the Internship Project Dashboard</p>
    <p>Project is successfully running 🚀</p>
    """

if _name_ == '_main_':
    app.run(debug=True)