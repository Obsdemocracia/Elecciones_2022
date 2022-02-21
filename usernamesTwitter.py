# imports
import tweepy
import os
import pandas as pd

# Authentication

# API v2
#client = tweepy.Client(os.environ.get('TWITTER_API'))

# API v1
auth = tweepy.OAuth2BearerHandler(os.environ.get('TWITTER_API'))
api = tweepy.API(auth)

# search users
def searchUser(input):
    query = (name:=input.split("$"))[1]
    name = name[0]
    results = [None for i in range(6)]
    search = api.search_users(query,page=1,count=3)
    k=0
    for user in search:
        results[k*2] = user.name
        results[(k*2)+1] = user.screen_name
        k+=1
    index=['Name1', 'User1', 'Name2', 'User2', 'Name3', 'User3']
    index = [name+i for i in index]
    return pd.Series(results, index=index)
    
# read excel file
df=pd.read_excel("20220131_candidatos-congreso_18012022.xlsx", sheet_name="Candidatos")

# select rows
df1_157=df[df["Consecutivo"].ge(1) & df["Consecutivo"].le(157)]

# build query
df1_157["Busqueda1"] = "Bsq1$"+df1_157["NOMBRE1"].fillna('')+" "+df1_157["NOMBRE2"].fillna('')+" "+df1_157["APELLIDO1"].fillna('')
df1_157["Busqueda2"] = "Bsq2$"+df1_157["NOMBRE1"].fillna('')+" "+df1_157["APELLIDO1"].fillna('')
df1_157["Busqueda3"] = "Bsq3$"+df1_157["NOMBRE1"].fillna('')+" "+df1_157["NOMBRE2"].fillna('')+" "+df1_157["APELLIDO1"].fillna('')+" "+df1_157["AGRUPACIÓN POLITICA"].fillna('')
df1_157["Busqueda4"] = "Bsq4$"+df1_157["NOMBRE1"].fillna('')+" "+df1_157["APELLIDO1"].fillna('')+" "+df1_157["AGRUPACIÓN POLITICA"].fillna('')

# search 
df1_157 = df1_157.join(df1_157["Busqueda1"].apply(searchUser))
df1_157 = df1_157.join(df1_157["Busqueda2"].apply(searchUser))
df1_157 = df1_157.join(df1_157["Busqueda3"].apply(searchUser))
df1_157 = df1_157.join(df1_157["Busqueda4"].apply(searchUser))

# save data to excel file
df1_157.to_excel("outputTwitter.xlsx")  