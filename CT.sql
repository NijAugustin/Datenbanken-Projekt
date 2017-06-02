CREATE TABLE tweet (
    tweetID int ,
    name varchar(255),
    text varchar(255),
    retweetcount int,
    favouritecount int,
    datum date,
    uhrzeit varchar(255),
    PRIMARY KEY (tweetID)
);

CREATE TABLE hashtags (
    hashtag varchar(255), 
    PRIMARY KEY (hashtag)
);

CREATE TABLE share (
    tweetID int,
    hashtag varchar(255),
    FOREIGN KEY(tweetID)
	REFERENCES tweet(tweetID), 
   FOREIGN KEY(hashtag)
   REFERENCES hashtags(hashtag), 
);