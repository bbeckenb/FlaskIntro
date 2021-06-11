# Put your app in here.
from flask import Flask, request
from operations import *

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
    a = int(request.form["a"])
    b = int(request.form["b"])
    print(request.form)
    return f"""
    <h1>Your addition result is {add(a,b)}</h1>
    """

@app.route('/sub')
def sub_form():
    return """
    <h1>Subtract a and b</h1> 
    <form method="POST">
        <input type='number' placeholder='a' name='a'/>
        <input type='number' placeholder='b' name='b'/>
        <button>Submit</button>
    </form>
    """

@app.route('/sub', methods=["POST"])
def subtraction_addition():
    a = int(request.form["a"])
    b = int(request.form["b"])
    print(request.form)
    return f"""
    <h1>Your subtraction result is {sub(a,b)}</h1>
    """

@app.route('/mult')
def mult_form():
    return """
    <h1>Multiply a and b</h1> 
    <form method="POST">
        <input type='number' placeholder='a' name='a'/>
        <input type='number' placeholder='b' name='b'/>
        <button>Submit</button>
    </form>
    """

@app.route('/mult', methods=["POST"])
def perform_multiplication():
    a = int(request.form["a"])
    b = int(request.form["b"])
    print(request.form)
    return f"""
    <h1>Your multiplication result is {mult(a,b)}</h1>
    """

@app.route('/div')
def div_form():
    return """
    <h1>Divide a and b</h1> 
    <form method="POST">
        <input type='number' placeholder='a' name='a'/>
        <input type='number' placeholder='b' name='b'/>
        <button>Submit</button>
    </form>
    """

@app.route('/div', methods=["POST"])
def perform_division():
    a = int(request.form["a"])
    b = int(request.form["b"])
    print(request.form)
    return f"""
    <h1>Your addition result is {div(a,b)}</h1>
    """


