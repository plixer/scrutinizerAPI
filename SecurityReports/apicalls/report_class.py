import sys
sys.path.append("..")
from scrutapi import scrut_api_class
import pandas as pd
import dash_core_components as dcc
import plotly.graph_objs as go

#this class is used in order to create the graph objects that are served up by plotly. 
#in the API call you can pass in the filters you want in order to get data back. 
#keep in mind, if you want to use the make_graph() method, you may need to create a customer one
#depending on the report type you chose. 

class scrutinizer_reports:
    def __init__(self):
        self.scrut_api = scrut_api_class.api_call()     
    def dns_graph(self):
        self.scrut_api.make_call(report_type='srcHostFlows', filters = {
            "sdfDips_0": "in_GROUP_ALL",
            "sdfPorts_0":"in_53-17"
        }) #set filters and report type
        dns_data_df = self.scrut_api.make_graph() #converts returned data to a pandas object
        dns_graph = dcc.Graph(id='scatterplot', #creates plotly graph
                        figure = {
                        'data':[
                            go.Scatter(x=dns_data_df['Traffic'],
                                y=dns_data_df['Unique_Dests'],
                                text=dns_data_df['Source_IP'],
                                mode='markers',
                                marker=dict(
                                    size=dns_data_df['Traffic']/1000,
                                    color=dns_data_df['Unique_Dests'],
                                    
                                    
                                )
                            )],
                                    'layout':go.Layout(title='DNS Top Hosts',
                                                      xaxis={'title':'Number of Connections'},
                                                      yaxis={'title': 'Number of Unique Destinations' })
                                } 
                                )
        return dns_graph
    def source_hosts(self):
        self.scrut_api.make_call(report_type='srcHostFlows')
        source_data_df = self.scrut_api.make_graph()
        source_graph = dcc.Graph(id='scatterplot',
                        figure = {
                        'data':[
                            go.Scatter(x=source_data_df['Source_IP'],
                                y=source_data_df['Unique_Dests'],
 
                                mode='markers',
                                marker=dict(
                                    size=source_data_df['Traffic']/1000,
                                    color=source_data_df['Unique_Dests'],
                                    
                                    
                                ))],
                                    'layout':go.Layout(title='Sources to Number of Destinations')
                                } 
                                )
        return source_graph

    def smb_hosts(self):
        self.scrut_api.make_call(report_type='srcHostFlows', filters ={
            "sdfDips_0" :"in_GROUP_ALL",
            "sdfPorts_0":"in_445-6"
        })
        smb_data_df =  self.scrut_api.make_graph()
        
        smb_graph = dcc.Graph(id='scatterplot',
                            figure = {
                            'data':[
                                go.Bar(x=smb_data_df['Source_IP'],
                                    y=smb_data_df['Unique_Dests'],
                                    marker = dict(
                                        color=smb_data_df['Traffic']
                                    )
                                )],
                                        'layout':go.Layout(title='Top Hosts using SMB')
                                    } 
                                    )
        return smb_graph

    def host_count(self):
        self.scrut_api.make_call(report_type='custom_ApplicationSourceCount', filters ={
            "sdfDips_0" :"in_GROUP_ALL",
            "sdfPorts_0":"in_445-6",
            "sdfPorts_1": "in_53-17",
            "sdfPorts_2": "in_22-6",
            "sdfPorts_3": "in_20-6",
            "sdfPorts_4": "in_25-6"
        })
        host_count_data =  self.scrut_api.make_graph_host_count()
        host_graph = dcc.Graph(id='scatterplot',
                            figure = {
                            'data':[
                                go.Bar(x=host_count_data['Application'],
                                    y=host_count_data['Unique_Sources'],
                                    marker = dict(
                                        color=host_count_data['Unique_Sources']
                                    )
                                )],
                                        'layout':go.Layout(title='Number of Sources Using Applications')
                                    } 
                                    )
        return host_graph        