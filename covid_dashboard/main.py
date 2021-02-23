import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from kaggle.api.kaggle_api_extended import KaggleApi
from utils import *
from params_layout import *
from data_cleaning import clean_vaccines_data, clean_covid_data

country = sys.argv[1]
### Download most recent data from Kaggle
api = KaggleApi()
api.authenticate()

api.dataset_download_files('josephassaker/covid19-global-dataset',
    path='data/', unzip=True) # COVID-19 cases dataset

api.dataset_download_files('gpreda/covid-world-vaccination-progress',
    path='data/', unzip=True) # COVID-19 vaccinations dataset

### Cleaning DataFrames
vaccines_dataset = clean_vaccines_data()
country_data, weekly_covid_data = clean_covid_data(country)

# Define color_palette defined in params_layout
color_palette = linear_gradient(START_COLOR,
    finish_hex=END_COLOR,
    n=20)['hex']

plt.style.use(STYLE)

# Setting font defined in params_layout
matplotlib.rc('font', **font)

## Initializing the subplots
fig, axs = plt.subplots(nrows=2, ncols = 1, figsize=(8,12))
axs[0].barh(vaccines_dataset['country'],
    vaccines_dataset['daily_vaccinations'],
    color=color_palette)

## First graph: Total number of vaccinations in top 20 countries
axs[0].set_title('Number of Covid-19 vaccins administrated by country')
axs[0].set_xlabel("Number of vaccines administrated (in millions)")
axs[0].set_xlim(0,100000000)
axs[0].grid(False)
ticks = [0, 20, 40, 60, 80, 100]
axs[0].set_xticklabels(ticks)
annotate_barh(axs[0]) # Add labels to each horizontal bar

## Second graph: For a selected country, number of daily and weekly cases, and
# daily new vaccinations.
axs[1].set_title(f'COVID-19 in {country}')
axs[1].set_ylabel('Number of persons')
axs[1].plot(country_data.index,
            country_data['daily_new_cases'],
            c=END_COLOR,
            label='daily new cases')

axs[1].plot(country_data.index,
            country_data['daily_vaccinations'],
            c=START_COLOR,
            label='daily new vaccinations')

axs[1].bar(weekly_covid_data.index,
           weekly_covid_data['daily_new_cases'],
           width=5,
           alpha=0.3,
           color=END_COLOR,
           label='weekly contaminations')

### Adding the legend
plt.legend()
plt.savefig('covid_dashboard.png')
