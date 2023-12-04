import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    int_features = [float(x) for x in request.form.values()]

    if int_features[0]==0:
        f_features=[0,0,0]+int_features[1:]
    elif int_features[0]==1:
        f_features=[1,0,0]+int_features[1:]
    elif int_features[0]==2:
        f_features=[0,1,0]+int_features[1:]
    else:
        f_features=[0,0,1]+int_features[1:]

    if f_features[6]==0:
        fn_features=f_features[:6]+[0,0]+f_features[7:]
    elif f_features[6]==1:
        fn_features=f_features[:6]+[1,0]+f_features[7:]
    else:
        fn_features=f_features[:6]+[0,1]+f_features[7:]

    final_features = [np.array(fn_features)]
    predict = model.predict(final_features)

    if predict==0:
        output='Normal'
    elif predict==1:
        output='DOS'
    elif predict==2:
        output='PROBE'
    elif predict==3:
        output='R2L'
    else:
        output='U2R'

    return render_template('index.html', output=output)

@app.route('/scan', methods=['POST'])
def scan():
    api_key = '991fee67ed8311a3982846c6ab1d35afa7aac82aeb2cdf4d0ef888545f8eb550'
    url = request.form['url']
    scan_url = f'https://www.virustotal.com/api/v3/urls/{url}'
    headers = {
        'x-apikey': api_key
    }

    response = requests.get(scan_url, headers=headers)
    scan_data = response.json()

    return render_template('result.html', data=scan_data)

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    predict = model.predict([np.array(list(data.values()))])

    if predict==0:
        output='Normal'
    elif predict==1:
        output='DOS'
    elif predict==2:
        output='PROBE'
    elif predict==3:
        output='R2L'
    else:
        output='U2R'

    return jsonify(output)


@app.route('/prediction')
def pridiction():
    return render_template('prediction.html')

@app.route('/pandas_profiling')
def pandas_profiling():
    return render_template('pandas_profiling.html')

@app.route('/scan_here')
def scan_here():
    return render_template('scan_here.html')

@app.route('/about')
def aboutus():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
