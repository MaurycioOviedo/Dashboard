import dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, dcc, Output, Input
from dash_extensions.javascript import assign
import dash_bootstrap_components as dbc
import plotly.express as px



# Cool, dark tiles by Stadia Maps.
url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '



# Rotated custom marker.
iconUrl = "https://www.pngplay.com/wp-content/uploads/13/Bird-Silhouette-No-Background.png"
marker = dict(rotate=True, markerOptions=dict(icon=dict(iconUrl=iconUrl, iconAnchor=[16, 16], weight=0.005)))
patterns = [dict(repeat='10', dash=dict(pixelSize=5, pathOptions=dict(color='#000', weight=1, opacity=0.2))),
            dict(offset='16%', repeat='33%', marker=marker)]
rotated_markers = dl.PolylineDecorator(positions=[[42.9, -15], [44.18, -11.4], [45.77, -8.0], [47.61, -6.4],
                                                  [49.41, -6.1], [51.01, -7.2]], patterns=patterns)




# A few cities in Denmark.
cities = [dict(name="Pássaro", lat=29.006360, lon=-81.144778),
          dict(name="Pássaro", lat=29.016360, lon=-81.144778),
          dict(name="Pássaro", lat=29.026360, lon=-81.144778),
          #
          #dict(name="Aarhus", lat=56.1780842, lon=10.1119354),
          #dict(name="Copenhagen", lat=55.6712474, lon=12.5237848)
          ]
# Create drop down options.

dd_options = [dict(value=c["name"], label=c["name"]) for c in cities]
dd_defaults = [o["value"] for o in dd_options]

# Generate geojson with a marker for each city and name as tooltip.
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in cities])
# Create javascript function that filters on feature name.
geojson_filter = assign("function(feature, context){return context.props.hideout.includes(feature.properties.name);}")
# Create example app.

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP,'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css' ], prevent_initial_callbacks=True )
server = app.server
df = px.data.gapminder()

app.layout = html.Div([

    dbc.Row([
        dbc.Col([
            html.H1(['Monitoramento de passaros '],
                    style={'color': '#7fafdf',
                           'background-size': '100%',
                           'font-family': 'playfair display,sans-serif'}),
            html.H6([' Sistema de detecção de animais silvestre em regiões de perigo para os aeroportos'],
                    style={'border-left': '#2cfec1 solid 1rem',
                           'color': '#7fafdf',
                           'padding-left': '1rem',
                           'max-width': '150rem',
                           'margin': '2rem 0 3rem'})
        ], width='auto')
    ]),

    dbc.Row([
        dbc.Col([
            html.Label('Aeroportos', style={'color': '#7fafdf'}),
            dcc.RadioItems(options=['New York City', 'Montréal', 'San Francisco'],style={'color': '#7fafdf'},
                           value='Montréal'),
        ], width=4, style={"margin-top": "10px",
                           "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 30), 0 4px 20px 0 rgba(0, 0, 0, 30)",
                           "color": "#0000FF",
                           'margin-bottom': '30px'}),
        dbc.Col([
            html.Label('Anos', style={'color': '#7fafdf'}),
            dcc.Dropdown(options=[x for x in df.year.unique()],
                         style={'color': '#7fafdf'},
                         value=df.year[2]),
        ], width=4, style={"margin-top": "10px",
                           "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 30), 0 4px 20px 0 rgba(0, 0, 0, 30)",
                           "color": "#0000FF",
                           'margin-bottom': '30px',
                           'margin-left': '10px',
                           'padding':'12px'})
    ]),

    dbc.Row([
        dbc.Col([
            html.Label('Escolha o Animal:',
                       style={'color': '#7fafdf'}),
            html.Br(),
            dcc.Input(value='Passaro', type='text'),
        ], width=4, style={"margin-top": "10px",
                           "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 30), 0 4px 20px 0 rgba(0, 0, 0, 30)",
                           "color": "#0000FF",
                           'margin-bottom': '30px'}),
        dbc.Col([
            html.Label('Meses',
                       style={'color': '#7fafdf'}),
            dcc.Slider(min=1, max=12, step=1, value=6),
        ], width=4, style={"margin-top": "10px",
                           "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 30), 0 4px 20px 0 rgba(0, 0, 0, 30)",
                            "color": "#0000FF",
                           'margin-bottom': '30px',
                           'margin-left': '10px',
                           'padding':'12px'})
    ]),

    dbc.Row([
         dl.Map(children=[
             dl.TileLayer(maxZoom=15),
             dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}),
             dl.GeoJSON(data=geojson, options=dict(filter=geojson_filter), hideout=dd_defaults, id="geojson", zoomToBounds=True),
             rotated_markers

        ], style={'width': '100%', 'height': '700px'}, id="map"),
    ], style={'padding': '10px 10px'}),

],style={'background-color': '#1f2630',
         'font-family': 'open sans,helveticaneue,helvetica neue,Helvetica,Arial,sans-serif',
         'line-height': '1.8',
         'width': '100%',
         'height': '100%',
         'padding': '40px 40px 40px 40px'})

# Link drop down to geojson hideout prop (could be done with a normal callback, but clientside is more performant).
app.clientside_callback("function(x){return x;}", Output("geojson", "hideout"), Input("dd", "value"))

if __name__ == '__main__':
    app.run_server(debug=True)