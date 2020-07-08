DROP TABLE IF EXISTS Members;

CREATE TABLE Members (
    memberID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    email varchar(255) NOT NULL
);


DROP TABLE IF EXISTS Genres;

CREATE TABLE Genres (
    genreID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    genre varchar(255) NOT NULL
);


DROP TABLE IF EXISTS BookClubs;

CREATE TABLE BookClubs (
    bookClubID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    clubName varchar(255) NOT NULL,
    meetingFrequency int(11) DEFAULT NULL,
    clubGenreID int(11) NOT NULL,
    clubLeaderID int(11) NOT NULL,
    FOREIGN KEY (clubGenreID)
        REFERENCES Genres(genreID),
    FOREIGN KEY (clubLeaderID)
        REFERENCES Members(memberID)
);

DROP TABLE IF EXISTS ClubMeetings;

CREATE TABLE ClubMeetings (
    meetingID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dateTime dateTime NOT NULL,
    bookClubID int(11) NOT NULL,
    meetingBookID int(11) NOT NULL,
    meetingLeaderID int(11) NOT NULL,
    FOREIGN KEY (meetingBookID)
        REFERENCES Books(bookID),
    FOREIGN KEY (meetingLeaderID)
        REFERENCES Members(memberID)
);


DROP TABLE IF EXISTS Books;

CREATE TABLE Books (
    bookID int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title varchar(255) NOT NULL
    author varchar(255) NOT NULL
    bookGenreID int(11) NOT NULL
    FOREIGN KEY (bookGenreID)
        REFERENCES Genres(genreID)
)