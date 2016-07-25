
import os

filename = open('./items.json', 'r')

date = filename.read()

def printzh(date):
    for i in date:
        print i.encode('utf-8')
        
printzh(date)
