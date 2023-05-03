import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css', "https://fonts.googleapis.com/css2?family=Yeseva+One&family=Bruno+Ace+SC&Barlow+Condensed:wght@500&display=swap"], external_scripts=['assets/main.js'])


server = app.server
app.config.suppress_callback_exceptions = True