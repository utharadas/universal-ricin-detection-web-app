import pandas as pd
import pickle

# Load the trained model - Chamge the name as per new versions
pipeline = pickle.load(open('finalmodel3.pkl', 'rb'))


# Methods to read data - do not change
def read_data():
    # Set frequencies at which you want to test the data. The default ones are below
    frequency = 25123
    frequency_shift_back = 19954
    frequency_shift_forward = 31634

    # Input data - run program
    z = float(input(f'Z at {frequency}:: '))
    pa = float(input(f'PA at {frequency}:: '))

    
    z_shift_back = float(input(f'Z at {frequency_shift_back}:: '))
    pa_shift_back = float(input(f'PA at {frequency_shift_back}:: '))

    
    z_shift_forward = float(input(f'Z at {frequency_shift_forward}:: '))
    pa_shift_forward = float(input(f'PA at {frequency_shift_forward}:: '))

    # Input other variables - run program

    time = int(input('Time (Works best at 10 minutes): '))

    pH = float(input('pH: '))
    carbs = float(input('carbs: '))
    orp = float(input('orp: '))
    doppm = float(input('do(ppm): '))
    cond400h = float(input('cond 400h: '))
    cond10kh = float(input('cond 10kh: '))
    b = float(input('b*: '))
    a = float(input('a*: '))

    # Calculate additional features
    las5freq = frequency_shift_forward - frequency_shift_back
    last5z = (z + z_shift_back + z_shift_forward) / 3
    last5pa = (pa + pa_shift_back + pa_shift_forward) / 3

    last5zincrease = z_shift_forward - z_shift_back
    last5paincrease = pa_shift_forward - pa_shift_back

    z_slope = last5zincrease / las5freq
    pa_slope = last5paincrease / las5freq

    # Create DataFrame with an explicit index
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

def read_csv(path):
    df = pd.read_csv(path)
    df_f = df.iloc[[0]]
    df_f['Last5Z'] = (df.iloc[2]['Z(Ohm)']+df.iloc[1]['Z(Ohm)']+df.iloc[0]['Z(Ohm)'])/3
    df_f['Last5increase']  = df.iloc[2]['Z(Ohm)']-df.iloc[1]['Z(Ohm)']
    df_f['Last5freq']  = df.iloc[2]['Freq(Hz)']-df.iloc[1]['Freq(Hz)']
    df_f['Last5slope'] = df_f['Last5increase']/df_f['Last5freq']

    df_f['Last5PA'] = (df.iloc[2]['PA']+df.iloc[1]['PA']+df.iloc[0]['PA'])/3
    df_f['Last5increasePA']  = df.iloc[2]['PA']-df.iloc[1]['PA']
    df_f['Last5slopePA'] = df_f['Last5increasePA']/df_f['Last5freq']
    return df_f

#If you want to test large amounts of data, write a new method to read a csv to test it
choice = int(input("Enter 1 if you want to enter information manually, enter 0 if you want to enter from a csv: "))
if (choice==0):
    path = input('Enter path name(ex. sample.csv): ')
    
df = read_data() if (choice ==1) else read_csv(path)

# Function to predict using the pipeline
def predict(df: pd.DataFrame):
    return pipeline.predict(df)

# Get prediction result
result = predict(df)

# Display prediction result
print("ricin present" if result == 1 else "no ricin")
