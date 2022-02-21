# imports
from googlesearch import search
from googlesearch import get_random_user_agent
from urllib.parse import urlparse
import pandas as pd
import time, random

status = None

# select user_agent
user = get_random_user_agent()
user = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'

# look for queries in google: adapted from 
def identify_twitter(query):  
    username=""
    global status

    # check if there is no error (429)
    if status is not None:
        return status
    try:
        # print(query)
        response = search(query, tld="co.in", num=3, stop=3, pause=5, user_agent=user)
        for result in response:
            parsed_url=urlparse(result)
            # check that URL contains Twitter
            if "twitter" in parsed_url.hostname:
                # avoid wrong URLS: status, search, hashtags
                if ("status" not in parsed_url.path) and ("search" not in parsed_url.path) and ("hashtag" not in parsed_url.path):
                    username = "@"+parsed_url.path[1:]
                    break
        # add random time delay
        time.sleep(random.random()*2)
    # catch exception
    except Exception as e:
        status = str(e)
        return status
    return username

# exhaustive search
def build_search(row):

    # get row information
    row = row.fillna('')
    name1, name2, last1, last2, corporacion, depto, partido = row["NOMBRE1"], row["NOMBRE2"], row["APELLIDO1"], row["APELLIDO2"], row["DESC_CORP"], row["DESC_DPTO"], row["AGRUPACIÓN POLITICA"]

    # check if there is a second name
    if name2 != "":
        # query 1
        query = name1+" "+name2+" "+last1+" "+last2+" inurl:twitter"
        if (username:=identify_twitter(query)) != "":
            return username
        # query 2
        query = name1+" "+name2+" "+last1+" inurl:twitter"
        if (username:=identify_twitter(query)) != "":
            return username
        # query 3
        query = name1+" "+name2+" "+corporacion+" inurl:twitter"
        if (username:=identify_twitter(query)) != "":
            return username
    
    # no second name
    else:
        # query 1
        query = name1+" "+last1+" "+last2+" inurl:twitter"
        if (username:=identify_twitter(query)) != "":
            return username

    # last query
    query = name1+" "+last1+" "+corporacion+" inurl:twitter"
    if (username:=identify_twitter(query)) != "":
        return username

    # no user found
    return ""
    
# read excel file
df=pd.read_excel("20220131_candidatos-congreso_18012022.xlsx", sheet_name="Candidatos")

# select rows
df1_157=df[df["Consecutivo"].ge(1) & df["Consecutivo"].le(157)]


df1_157["Busqueda1"] = df1_157["NOMBRE1"].fillna('')+" "+df1_157["NOMBRE2"].fillna('')+" "+df1_157["APELLIDO1"].fillna('')+ " "+df1_157["APELLIDO2"].fillna('')+ " "+df1_157["DESC_CORP"].fillna('')+ " "+df1_157["DESC_DPTO"].fillna('')+" inurl:twitter"
df1_157["Busqueda2"] = df1_157["NOMBRE1"].fillna('')+" "+df1_157["NOMBRE2"].fillna('')+" "+df1_157["APELLIDO1"].fillna('')+ " "+df1_157["APELLIDO2"].fillna('')+ " "+df1_157["AGRUPACIÓN POLITICA"].fillna('')+" inurl:twitter"

# look for usernames and save them in a new column
df1_157["usernames1"]=df1_157["Busqueda1"].apply(identify_twitter)
df1_157["usernames2"]=df1_157["Busqueda2"].apply(identify_twitter)
df1_157["busquedaExahustiva"]=df1_157.apply(build_search, axis=1)

# save data to excel file
df1_157.to_excel("output.xlsx")  
