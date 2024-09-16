from flask import Flask, render_template
import os
from routes.timeseriers import timeseries_bp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

app.register_blueprint(timeseries_bp)

if __name__ == '__main__':
    app.run(debug=True)