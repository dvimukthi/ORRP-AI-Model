# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from datetime import datetime

import joblib

# Load dataset into a pandas DataFrame
class BestRoomRatePredictorModelCreator:

    # default constructor
    def __init__(self):
        self.model = None

    
    def setup(self, file_name, file_to_save):
        self.model = None
        self.df = self.load_data(file_name)
        self.clean_data()
        self.creat_model()
        self.save_model(file_to_save)

    # load data from given file_name
    def load_data(self, file_name):
        try:
            df = pd.read_csv(file_name)
            return df
        except Exception as e:
            print(e)
        return None

    def clean_data(self):
        #Convert text Date to pythin datetime object
        self.df["date_col"] = pd.to_datetime(self.df["Date"], format="%d/%m/%Y")

        # we need to get the day of the week and month 
        self.df["month"] = self.df["date_col"].dt.month
        self.df["day_of_week"] = self.df["date_col"].dt.dayofweek

        # drop unwanted fields
        self.df = self.df.drop(
            [
                "Id",
                "Date",
                "date_col",
                "NumberOfBookings",
                "DailyRevenue",
                "RoomType",
                "RoomCategory",
                "EventName",
                "EventType",
                "Demography",
                "EventShowtime",
                "EventLocation",
                "HotelName",
                "HotelLocation",
                "Facilities",
            ],
            axis=1,
        )

        self.df.fillna(0, inplace=True)
        print(self.df.head(5))

    # Create model
    def creat_model(self):
        # Define the independent and dependent variables
        X = self.df.drop(["RoomPrice"], axis=1)
        y = self.df["RoomPrice"]

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a linear regression model on the training set
        model = LinearRegression()
        model.fit(X_train, y_train)
        # Make predictions on the testing set
        y_pred = model.predict(X_test)
        # Evaluate the model's performance on the testing set using mean squared error
        mse = mean_squared_error(y_test, y_pred)
        score = model.score(X_test,y_test)
        print("Mean Squared Error:", mse)
        print("Score:", score)
        if score > 0.75 :
            self.model = model
        else:
            raise Exception("Model score lower than minimum expectation. Please check data")

    # Save the model to be used in the future
    def save_model(self, file_name):
        if file_name is not None:
            joblib.dump(self.model, file_name)
            
    # Retrieve the model use in any application
    def get_model(self, file_name=None):
        if file_name is not None:
            self.model = joblib.load(file_name)

        return self.model
             


def predict_and_test_model(model):
    # Predict the room rate for a specific event
    # by sending all the room types with event detailsto the model to see the price for each room type
    new_data = [
        {
            "RoomTypeCode": "1",
            "NumberOfOccupents": "2",
            "RoomCategoryCode": "2",
            "EventTypeCode": "3",
            "DemographyCode": "2",
            "ShowTimeCode": "3",
            "EventLocationcode": "2",
            "month": "05",
            "day_of_week": "1",
            "RoomType":"Superior Twin Room",
            "EventType":"Musical Show",
        },
        {
            "RoomTypeCode": "2",
            "NumberOfOccupents": "1",
            "RoomCategoryCode": "1",
            "EventTypeCode": "3",
            "DemographyCode": "2",
            "ShowTimeCode": "3",
            "EventLocationcode": "2",
            "month": "05",
            "day_of_week": "1",
            "RoomType":"Superior King Room",
            "EventType":"Musical Show",
        },
        {
            "RoomTypeCode": "3",
            "NumberOfOccupents": "4",
            "RoomCategoryCode": "3",
            "EventTypeCode": "3",
            "DemographyCode": "2",
            "ShowTimeCode": "3",
            "EventLocationcode": "2",
            "month": "05",
            "day_of_week": "1",
            "RoomType":"Premium Double Room",
            "EventType":"Musical Show",
        },
        {
            "RoomTypeCode": "4",
            "NumberOfOccupents": "5",
            "RoomCategoryCode": "5",
            "EventTypeCode": "3",
            "DemographyCode": "2",
            "ShowTimeCode": "3",
            "EventLocationcode": "2",
            "month": "05",
            "day_of_week": "1",
            "RoomType":"Executive Room",
            "EventType":"Musical Show",
        },
        {
            "RoomTypeCode": "5",
            "NumberOfOccupents": "6",
            "RoomCategoryCode": "4",
            "EventTypeCode": "3",
            "DemographyCode": "2",
            "ShowTimeCode": "3",
            "EventLocationcode": "2",
            "month": "05",
            "day_of_week": "1",
            "RoomType":"Cilantro Suite",
            "EventType":"Musical Show",
        },
    ]

    for room in new_data:
        df = pd.DataFrame([room])

        # Prepare the input to match the data used to fit model
        df_new = df.drop(["RoomType", "EventType"], axis=1)
        
        # predict rates for given room type for event details
        room_rate = model.predict(df_new)

        print(
            "Predicted room {} rate for the event {} : {}".format(
                room["RoomType"], room["EventType"], str(round(room_rate[0],2))
            )
        )


if __name__ == "__main__":
    cvs_name = "./Hotel_Dataset.csv"
    model_file_name = "./best_room_rate_predictor.joblib"
    predictor = BestRoomRatePredictorModelCreator()
    # predictor.setup(cvs_name, model_file_name)
    model = predictor.get_model(file_name=model_file_name)
    predict_and_test_model(model)
