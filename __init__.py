from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from flask import Flask, jsonify
from urllib.request import urlopen
import json
from datetime import datetime
from collections import Counter
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
   return render_template('contact.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
     return render_template('graphique.html')

@app.route("/histogramme/")
def monhistogramme():
     return render_template('histogramme.html')
  
@app.route('/commits/')
def moncommits():
     return render_template('commits.html')

@app.route('/api/commits/minutes')
def commits_minute_distribution():
    # API GitHub d'origine (à ne pas changer)
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits?per_page=100'
    response = urlopen(url)
    raw_content = response.read()
    commits = json.loads(raw_content.decode('utf-8'))

    minutes = []
    for commit in commits:
        date_str = commit.get('commit', {}).get('author', {}).get('date')
        if date_str:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(dt.minute)

    counter = Counter(minutes)
    results = [{'minute': m, 'count': counter.get(m, 0)} for m in range(60)]

    return jsonify(results)
  

  
if __name__ == "__main__":
  app.run(debug=True)
