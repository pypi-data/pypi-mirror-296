import argparse
from sj_util.helpers.utils import write_log
from sj_util.helpers.job_trace import parse_sql_trace,parse_job_sql_trace

LOG_CATEGORY="CLARITY_CLI"
def parse_trace(file_name:str,job_name:str=None):
    if job_name!=None:
        write_log(category=LOG_CATEGORY,message="Parsing Trace file {} for Job {}".format(file_name,job_name))
    else:
        write_log(category=LOG_CATEGORY,message="Parsing Trace file {}".format(file_name))


def cli_entry_point():
    print("Clarity CLI interface provding utility functions.")
    parser=argparse.ArgumentParser()
    subparsers=parser.add_subparsers(dest="command")

    parser_parse=subparsers.add_parser('parse',help="Parse Clarity XML Trace file",description="Parse Clarity XML Trace file. If the Job name is provided only parses the Job related data.",)
    parser_parse.add_argument('-f','--filename',help="Path to XML trace file to parse.",required=True)
    parser_parse.add_argument('-j','--jobname',help="Job name(optional), to parse only entries related to Job.",required=False)

    args=parser.parse_args()
    
    if args.command=="parse":
        if args.jobname!=None:
            parse_job_sql_trace(args.filename,args.jobname)
        else:
            parse_sql_trace(args.filename)
    else:
        parser.print_help()

if __name__=="__main__":
    parse_sql_trace("/Users/sj652744/Downloads/bg-trace.xml")