from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

def get_covid_data():
    '''Download COVID-19 data from Kaggle '''

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files('josephassaker/covid19-global-dataset',
        path='data/', unzip=True) # COVID-19 cases dataset

    return pd.read_csv('data/worldometer_coronavirus_daily_data.csv')

def get_vaccines_data():
    ''' Download COVID-19 vaccinations data from Kaggle '''

    api = KaggleApi()
    api.authenticate()

    api.dataset_download_files('gpreda/covid-world-vaccination-progress',
        path='data/', unzip=True) # COVID-19 vaccinations dataset

    return pd.read_csv('data/country_vaccinations.csv')
