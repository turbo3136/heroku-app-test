import requests
import pandas as pd

from config import STATES_PATH, STATES_INFO_PATH


def get_df_from_json_api_request(url):
    response = requests.get(url)  # use the request library to grab the data

    # let the user know the response
    print(
        'API Response Code: {}, {}'.format(response.status_code, requests.status_codes._codes[response.status_code][0])
    )

    return pd.DataFrame(response.json())  # grab the json from the response and convert to dataframe


def clean_df_states_historical_data(df):
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')  # convert the date column to a datetime object
    df['dateChecked'] = pd.to_datetime(df['dateChecked'])  # convert the dateChecked column to a datetime object

    return df


def process_data():
    assumed_death_rate = 0.01

    # grab population
    df_population_temp = pd.read_csv('http://www2.census.gov/programs-surveys/popest/datasets/2010-2019/national/totals/nst-est2019-alldata.csv?#')
    # df_population_temp.head()

    # grab fips lookup
    df_fips = pd.read_csv('https://gist.githubusercontent.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53/raw/11d15233327c8080c9646c7e1f23052659db251d/us-state-ansi-fips.csv')
    # df_fips.head()

    # join to fips to grab the state abbreviation
    df_population = df_population_temp.merge(df_fips, left_on='STATE', right_on=' st')
    df_population = df_population[[' stusps', 'POPESTIMATE2019']].rename(columns={' stusps': 'state', 'POPESTIMATE2019': 'population'})
    df_population['state'] = df_population['state'].str.strip()
    # df_population.head()
    # df_population.columns.values

    url_states_historical_data = 'https://covidtracking.com/api/states/daily'  # historical data by state and date, not including the current date
    url_states_info = 'https://covidtracking.com/api/states/info'  # info about state data
    url_states_current_values = 'https://covidtracking.com/api/states'  # current data for each state

    # grab the states historical
    df_states_historical_data = get_df_from_json_api_request(url_states_historical_data)
    df_states_historical_data = clean_df_states_historical_data(df_states_historical_data)
    # df_states_historical_data.head()

    # add columns with interesting info
    df_states = df_states_historical_data.merge(df_population, on='state')

    # now sort the data and reindex so we have it in order for rolling calcs
    df_states = df_states.sort_values(['state', 'date']).reset_index(drop=True)

    # add a bunch of calcs
    df_states['positive_test_rate'] = df_states['positive'] / df_states['totalTestResults']
    df_states['pct_of_population_tested'] = df_states['totalTestResults'] / df_states['population']
    df_states['pct_of_population_positive'] = df_states['positive'] / df_states['population']
    df_states['simple_death_rate'] = df_states['death'] / df_states['positive']
    df_states['inferred_positive'] = df_states['death'] / assumed_death_rate
    df_states['hidden_positive'] = df_states['inferred_positive'] - df_states['positive']
    df_states['pct_of_population_inferred_positive'] = df_states['inferred_positive'] / df_states['population']
    df_states['pct_of_population_hidden_positive'] = df_states['hidden_positive'] / df_states['population']
    df_states['positive_test_rate_today'] = df_states['positiveIncrease'] / df_states['totalTestResultsIncrease']
    # rolling averages
    df_states['positiveIncrease_last_7'] = df_states.groupby('state')['positiveIncrease'].rolling(7).sum().reset_index(drop=True)
    df_states['totalTestResultsIncrease_last_7'] = df_states.groupby('state')['totalTestResultsIncrease'].rolling(7).sum().reset_index(drop=True)
    df_states['positive_test_rate_7_day_avg'] = df_states['positiveIncrease_last_7'] / df_states['totalTestResultsIncrease_last_7']
    df_states['pct_of_population_hospitalized'] = df_states['hospitalizedCurrently'] / df_states['population']

    # df_states.head()

    # grab the states info
    df_states_info = get_df_from_json_api_request(url_states_info)
    # df_states_info.head()

    # save the data
    df_states.to_csv(STATES_PATH, index=False)
    df_states_info.to_csv(STATES_INFO_PATH, index=False)

    return True


if __name__ == '__main__':
    process_data()
