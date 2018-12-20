import requests
import requests.packages.urllib3
import json
import pandas as pd
import sys


requests.packages.urllib3.disable_warnings()

#api call is a classe that will be used to create the various API calls to Scrutinizer. Running the Make_call function stores the data in self.resp
#that data can be viewed as is, or you can run the make_graph functions to create the pandas object for graphing. 
#this returned data is later used in report_class.py to make the reports for plotly. 
sys.path.append('..')
with open('settings.json') as json_data_file:
    config = json.load(json_data_file)

print(config)
class api_call:
    def __init__(self, verify=False,):

        hostname = config['scrutinizer_ip']
        authToken = config['api_key']

        if hostname == "Scrutinizer Hostname or IP Here":
            raise ValueError("You need to put in Scrutinizer host IP in settings.json")
        if authToken == "API KEY HERE":
            raise ValueError("You need an authentication token in settings.json")
            
        self.url = "https://{}/fcgi/scrut_fcgi.fcgi".format(hostname)
        self.verify = verify
        self.authToken = authToken
    def make_call(
                    self, 
                    report_type = "host2host",
                    filters = {"sdfDips_0": "in_GROUP_ALL"}
                  ):
        self.rpt_json = {
                "reportTypeLang":report_type,
                "reportDirections": {"selected": "inbound"},
                "dataGranularity": {"selected": 1},
                "orderBy": "countdistinct_destinationipaddress",
                "times": {"dateRange": "LastTenMinutes"},
                "filters": filters,
                "rateTotal": {"selected": "total"},
                "dataFormat": {"selected": "raw"},
                "bbp": {"selected" : "bytes"}     
        }

        self.data_requested = {
                "inbound": { 
                   "table": { 
                     "query_limit": {"offset": 0, "max_num_rows": 10}
                   }
                }
               }

        self.params = {
                "rm": "report_api",
                "action": "get",
                 "rpt_json": json.dumps(self.rpt_json),
                "data_requested": json.dumps(self.data_requested),
                "authToken":self.authToken
             }
        self.resp = requests.get(self.url, params=self.params, verify=self.verify)
        
    def make_graph(self): #method creats a pandas object, only tested for source host flows report. May need new methods for different report types later
        df = pd.read_json(json.dumps(self.resp.json()))['report']['table']['inbound']['rows'] #creates dataframe in pandas. 
        scrut_df = pd.DataFrame({
                    'Source_IP':[ip[1]['label'] for ip in df ], 
                    'Unique_Dests':pd.to_numeric([ip[4]['label'] for ip in df ], errors='coerce'),#converts to int64 for graphing(default is object)
                    'Traffic': pd.to_numeric([ip[5]['label'] for ip in df ], errors='coerce')}, index=[num for num in range(len(df))])
        

        return scrut_df

    def make_graph_host_count(self):
        df = pd.read_json(json.dumps(self.resp.json()))['report']['table']['inbound']['rows']
        scrut_df = pd.DataFrame({
                    'Application':[ip[1]['label'] for ip in df ], 
                    'Unique_Sources':pd.to_numeric([ip[4]['label'] for ip in df ], errors='coerce')#converts to int64 for graphing(default is object)
                    }, index=[num for num in range(len(df))])
        

        return scrut_df
        
        

