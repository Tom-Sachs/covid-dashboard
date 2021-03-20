import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from utils import *
from params_layout import *
from clean_data import clean_vaccines_data, clean_covid_data
from get_data import *

def plot_vaccinations_barh(ax, vaccines_data):
  ''' Plots horizontal barchart displaying number of vaccines administrated in
  top 20 countries '''

  # Adapting the x axis depending on the maximum value
  xticks_spaces = 20000000
  xlim = round(vaccines_data['daily_vaccinations'].max() + 2*xticks_spaces, -7)
  if xlim%xticks_spaces != 0:
    xlim = xlim - (xticks_spaces/2)

  ax.barh(vaccines_data['country'],
      vaccines_data['daily_vaccinations'],
      color=color_palette)
  ax.set_title('Number of Covid-19 vaccines administrated by country')
  ax.set_xlabel("Number of vaccines administrated (in millions)")
  ax.set_xlim(0,xlim)
  ax.grid(False)
  ticks = list(range(0,int(xlim/1000000 + 20), 20))
  ax.set_xticklabels(ticks)
  annotate_barh(ax) # Add labels to each horizontal bar

def plot_daily_covid_and_vaccines_line(ax,country_data):

  ax.set_title(f'COVID-19 in {country}')
  ax.set_ylabel('Number of persons')

  ax.plot(country_data.index,
    country_data['daily_new_cases'],
    c=END_COLOR,
    label='daily new cases')

  ax.plot(country_data.index,
    country_data['daily_vaccinations'],
    c=START_COLOR,
    label='daily new vaccinations')

def plot_weekly_covid_cases_bar(ax,weekly_covid_data):

  ax.bar(weekly_covid_data.index,
    weekly_covid_data['daily_new_cases'],
    width=5,
    alpha=0.3,
    color=END_COLOR,
    label='weekly contaminations')

def plot_graphs(country_data, weekly_covid_data, vaccines_data,
  country = 'France'):

  # Matplotlib Styles
  plt.style.use(STYLE)
  matplotlib.rc('font', **font)

  ## Initializing the subplots
  fig, axs = plt.subplots(nrows=2, ncols = 1, figsize=(8,12))

  ## First graph: Total number of vaccinations in top 20 countries
  plot_vaccinations_barh(axs[0],vaccines_data)

  ## Second graph: For a selected country, number of daily and weekly cases, and
  # daily new vaccinations.
  plot_daily_covid_and_vaccines_line(axs[1],country_data)
  plot_weekly_covid_cases_bar(axs[1],weekly_covid_data)

  ### Adding the legend and saving plot
  plt.legend()
  plt.savefig('covid_dashboard.png')



if __name__ == "__main__":

  try:
    country = sys.argv[1]
  except IndexError:
    country = 'France'

  ### Defining Color Palette
  color_palette = linear_gradient(START_COLOR,
    finish_hex=END_COLOR,
    n=20)['hex']

  ### Loading data
  covid_data = get_covid_data()
  vaccines_data = get_vaccines_data()

  ### Cleaning DataFrames
  country_data, weekly_covid_data = clean_covid_data(covid_data, vaccines_data, country)
  vaccines_data = clean_vaccines_data(vaccines_data)

  ### Plot graphs
  plot_graphs(country_data, weekly_covid_data, vaccines_data, country=country)
