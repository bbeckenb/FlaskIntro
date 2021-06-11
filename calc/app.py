# Put your app in here.
from flask import Flask, request
from operations import add

app = Flask(__name__)

print(add(4, 5))
# print(sub(4, 5))
# print(mult(4, 5))
# print(div(4, 5))

@app.route('/add')
def add_form():
    return """
    <h1>Add a and b</h1> 
    <form method="POST">
        <input type='number' placeholder='a' name='a'/>
        <input type='number' placeholder='b' name='b'/>
        <button>Submit</button>
    </form>
    """

@app.route('/add', methods=["POST"])
def perform_addition():
    a = request.form["a"]
    b = request.form["b"]
    print(request.form)
    return f"""
    <h1>Your addition result is {add(a,b)}</h1>
    """




