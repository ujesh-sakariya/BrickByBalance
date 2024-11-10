from prophet.serialize import model_from_json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Define the base path to the models directory
PATH = Path(__file__).resolve().parent.joinpath('Models')

# Correct the file paths
SEMI_PATH = PATH.joinpath("serialized_model_Semi_Detached_Average_Price.json")
DET_PATH = PATH.joinpath("serialized_model_Detached_Average_Price.json")
TERR_PATH = PATH.joinpath("serialized_model_Terraced_Average_Price.json")
FLAT_PATH = PATH.joinpath("serialized_model_Flat_Average_Price.json")

'''
Handles the prediction of a house price given a house type and time scale
'''
def predict(house_type: str, year_range: int,region_in:str = ''):
    '''Predicts the average value of a given house type at a given point in the future'''

    if house_type == "Semi":
        model_path = str(SEMI_PATH)
    elif house_type == "Det":
        model_path = str(DET_PATH)
    elif house_type == "Terr":
        model_path = str(TERR_PATH)
    elif house_type == "Flat":
        model_path = str(FLAT_PATH)
    else:
        print("Invalid house type specified.")
        return

    # Load the model
    with open(model_path, 'r') as fin:
        model = model_from_json(fin.read())

    # Generate a future date
    today = datetime.today()
    future_date = [pd.Timestamp(today.replace(year=today.year + year_range))]
    future_df = pd.DataFrame({'ds': future_date})

    # Add regressor values (these should be adjusted based on expectations)
    future_df['Interest'] = 2.0  # Replace with your expected value for Interest
    future_df['Inflation'] = 1.5  # Replace with your expected value for Inflation
    #handle region input
    regions = {'Wales':0, 
               'Inner London':0, 
               'Outer London':0, 
               'London':0, 
               'East of England':0, 
                'North West':0, 
                'South East':0, 
                'West Midlands Region':0, 
                'South West':0, 
                'East Midlands':0 ,
                'Yorkshire and The Humber':0,
                 'North East':0, 'Scotland':0}
    if region_in != '':
        try:
            regions[region_in] = 1
        except KeyError as e :
            raise e('ERROR BAD REGION')
    # add region regressors
    for region in regions:
        future_df[region] = regions[region]
    # Predict using the model
    forecast = model.predict(future_df)

    # Print the results
    print(f"Predicted price range for {future_date[0].date()}:")
    print(f"Median (yhat): {forecast['yhat'].iloc[0]:.2f}")
    print(f"Lower bound (yhat_lower): {forecast['yhat_lower'].iloc[0]:.2f}")
    print(f"Upper bound (yhat_upper): {forecast['yhat_upper'].iloc[0]:.2f}")

if __name__ == '__main__':
    predict('Semi', 10)
