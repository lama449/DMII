'''
Alex Lam and Maria Davis
Data Mining II final project
11/15/2020

This python file provides util functions for the scraper
'''
import datetime

def log(text):
    now = datetime.datetime.now()
    print('[' + now.strftime("%I:%M:%S") + '] ' + text)