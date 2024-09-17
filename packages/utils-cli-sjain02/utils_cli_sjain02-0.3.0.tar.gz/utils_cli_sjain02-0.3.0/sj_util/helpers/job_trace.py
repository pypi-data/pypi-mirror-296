import xml.etree.ElementTree as ET
import csv
import os
import sys
from sj_util.helpers.utils import write_csv_data
# XPATH
root_xpath="INFO"
job_xpath='job'
persistence_xpath='persistence'
statement_xpath='statement'
execute_xpath='execute'

# def write_csv_data(csv_file_path,data):
#     with open(csv_file_path,'a') as f:
#         csv_h=csv.writer(f)
#         csv_h.writerows(data)
def parse_job_sql_trace(trace_file_path:str,job_name:str):
    if not os.path.exists(trace_file_path):
        print("The file {} path doesn't not exist".format(trace_file_path))
        sys.exit(-1)
    trace_file_name=os.path.basename(trace_file_path)
    if not trace_file_name.endswith('.xml'):
        print("The file {} doesn't have .xml extension".format(trace_file_name))
        sys.exit(-1)
    out_file=trace_file_name.split('.')[0]+'.csv'
    doc=ET.parse(trace_file_path)
    header=['Date','User','Session','Thread','Category','JobId','StatementId','ExecuteId','Query']
    with open(out_file,'w') as f:
        csv_h=csv.writer(f)
        # Write headers of CSV
        csv_h.writerow(header)

    data_rows=[]
    if job_name!=None:
        global root_xpath
        root_xpath=root_xpath+'[@action="{}"]'.format(job_name)
    check_xpath="/".join([job_xpath,persistence_xpath,statement_xpath,execute_xpath])
    for item in doc.iterfind(root_xpath):
        if item.find(check_xpath)!=None:
            dt=item.get('date')
            user=item.get('user')
            session=item.get('session')
            thread=item.get('thread')
            category=item.get('category')
            # rest element
            job=item.find(job_xpath)
            id=job.get('id')
            # Statement
            for persistence in job.iterfind(persistence_xpath):
                persistenceId=persistence.get('id')
                statement=persistence.find(statement_xpath)
                if statement.find('execute')!=None:
                    temp_execute_path=execute_xpath
                elif statement.find('executeUpdate')!=None:
                    temp_execute_path='executeUpdate'
                elif statement.find('executeBatch')!=None:
                    temp_execute_path='executeBatch'                    
                for execute in statement.iterfind(temp_execute_path):
                    executeId=statement.get('id')
                    parse_text=execute.text.strip().split()
                    parsed_query=" ".join(parse_text)
                    data_rows.append((dt,user,session,thread,category,id,persistenceId,executeId,parsed_query))
                    if len(data_rows)>30:
                        write_csv_data(out_file,data_rows)
                        data_rows.clear()
    if len(data_rows)>0:
        write_csv_data(out_file,data_rows)
        data_rows.clear()
    
def parse_sql_trace(trace_file_path:str)->None:
    if not os.path.exists(trace_file_path):
        print("The file {} path doesn't not exist".format(trace_file_path))
        sys.exit(-1)
    trace_file_name=os.path.basename(trace_file_path)
    if not trace_file_name.endswith('.xml'):
        print("The file {} doesn't have .xml extension".format(trace_file_name))
        sys.exit(-1)
    out_file=trace_file_name.split('.')[0]+'.csv'
    doc=ET.parse(trace_file_path)
    header=['Date','User','Session','Thread','Category','JobId','StatementId','ExecuteId','Query']
    with open(out_file,'w') as f:
        csv_h=csv.writer(f)
        # Write headers of CSV
        csv_h.writerow(header)

    data_rows=[]
    check_xpath="/".join([job_xpath,persistence_xpath,statement_xpath,execute_xpath])
    for item in doc.iterfind(root_xpath):
        if item.find(check_xpath)!=None:
            dt=item.get('date')
            user=item.get('user')
            session=item.get('session')
            thread=item.get('thread')
            category=item.get('category')
            # rest element
            job=item.find(job_xpath)
            id=job.get('id')
            # Statement
            for persistence in job.iterfind(persistence_xpath):
                persistenceId=persistence.get('id')
                statement=persistence.find(statement_xpath)
                if statement.find('execute')!=None:
                    temp_execute_path=execute_xpath
                elif statement.find('executeUpdate')!=None:
                    temp_execute_path='executeUpdate'
                elif statement.find('executeBatch')!=None:
                    temp_execute_path='executeBatch'                    
                for execute in statement.iterfind(temp_execute_path):
                    executeId=statement.get('id')
                    parse_text=execute.text.strip().split()
                    parsed_query=" ".join(parse_text)
                    data_rows.append((dt,user,session,thread,category,id,persistenceId,executeId,parsed_query))
                    if len(data_rows)>30:
                        write_csv_data(out_file,data_rows)
                        data_rows.clear()
    if len(data_rows)>0:
        write_csv_data(out_file,data_rows)
        data_rows.clear()

if __name__=="__main__":
    parse_job_sql_trace(sys.argv[1],sys.argv[2])