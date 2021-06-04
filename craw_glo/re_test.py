import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter

link = 'https://topphimmoi.com/'

r = requests.get(link)
print(r.url)
