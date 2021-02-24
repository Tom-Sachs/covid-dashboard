import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from utils import get_date_six_months_ago

standardized_country_names = {'United Arab Emirates': 'UAE',
        'United Kingdom':'UK',
        'United States':'USA'}

def clean_vaccines_data():

    # Load dataset
    vaccines_dataset = pd.read_csv('data/country_vaccinations.csv')

    # Standardize country names
    vaccines_dataset['country'].replace(standardized_country_names,inplace=True)

    # Keep relevant columns and convert date to datetime object
    daily_vac = vaccines_dataset[['country','date','daily_vaccinations','vaccines']]
    daily_vac.loc[:,'date'] = pd.to_datetime(daily_vac['date'])

    # Group by country
    daily_vac_country = daily_vac.groupby(
        ['country','vaccines']).sum().sort_values('daily_vaccinations',
        ascending=False)

    # Keep only the top 20 countries
    daily_vac_country = daily_vac_country.head(20)
    daily_vac_country.reset_index(inplace=True)
    daily_vac_country.sort_values('daily_vaccinations',
        ascending=True,
        inplace=True)

    return daily_vac_country


def clean_covid_data(country):
    ''' Returns two DataFrames :

    - country_data: With daily new COVID-19 cases, daily new COVID-19 vaccinations for a
    selected country and for the last 6 months.

    - weekly_covid_data: With weekly new COVID-19 cases for a selected country and
    for the last 6 months.
    '''

    # Define variable six_months_ago, to keep data from last 6 months only
    six_months_ago = get_date_six_months_ago()

    # Load data
    covid_data = pd.read_csv('data/worldometer_coronavirus_daily_data.csv')
    vaccines_dataset = pd.read_csv('data/country_vaccinations.csv')

    # Standardize country names
    covid_data['country'].replace(standardized_country_names,inplace=True)
    vaccines_dataset['country'].replace(standardized_country_names,inplace=True)

    # CLean covid_data
    covid_data.loc[:,'date'] = pd.to_datetime(covid_data['date']) # Convert date to datetime
    country_data = covid_data[covid_data['country']==country] # Select Country Data
    country_data = country_data[['date','country',
    'daily_new_cases','daily_new_deaths']] # Keep only relevant columns
    country_data = country_data[country_data['date']>str(six_months_ago)] # Filter date to keep last 6 months only
    country_data.set_index('date', inplace=True)

    # Join with vaccines_dataset
    daily_vac = vaccines_dataset[['country','date','daily_vaccinations','vaccines']]
    daily_vac.loc[:,'date'] = pd.to_datetime(daily_vac['date'])
    vaccination_data = daily_vac[daily_vac['country']==country].set_index('date')[['daily_vaccinations']]

    # Filling missing values by 0 only at the beginning of the period.
    # For the most recent data, we want to keep NaNs to prevent the daily
    # vaccination plot from dropping to 0.
    country_data = country_data.join(vaccination_data).fillna(0)
    condition = (country_data.index>='2021-02-17') & (country_data.daily_vaccinations==0)
    country_data.loc[condition,'daily_vaccinations'] = 'NaN'

    # Weekly_cases
    covid_data = pd.read_csv('data/worldometer_coronavirus_daily_data.csv')
    covid_data.loc[:,'date'] = pd.to_datetime(covid_data['date']) - pd.to_timedelta(7,unit='d')
    weekly_covid_data = covid_data[covid_data['date'] > str(six_months_ago)]
    weekly_covid_data = weekly_covid_data[weekly_covid_data['country']==country].groupby(pd.Grouper(key='date', freq='W-MON')).mean()

    return country_data, weekly_covid_data


