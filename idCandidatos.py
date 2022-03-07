import json
import tweepy
import os
import re
import unidecode

client = tweepy.Client(os.environ.get('TWITTER_API'))
candidatos = json.load(open("candidatos.json"))
ok = True

for candidato in candidatos:
    if not ok:
        candidato["twitterID"] = -3
    elif re.match(r'^[@][A-Za-z0-9_]{1,15}$', handle := unidecode.unidecode(candidato["twitterHandle"].strip())) is not None:
        try:
            response = client.get_user(username = handle[1:])
            if response.data is None:
                candidato["twitterID"] = -2
            else:
                candidato["twitterID"] = response.data.id
        except Exception as e:
            ok = False
            candidato["twitterID"] = -3
            print(e)

    else:
       candidato["twitterID"] = -1
    
with open('candidatosID.json', 'w') as outfile:
    json.dump(candidatos, outfile)
  

