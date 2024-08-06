from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_World():
    return "<p>Hello, World!</p>"
@app.route("/Student")
def show():
    return "<p>Test!</p>"
    

if __name__ == '__main__':
    app.run(debug=True)