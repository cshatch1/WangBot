#This code is useless now, but I'm going to keep it anyways
#because I took all the time to code it and I *might* need
#it later


import re
import json
import sys
import requests
import urllib.request
import os
import time

INSTAGRAM_USERNAME = 'jaywang4968'
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/837363178031677480/yiqHnePBSVypGb79NtZ0Fz0boN-YrJG_4Spt6rXS5MCCZ67ccPpjp0FQo1Uutp0p6Bdn'
TIME_INTERVAL = 1.5

def get_user_fullname(html):
  return html.json()["graphql"]["user"]["fullname"]

def get_total_photos(html):
  return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])

def get_last_publication_url(html):
  return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]

def get_last_photo_url(html):
  return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]

def get_last_thumb_url(html):
  return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]

def get_description_photo(html):
  return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]

def webhook(WEBHOOK_URL, html):
  data = {}
  data["embeds"] = []
  embed = {}
  embed["image"] = {"url":get_last_thumb_url(html)}
  data["embeds"].append(embed)
  result = requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
  try:
    result.raise_for_status()
  except requests.exceptions.HTTPError as err:
    print(err)
  else:
    print("Image successfully posted in Discord, code {}.".format(result.status_code))

def get_instagram_html(INSTAGRAM_USERNAME):
  headers = {
      "Host": "www.instagram.com",
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
  }
  html = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
  return html

def main():
  try:
    html = get_instagram_html(INSTAGRAM_USERNAME)
    if(os.environ.get("LAST_IMAGE_ID") == get_last_publication_url(html)):
      print("Not new image to post in discord.")
    else:
      os.environ["LAST_IMAGE_ID"] = get_last_publication_url(html)
      print("New image to post in discord.")
      webhook(WEBHOOK_URL, get_instagram_html(INSTAGRAM_USERNAME))
  except Exception as e:
    print(e)

if __name__ == "__main__":
    if INSTAGRAM_USERNAME != None and WEBHOOK_URL != None:
        while True:
            main()
            time.sleep(float(TIME_INTERVAL or 600)) # 600 = 10 minutes
    else:
        print('Please configure variables properly!')