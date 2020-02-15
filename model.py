def prediction_model(input_values):
    import pickle
    import joblib
    import pandas as pd
    from sklearn.linear_model import SGDClassifier
    from sklearn import linear_model

    # Create Datafram
    columns = ['Trip Seconds', 'Trip Miles', 'rain_1h', 'PCA_76', 'DCA_76', 'temp', 'November', 'PCA_56', 'snow_1h', 'DCA_56']
    user_input_df = pd.DataFrame(input_values, columns).transpose()

    # Load the model
    model = pickle.load( open( "improved_model.p", "rb" ) )
    my_scaler = joblib.load('scaler.pkl')

    # Scale User inputs
    inputs_scaled = my_scaler.transform(user_input_df)
    
    # Model the user inputs
    scaled_predict = model.predict(inputs_scaled)

    # format output - one item in a list
    fare = round(scaled_predict[0],2) + 2.50 + columns[2]*0.15

    return fare