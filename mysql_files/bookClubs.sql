DROP TABLE IF EXISTS ClubMeetings;
DROP TABLE IF EXISTS BookClubs;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS Members;

CREATE TABLE Members (
    memberID int(11) NOT NULL AUTO_INCREMENT,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    PRIMARY KEY (memberID)
);

INSERT INTO Members (firstName, lastName, email)
    VALUES ('Inigo', 'Montoya', 'inigo.montoya@florian.com');
INSERT INTO Members (firstName, lastName, email)
    VALUES ('Jay', 'Gatsby', 'jgats@westegg.org');
INSERT INTO Members (firstName, lastName, email)
    VALUES ('Veruca', 'Salt', 'veruca.salt@wonka.edu');


CREATE TABLE Genres (
    genreID int(11) NOT NULL AUTO_INCREMENT,
    genre varchar(255) NOT NULL,
    PRIMARY KEY (genreID)
);


CREATE TABLE BookClubs (
    bookClubID int(11) NOT NULL AUTO_INCREMENT,
    clubName varchar(255) NOT NULL,
    meetingFrequency int(11) DEFAULT NULL,
    clubGenreID int(11) NOT NULL,
    clubLeaderID int(11) NOT NULL,
    PRIMARY KEY (bookClubID),
    FOREIGN KEY (clubGenreID)
        REFERENCES Genres(genreID),
    FOREIGN KEY (clubLeaderID)
        REFERENCES Members(memberID)
);


CREATE TABLE Books (
    bookID int(11) NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    author varchar(255) NOT NULL,
    bookGenreID int(11) NOT NULL,
    PRIMARY KEY (bookID),
    FOREIGN KEY (bookGenreID)
        REFERENCES Genres(genreID)
);

CREATE TABLE ClubMeetings (
    meetingID int(11) NOT NULL AUTO_INCREMENT,
    meetingDateTime datetime(0) NOT NULL,
    bookClubID int(11) NOT NULL,
    meetingBookID int(11) NOT NULL,
    meetingLeaderID int(11) NOT NULL,
    PRIMARY KEY (meetingID),
    FOREIGN KEY (meetingBookID)
        REFERENCES Books(bookID),
    FOREIGN KEY (meetingLeaderID)
        REFERENCES Members(memberID)
);


