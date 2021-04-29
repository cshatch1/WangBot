#This code stops WangBot from dying when not used
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "A cum-slave, back from the grave"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
