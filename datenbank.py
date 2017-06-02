import psycopg2
from psycopg2 import sql
def doppelte_filtern(hashtag,liste):
    for x in liste:
        if(x == hashtag):
            return False
    return True

def sonderzeichen(a):
    tag         = a.replace("\n","")
    tag         = tag.replace(":","")
    tag         = tag.replace("?","")
    tag         = tag.replace(".","")
    tag         = tag.replace("!","")
    tag         = tag.replace("-","")
    tag         = tag.decode("utf-8",'ignore')
    return tag
    
tweet_liste = []
datei_name = "tweets_gefiltert.txt"

with open(datei_name,"r") as fp:
    for line in fp:
        tweet_liste.append(line)

#****** Hashtags fuer das Einfuegen in Tabelle 'hashtags' vorbereiten
tag_liste = []
for tweet in tweet_liste:
    hashtag_liste = tweet.split("\t")[6].split(";")
    j = 0
    for tag in hashtag_liste:
        tag = sonderzeichen(tag)
        #doppelte Hashtags finden und heraufiltern und Sonderzeichen entfernen
        if(doppelte_filtern(tag,tag_liste)):
            tag_liste.append(tag)

#****** Verbindung zur Datenbank 'election' aufbauen
print "***Verbindung zur Datenbank 'Election' aufbauen***"
conn = psycopg2.connect("host='localhost' dbname='election' user='postgres' password='postgres'")
cursor = conn.cursor()
#******** Hashtags in die Tabelle 'Hashtag' einfuegen
print "***Hashtags in die Tabelle 'Hashtag' schreiben***"
for h in tag_liste:
     cursor.execute(sql.SQL("INSERT INTO hashtags(hashtag) VALUES (%s);"),[h])
     conn.commit()   
tweet_id = 0
print "***Tweets in die Tabelle 'Tweets' schreiben***"
print "***TweetID und Hashtags in die Tabelle 'Share' schreiben***"
for tweet in tweet_liste:
    tweet_infos =  tweet.split("\t")
    #*********  Tweets in die Tabelle 'tweets'-einfuegen
    
    name            = tweet_infos[1]
    text            = tweet_infos[2]
    text            = text.decode("utf-8",'ignore')
    datum           = tweet_infos[3].split("T")[0]
    uhrzeit         = tweet_infos[3].split("T")[1]
    retweet_count   = int(tweet_infos[4])
    fav_count       = int(tweet_infos[5])
    
    cursor.execute(("INSERT INTO tweets(tweetid,autor,text,favourite,retweet,datum,uhrzeit) VALUES (%s,%s,%s,%s,%s,%s,%s);"),[tweet_id,name,text,fav_count,retweet_count,datum,uhrzeit])
    conn.commit()
    
    
    #**********     Hashtag und TweetID in die 'Share'-Tabelle einfuegen
    for hashtag in tweet_infos[6].split(";"):
        hashtag     = sonderzeichen(hashtag)
        if(len(hashtag) >1):
            cursor.execute(sql.SQL("INSERT INTO share(tweetid,hashtag) VALUES (%s,%s);"),[tweet_id,hashtag])
            conn.commit()
    tweet_id+=1
# Verbindung zur Datenbank beenden
print "***Verbindung zur Datenbank trennen***"
cursor.close()
conn.close()