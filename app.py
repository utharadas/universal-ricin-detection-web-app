from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model
pipeline = pickle.load(open('finalmodel3.pkl', 'rb'))

def process_data(data):
    # Extract data from the received JSON
    frequency = data['frequency']
    z = data['z']
    pa = data['pa']
    z_shift_back = data['z_shift_back']
    pa_shift_back = data['pa_shift_back']
    z_shift_forward = data['z_shift_forward']
    pa_shift_forward = data['pa_shift_forward']
    time = data['time']
    pH = data['pH']
    carbs = data['carbs']
    orp = data['orp']
    doppm = data['doppm']
    cond400h = data['cond400h']
    cond10kh = data['cond10kh']
    b = data['b']
    a = data['a']

    # Calculate additional features
    las5freq = z_shift_forward - z_shift_back
    last5z = (z + z_shift_back + z_shift_forward) / 3
    last5pa = (pa + pa_shift_back + pa_shift_forward) / 3
    last5zincrease = z_shift_forward - z_shift_back
    last5paincrease = pa_shift_forward - pa_shift_back
    z_slope = last5zincrease / las5freq
    pa_slope = last5paincrease / las5freq

    # Create DataFrame
    df = pd.DataFrame([{
        'Freq(Hz)': frequency,
        'Z(Ohm)': z,
        'PA': pa,
        'Time(m)': time,
        'Total carbohydrate': carbs,
        'pH': pH,
        'ORP': orp,
        'Conductivity (400H)': cond400h,
        'Conductivity (10kH)': cond10kh,
        'DO (ppm)': doppm,
        'a*': a,
        'b*': b,
        'Last5Z': last5z,
        'Last5increase': last5zincrease,
        'Last5freq': las5freq,
        'Last5slope': z_slope,
        'Last5increasePA': last5paincrease,
        'Last5PA': last5pa,
        'Last5slopePA': pa_slope
    }])
    
    return df

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = process_data(data)
    result = pipeline.predict(df)
    return jsonify({'result': 'ricin present' if result == 1 else 'no ricin'})

if __name__ == '__main__':
    app.run(debug=True)
