from datetime import datetime
import pyshorteners
import re
from flask import Flask, request, send_file,jsonify
# from pyngrok import ngrok
import tempfile

# Set up Flask app
app = Flask(__name__)
# ngrok.set_auth_token("2aUKxhETRkeaHgT49YAsp3KlWpc_3WYPatDEW3zozbZzFdw8A")


import os
import pymysql
import natsort
import time
import requests
# MySQL database connection settings
db_host = "monorail.proxy.rlwy.net"
db_user = "root"
db_password = "qnbMsdLJIhIZpwwiUuyWwQPhTwCPaeyI"
db_name = "railway"



conn = pymysql.connect(
      host=db_host,
      user=db_user,
      password=db_password,
      database=db_name,
      port=48084,

      # ssl={'ca': '/content/cacert.pem'}  # Specify the path to your SSL certificate file
  )
cursor = conn.cursor()
type_tiny = pyshorteners.Shortener()

posted=False




def check(result):
    try:
        # Check if the author already exists in the table
        cursor.execute("SELECT * from User")
        result.append( cursor.fetchall() )
        print(result)
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    



while not posted:
    time.sleep(15)
    post=[]
    message=""
    hashtag="#mihai"
    receiver="+37378680295"


    if not check(post):
        continue
    post=post[0][0]
    print(post[0])
    user_id=post[0]
    db_time=int(post[1])
    print(db_time,type(db_time))
    response=requests.get("https://graph.instagram.com/me/media?fields=id,caption,media_url,media_type,timestamp,children{media_url}&limit=1&access_token=IGQWROZAER2M3d6T2xhbDB2OUpXelRfUDNlRFJYRWY2ZADZAfenQwaFIwVnE4QVBMUWxVMVc0MDN1Q0pTa2txaGl0RzEtdTg4Ti1ocHk0Y0t2U3BPU1NLSG9nMHhSNW1FODFmck5TY3dKSzZA0NHJEN2F1NENSNHhXVTgZD")
    data=response.json()['data']
    for i in data: 
        if "caption" in i:
            code=i['caption']
            print("++",code)
            if hashtag in code:
                match = re.findall(r"\#[\S]+", code, flags=re.MULTILINE)
                # print(match)
                for m in match:
                    code = code.replace(m, "")
                # [code.replace(x, "") for x in match]
                print(code)
                message = code
            


            
            
            dt_object = datetime.strptime(i["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
            unix_timestamp = int(dt_object.timestamp())
            print(unix_timestamp)
            if unix_timestamp > db_time:
                long_url = i['media_url']
                short_url = type_tiny.tinyurl.short(long_url)
                
                print("The Shortened URL is: " + short_url)
                message+=f"\n{short_url}"
                # TODO
                requests.post(f"http://localhost:5678/webhook/68472022-64e5-4e26-a13f-be0bbbd7394e",{"Target":{receiver},"Message":{message}})
                cursor.execute(f"UPDATE User SET last_post = {unix_timestamp} WHERE id = 1;")
                conn.commit()
                posted=True