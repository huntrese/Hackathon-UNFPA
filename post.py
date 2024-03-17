import requests

receiver="+37368352111"
message="hola hola"
requests.post(f"http://localhost:5678/webhook-test/68472022-64e5-4e26-a13f-be0bbbd7394e",{"Target":{receiver},"Message":{message}})