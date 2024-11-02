from flask import Flask, request, send_file, render_template
import pandas as pd
import script
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['place-name']
    page=request.form['pages']
    scrapper=script.Scraper(user_input,page)
    
    csv_path = 'hotels_data.csv'
    

    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
