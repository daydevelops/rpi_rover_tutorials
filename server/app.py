from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def showController():
    return render_template('controller.html')

if __name__ == "__main__":
	app.run()
