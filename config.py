import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data/')

STATES_FILENAME = 'states.csv'
STATES_INFO_FILENAME = 'states_info.csv'

STATES_PATH = os.path.join(DATA_DIR, STATES_FILENAME)
STATES_INFO_PATH = os.path.join(DATA_DIR, STATES_INFO_FILENAME)

LOGO_PATH = '/static/covid.jpeg'
HOMEPAGE_IMG_LINK = '/static/xkcd_covid_charts.png'
FOUROHFOUR_IMG_LINK = '/static/xkcd_fourohfour.png'
