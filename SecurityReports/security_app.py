import dash_core_components as dcc
import plotly.graph_objs as go
import dash
import dash_html_components as html
import pandas as pd
import json
from apicalls import report_class
from graphdescriptions import graph_descriptions

app = dash.Dash(__name__)
report_maker = report_class.scrutinizer_reports()
print("Gathering Data for Security Report")
dns_graph = report_maker.dns_graph()
print("25% Complete")
source_hosts = report_maker.source_hosts()
print("50% Complete")
smb_hosts = report_maker.smb_hosts()
print("75% Complete")
host_count = report_maker.host_count()
print("100% Complete")

# report_maker = 'placeholder'
# source_hosts = 'placeholder'
# dns_graph = 'placeholder'
# smb_hosts = 'placeholder'
# host_count = 'placeholder'
dns_description = graph_descriptions.dns_description
source_description = graph_descriptions.sources_description
smb_description = graph_descriptions.smb_description
host_count_description = graph_descriptions.host_count_description

nav_menu = html.Div([

        dcc.Location(id='url', refresh=False),
        html.Ul([
                html.Li([
                        dcc.Link('Home', href='/')
                        ]),
                html.Li([
                        dcc.Link('DNS Report', href='/page-2')
                        ]),
                html.Li([
                        dcc.Link('Sources to Unique Destinations',href='/page-3')
                        ]),
                html.Li([
                        dcc.Link('SMB Traffic',href='/page-4')
                        ]),
                html.Li([
                        dcc.Link('Host Per Application',href='/page-5')
                        ]),
                ], className='nav navbar-nav'),
        
    ], className='navbar navbar-default navbar-static-top')

sample_div = html.Div('hello', id='the-text')
app.layout = html.Div([
    nav_menu,
    html.Div(id='page-content')

]

    )



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/':
        return html.Div([
            html.H3('Welcome to your Scrutinizer Security Report')
        ])
        print('hey your on the root')
    elif pathname =='/page-2':
        return html.Div(
            [html.Div([dns_graph]),
            html.Div(
                [html.H2('DNS Report'), 
                html.Div([html.P(dns_description)])], style = {'marginLeft':25})])
    elif pathname == '/page-3':
        return html.Div(
            [html.Div([source_hosts]),
            html.Div(
                [html.H2('Most Unique Connections'), 
                html.Div([html.P(source_description)])], style = {'marginLeft':25})])
    elif pathname == '/page-4':
        return html.Div(
            [html.Div([smb_hosts]),
            html.Div(
                [html.H2('SMB Top Producers'), 
                html.Div([html.P(smb_description)])], style = {'marginLeft':25})])
    elif pathname == '/page-5':
        return  html.Div(
            [html.Div([host_count]),
            html.Div(
                [html.H2('Number of Hosts per Application'), 
                html.Div([html.P(host_count_description)])], style = {'marginLeft':25})])    
    else:
        return html.Div([
            html.H3('Welcome to your Scrutinizer Security Report')
        ])        
    
app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})

if __name__ == '__main__':
    app.run_server(use_reloader=False)