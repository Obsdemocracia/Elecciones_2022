import json
import tweepy
import os

client = tweepy.Client(os.environ.get('TWITTER_API'))
candidatos = json.load(open("candidatosID.json"))

for candidato in candidatos:
    if candidato["twitterID"] > 0 and ok:
        try:
            response = client.get_users_following(candidato["twitterID"],max_results=1000)
            if response.data is None:
                candidato["twitterFollowing"] = []
            else:
                candidato["twitterFollowing"] = [[f["username"],f["id"]] for f in response.data]
        except Exception as e:
            ok = False
            candidato["twitterFollowing"] = []
            print(e)
    else:
       candidato["twitterFollowing"] = []

with open('candidatosFollowing.json', 'w') as outfile:
    json.dump(candidatos, outfile)


