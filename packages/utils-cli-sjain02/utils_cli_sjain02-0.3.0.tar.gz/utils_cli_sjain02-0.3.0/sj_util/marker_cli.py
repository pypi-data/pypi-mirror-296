import sqlite3
from urltitle import URLTitleReader, URLTitleError
import argparse
from sj_util.helpers.decorators import pprint
from sj_util.helpers.utils import write_csv_data


def get_db_connection():
  
    db_connection=sqlite3.connect('app.db')
    return db_connection

def execute_query(query,fetch:str=None):
    """Execute the SQL query.
    query: str -> The SQL query
    fetch: str-> all|one|None determines the result to be returned or not
    """
    connection=get_db_connection()
    cursor=connection.cursor()
    result=None
    if fetch=="all":
        cursor=connection.execute(query)
        result=cursor.fetchall()
    elif fetch=="one":
        cursor=connection.execute(query)
        result=cursor.fetchone()
    else:
        result=connection.execute(query)
    connection.commit()
    connection.close()
    return result
    
def initialize_db():
    bookmark_query="""
Create table if not exists bookmark(
id integer primary key autoincrement,
title text not null,
url text not null unique
)
"""
    execute_query(bookmark_query)

def normalizetitle(title):
    normalize_terms=['\'','#','/']
    normalize_title=None
    for replace_char in normalize_terms:
        normalize_title=title.replace(replace_char,'')
    return normalize_title

def insert_bookmark(url,explict_title=None):
    reader=URLTitleReader(verify_ssl=False)
    title=None
    try:
        title=reader.title(url)
        normalize_title=normalizetitle(title)
        if explict_title!=None:
            title=explict_title
        insert_query="""insert or ignore into bookmark(title,url) values('{}','{}')""".format(normalize_title,url)
        result=execute_query(insert_query)
        if result.lastrowid==0:
            pprint("No record inserted. Either it exist or URL is malformed")
        else:
            pprint("The recorded added with id: {}".format(result.lastrowid))
    except URLTitleError:
        pprint("Error: Unable to extract title from {}. It may be malformed!".format(url))

def update_title(id,new_title):
    if id.isnumeric():
        old_bookmark=get_bookmarks(id=id,fetch=True)
        if old_bookmark:
            update_query="""update bookmark set title='{}' where id={}""".format(new_title,id)
            result=execute_query(update_query)
            if result!=None and result.rowcount==1:
                pprint("Update record with id {}".format(id))

def export():
    result=get_bookmarks(fetch=True)
    write_csv_data('bookmark.csv',result)
    pprint("The bookmarks are exported to bookmark.csv")


def get_bookmarks(id=None,fetch=False):
    """Get Bookmarks, if the fetch is set to True, the result will be returned else will be printed on the stdout"""
    if id==None:
        select_query="""select * from bookmark"""
        result=execute_query(select_query,fetch="all")
    elif id.isnumeric():
        select_query="""select * from bookmark where id={}""".format(id)
        result=execute_query(select_query,fetch="one")
    
    if result!=None and len(result)>0:        
        if fetch==True:
            return result
        else:
            pprint(result)
    else:
        if id==None:
            pprint("No Record found!")
        else:
            pprint("No record found with id {}".format(id))

def search_bookmark(search_term):
    formatted_search=["title like '%"+search+"%'" for search in search_term]
    search_string=" or ".join(formatted_search)
    select_query="""select title, url from bookmark where ({})""".format(search_string)
    result=execute_query(select_query,fetch="all")
    if len(result)>0:
        pprint(result)
    else:
        pprint("No Record found!")

def delete_bookmark(ids):
    delete_query="""delete from bookmark where id in ({})""".format(ids)
    result=execute_query(delete_query)
    pprint("Delete {} records".format(result.rowcount))

def cli_entry_point():
    print("Marker CLI interface provding utility function for Bookmark.")
    parser=argparse.ArgumentParser()
    subparsers=parser.add_subparsers(dest="command")

    app_parser=subparsers.add_parser('init',help="Initialized Bookmark DB.")
    app_parser=subparsers.add_parser('add',help="Add URL to Bookmark table.")
    app_parser.add_argument('-u','--url',help="URL to bookmark",required=True)
    app_parser.add_argument('-t','--title',help="Title for the URL, to overwrite decoded Title from URL",required=False)
    app_parser=subparsers.add_parser('search',help="Search all bookmarks matching search term/s.")
    app_parser.add_argument('-s','--searchterm',type=str,help="Search terms,Comma separated.",required=True)
    app_parser=subparsers.add_parser('get',help="Get all bookmark")
    app_parser.add_argument('-i','--id',help="Bookmark Id",required=False)
    app_parser=subparsers.add_parser('export',help="Export bookmarks to bookmark.csv")
    app_parser=subparsers.add_parser('delete',help="Delete bookmarks by id. Get id by marker-cli get")
    app_parser.add_argument('-i','--ids',type=str,help="Comma seperated id's.",required=True)
    app_parser=subparsers.add_parser('update',help="Update title of bookmark by id")
    app_parser.add_argument('-i','--id',type=str,help="Bookmark id",required=True)
    app_parser.add_argument('-t','--title',type=str,help="New Title",required=True)

    args=parser.parse_args()
    if args.command=="init":
        initialize_db()
    elif args.command=="add":
        insert_bookmark(args.url,args.title)
    elif args.command=="search":
        search_string=args.searchterm.split(',')
        print()
        search_bookmark(search_string)
    elif args.command=="get":
        if args.id==None:
            get_bookmarks()
        else:
            get_bookmarks(id=args.id)
    elif args.command=="export":
        export()
    elif args.command=="delete":
        delete_bookmark(args.ids)
    elif args.command=="update":
        update_title(args.id,args.title)
    else:
        parser.print_help()

# initialize_db()
# insert_bookmark("https://medium.com/analytics-vidhya/sqlite-database-crud-operations-using-python-3774929eb799")
# insert_bookmark("https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/release-announcements/CA-PPM-Release-and-Support-Lifecycle-Dates/5894","CA PPM Release and Support Lifecycle Dates")
# insert_bookmark("https://knowledge.broadcom.com/external/article?articleId=9783")
# insert_bookmark("https://knowledge.broadcom.com/external/article/214504/operation-not-permitted-error-while-star.html")
# app-cli add -u https://knowledge.broadcom.com/external/article/200076
# app-cli add -u https://knowledge.broadcom.com/external/article/375684
# https://knowledge.broadcom.com/external/article/9783
# get_bookmarks()
# # search_bookmark("cycle")
# search_bookmark(["clarity","portal"])

if __name__=="__main__":
    update_title("22","UVMS 6.10.101 or superior compatibility with DU 6.x")
    # search_bookmark()
    # delete_bookmark(["1","2"])
    # insert_bookmark("https://medium.com/analytics-vidhya/sqlite-database-crud-operations-using-python-3774929eb799")
    # insert_bookmark("https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/release-announcements/CA-PPM-Release-and-Support-Lifecycle-Dates/5894")

