# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Process
            The initial idea was to do something with hot springs, as soaking in them is a favorite pastime of mine. I found a dataset with the locations of all thermal springs in the United States. But what to do with that data? I thought it might be interesting to see if the locations of hot springs could be predicted somehow using other data. After searching around a bit I decided on county demographic data from the U.S. census, which I found in a nice clean state at Kaggle.

            I created the alien invasion scenario because I wanted a better story for the project than just a fun experiment to see if I could predict the location of a geologic feature from societal factors like income, race, and employment. 

            Data wrangling

            The first issue was how to sync the hot springs data, which was in latitude/longitude, with the census data, which was by county. I found a python library (geopy) that can obtain the county name for a lat/long coordinate. I also eliminated all the springs that are too hot to soak in (this being what gives immunity to the aliens’ weapons). And I removed any springs in Alaska and Hawaii, assuming they would be cut off from the aliens. The resulting dataframe had column for latitude, longitude, maximum surface temperature, and county for 964 swimmable hot springs in the continental United States.

            For the census data, I also eliminated Alaska and Hawaii (and Puerto Rico), and using a dataset that had the county ID numbers along with their latitude and longitude (I believe these are the geographic centers - N/S, E/W mid-points - and not the population centers - points where population is evenly distributed NSEW - but I am not completely certain.) Because the census data also had county ID numbers, I was able to merge them on this column, which added the lat/long coordinates to the census data.

            This gave me my basic features. There were 34 columns in total to use in a model or for further feature engineering. All features were quantitive and none were categorical. 

            Target variable(s)

            The next task was to decide on a target. The most basic was whether or not a given county had a hot spring or not. For a numerical option, using the lat/long coordinates from the springs and census dataframes, I used a function to calculate the distance from a county center to the nearest hot spring. Finally, based on these distances, I created three distance categories for the location of the nearest hot spring (<20, 20-50, >50 miles). 

            Baseline prediction(s)

            For the first target (spring/no spring), merely picking the majority class resulted in an accuracy of 82%. For the second target (miles to closest spring), using a baseline prediction of 194.83 miles (mean closest spring), the mean absolute error (MAE) was 112.14 miles. for the third target (three distance categories), selecting the majority class resulted in an accuracy of 85%. 

            Linear regression model

            The first model I attempted was linear regression, using distance to the closest spring as the target variable. With minimal feature engineering (see below), the MAE of the regression model was 101.5 miles, which is better than the baseline prediction, but not by much. R-squared was relatively low at 0.19. 

            Select K best features barely improved the model’s predictive power, but it did show that roughly half the features could be dropped (k=17 was considered optimal). The features that remained included all the ones that would be included in the final model below. 

            Decision tree model

            For the decision tree I used the three distance categories (<20, 20-50, >50 miles). Because the target classes were imbalanced, the first step was to upsample the data to create a dataset with balanced classes. Because there were no categorical variables, the pipeline only included StandardScaler and DecisionTreeClassifier. The first model with no parameter tuning (except max_depth) had a very high accuracy of 94%, with high precision and recall across the board. When this model was to predict the original data (not upsampled), it told a different story. While the majority class (>50 miles) still had high precision and recall, precision for the minority classes were relatively poor at 60-65% (recall was very high for both). 

            The next step was feature permutation. After playing around with different levels of minimum importance, I decided to keep only the top five features (Hispanic, Drive, MeanCommute, Black, PublicWork). This was for two reasons: (1) the model’s accuracy did not improve much with more features, and (2) so the users (“resistance forces”) actually using the tool didn’t have to enter too many variables. Next was a randomized parameter search, the results of which I incorporated but did not change much. 

            After some trial and error, I decided that training the model on non-upsampled data (i.e., imbalanced classes) was better. Doing this resulted in worse accuracy overall (around 75%), but precision for the minority classes was much better (80-85%). Recall was worse with this method, dropping to about the same as precision. Given the imprecise nature of the predictions, which means that even with a true positive, resistance forces would still need to find the relevant spring within a fairly large area, the time wasted searching for a nonexistent spring with a false positive was considered more costly than missing an actual spring with a false negative. Precision and recall for the majority class remained very high. 

            The worst case scenario would be sending resistance forces on a wild goose chase by predicting a spring is nearby when none in fact are even close. This model only gives such bad predictions in about 2% of counties. 

            Feature engineering

            Due to time constraints, I did not experiment much with feature engineering. Given that population levels of two minority groups ranked high in the feature permutation exercise, I created a variable for the total non-white population. This had higher than average importance in the permutation exercise, but not not high enough to be adopted for the final model. Other possibilities for feature engineering are discussed on the Insights page.

            Data

            Thermal springs: https://www.ngdc.noaa.gov/hazard/geotherm.shtml

            County lat/lon: https://en.wikipedia.org/wiki/User:Michael_J/County_table
            
            Census: https://www.kaggle.com/muonneutrino/us-census-demographic-data?select=acs2017_county_data.csv

            """
        ),

    ],
)

layout = dbc.Row([column1])