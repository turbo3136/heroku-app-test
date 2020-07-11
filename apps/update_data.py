import pandas as pd
from turbo_dash import turbo_dash
from turbo_dash.inputs import TurboInput
from turbo_dash.outputs import TurboOutput

from app import app
from config import STATES_PATH, LOGO_PATH


df = pd.read_csv(STATES_PATH)
# print(df.columns.values)
# ['date', 'state', 'positive', 'negative', 'pending',
#        'hospitalizedCurrently', 'hospitalizedCumulative',
#        'inIcuCurrently', 'inIcuCumulative', 'onVentilatorCurrently',
#        'onVentilatorCumulative', 'recovered', 'hash', 'dateChecked',
#        'death', 'hospitalized', 'total', 'totalTestResults', 'posNeg',
#        'fips', 'deathIncrease', 'hospitalizedIncrease',
#        'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease',
#        'population', 'positive_test_rate', 'pct_of_population_tested',
#        'pct_of_population_positive', 'simple_death_rate',
#        'inferred_positive', 'hidden_positive',
#        'pct_of_population_inferred_positive',
#        'pct_of_population_hidden_positive']


list_of_inputs = [
    TurboInput(
        output_id_list=['totalTestResults-line', 'pct_of_population_tested-line', 'pct_of_population_tested-violin'],
        input_type='Dropdown',
        df=df,
        value_column='state',
        input_component_id='state-filter',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[dataframe['state'] == value]
        ],
        input_label_class_name='sidebar-label',
    ),
]

list_of_outputs = [

]

td = turbo_dash(
    app_to_callback=app,
    list_of_inputs=list_of_inputs,
    list_of_outputs=list_of_outputs,
    layout_template='turbo',
    turbo_header_logo_file_path=LOGO_PATH,
    turbo_header_links_list=[
        {'href': '/testing', 'text': 'Testing', 'link_class_name': 'header-link-current'},
        {'href': '/positives', 'text': 'Positives'},
        {'href': '/deaths', 'text': 'Deaths'},
    ],
)

layout = td.layout
td.callbacks
