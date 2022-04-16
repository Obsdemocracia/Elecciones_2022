import tweepy
import os
import time
import sqlDB
import pickle

client = tweepy.Client(os.environ.get('TWITTER_API'))
followers = [2247024336]

with open('FicoGutierrez_followers.pkl', 'rb') as f:
    data = pickle.load(f)
    followers = data["FicoGutierrez"]

i = 0
if sqlDB.connect():
    for user in followers:
        try:
            # 900 request cada 15 min = 1 request cada segundo
            time.sleep(1.2)
            response = client.get_user(id = user,user_fields=["public_metrics","id","username","name"])
            if response.data is None:
                print("No se encontró el id ", user)
            else:
                try:
                    sqlDB.add_user(response.data.id,response.data.username,response.data.name,response.data.public_metrics["followers_count"],response.data.public_metrics["following_count"],response.data.public_metrics["tweet_count"])
                except Exception as e:
                    print(e)
                    print("Error: ",user)
        except Exception as e:
            print(e)
            print("Error: ",user)
        finally:
            print(i)
            i += 1
    sqlDB.get_users()
    sqlDB.disconnect()
