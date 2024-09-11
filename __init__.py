from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm5

@app.route("/contact/")
def contact():
    return render_template("contact.html")

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
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("graphique.html")

@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/Houssam78/5MCSI_Metriques/commits'
    commits_data = [
        # Exemple de données manuelles (au cas où la récupération dynamique n'est pas disponible)
        {'commit': {'author': {'date': '2024-02-11T11:57:27Z'}}},
        {'commit': {'author': {'date': '2024-02-11T12:01:15Z'}}},
        {'commit': {'author': {'date': '2024-02-11T12:34:22Z'}}},
    ]

    # Filtrage des minutes à partir des dates
    commit_minutes = {}
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        if minute in commit_minutes:
            commit_minutes[minute] += 1
        else:
            commit_minutes[minute] = 1

    return jsonify(results=commit_minutes)



if __name__ == "__main__":
  app.run(debug=True)
