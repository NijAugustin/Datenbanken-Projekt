import string
def hashtags_filtern(hashtag):
    hashtags_string = ""
    temp = hashtag.split()
    i = 0
    for tag in temp:
        #Wenn ein '#' gefunden wurden, dann ist ein Hashtag im Tweet vorhanden
        if(tag.find("#") != -1):
            # Bereinigung des Hashtags
            tag = tag.replace('?','')
            tag = tag.replace('.','')
            tag = tag.replace('!','')
            tag = tag.replace(' ','')
            tag = tag.replace(',','')
            tag = tag.replace('*','')
            tag = tag.replace('\n','')
            #nochmal am # gesplittet, falls mehrere 
            #Hashtags vorhanden sind
            tag_liste =tag.split("#")
            for x in tag_liste:
                hashtags_string +="#"+x+";"
    return hashtags_string
    
in_string = ""
datei_name = "tweet_daten.csv"  #Name der csv.-Datei, die gelesen werden soll
with open(datei_name,"r") as fp:
    for line in fp:
        # Datei wird zeilenweise eingelesen
        in_string = in_string+line
in_string = string.replace(in_string, ';;', ';')

#nachdem die gesamte Datei in einem String gespeichert wurde, die der String so aufgespaltet,dass jeder Tweet+dessen Information ein Listenelement ist
liste =in_string.split("\r\n")

#*** Dateiaufbau:   "TWEETID\tTWEETNAME\tTWEETTEXT\tTWEETZEIT\tRETWEETCOUNT\tFAVOURITECOUNT\tHASHTAGS\n" - jede Information wird durch einen Tabulator getrennt
out = ""
i=1
while (i < len(liste)):
    temp = liste[i].split(";")
     # Wenn das Hashtag-Symbol in einem Tweet gefunden wurde, dann wwerden die relevanten Informationen ausgelesen und gespeichert
    if(len(temp) == 9 and temp[1].find("#") != -1 ):
        tweet_id = i
        tweet_name = temp[0]
        tweet_text = temp[1].replace('"','')
        tweet_text = tweet_text.replace('\n',' ')
        tweet_text = temp[1].replace('"','')
        tweet_text = tweet_text.replace('\n',' ')
        tweet_zeit = temp[3]
        tweet_retweet_count=temp[5]
        tweet_fav_count=temp[6]
        out += str(tweet_id)+"\t"+tweet_name +"\t"+tweet_text+"\t"+tweet_zeit+"\t"+str(tweet_retweet_count)+"\t"+str(tweet_fav_count)+"\t"+hashtags_filtern(tweet_text)+"\n"
    i+=1
    
#Daten in Datei speichern
schreiben = open("tweets_gefiltert.txt","w") # Ergebnis speichern
schreiben.write(out) 
schreiben.close()
