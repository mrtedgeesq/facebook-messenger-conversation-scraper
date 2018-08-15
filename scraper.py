import codecs
import datetime
import csv
import urllib.parse

from bs4 import BeautifulSoup
f = codecs.open("message.html", 'r', 'utf-8')
html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')

with open('out.csv', 'w', newline='') as csvfile:
    fieldnames = ['author', 'time', 'words', 'chars', 'body']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    #print(soup.prettify())
    for message in soup.find_all("div", class_="pam"):
        authorTag = message.find("div", class_="_2lel")
        bodyTag = message.find("div", class_="_2let")
        timeTag = message.find("div", class_="_2lem")

        if authorTag is not None and timeTag is not None:
            author = authorTag.string
            bodyText = bodyTag.find(text=True) if bodyTag is not None else ""
            body = bodyText.string if bodyText is not None else ""
            safebody = urllib.parse.quote(body) # encodes the message body as a URL safe string so that we don't need to worry about escaping everthing
            time = timeTag.string
            #timeObj = datetime.datetime.strptime(time, "%d %B %Y %H:%M")
            words =  len(body.split())
            chars = len(body)
            print(author, time, words, chars, safebody)
            writer.writerow({'author': author, 'time': time, 'words': words, 'chars': chars, 'body': safebody})