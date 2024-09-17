import argparse
import csv

LOG_FILE='util-cli.log'
LOG_CATEGORY="UTILS_CLI"

# Utility functions shared acrossed

def write_log(category:str,message:str,log_file:str=LOG_FILE)->None:
    with open(log_file,'a') as f:
        print("{}: {}".format(category,message),file=f, end='\n')

def write_csv_data(csv_file_path,data):
    with open(csv_file_path,'a') as f:
        csv_h=csv.writer(f)
        csv_h.writerows(data)

def open_browser(url:str=None,search:str=None)->None:
    import webbrowser
    if url!=None and search==None:
        webbrowser.open_new_tab(url)
    elif url==None and search!=None:
        # Will loop through the JSON and open all search terms
        # webbrowser.open_new_tab(url)
        print("TODO.....")
    else:
        message="Can't open a new tab, neither URL nor search term provided"
        print(message)
        write_log(category=LOG_CATEGORY,message=message)

def rest_client(url,request_body,method,iterations):
    pass
