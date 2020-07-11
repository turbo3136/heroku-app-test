from app import app
from turbo_dash import turbo_dash

from config import LOGO_PATH, FOUROHFOUR_IMG_LINK


td = turbo_dash(
    app_to_callback=app,
    layout_template='404',
    turbo_header_logo_file_path=LOGO_PATH,
    turbo_header_links_list=[
        {'href': '/testing', 'text': 'Testing'},
        {'href': '/positives', 'text': 'Positives'},
        {'href': '/deaths', 'text': 'Deaths'},
        {'href': '/playground', 'text': 'Playground'},
    ],
    turbo_img_link=FOUROHFOUR_IMG_LINK,
)

layout = td.layout
td.callbacks
