CREATE TABLE BookClubs (
    bookClubID int(11) NOT NULL AUTO_INCREMENT,
    clubName varchar(255) NOT NULL,
    meetingFrequency int(11) DEFAULT NULL,
    clubGenre int(11) NOT NULL,
    clubLeader int(11) DEFAULT NULL,
    PRIMARY KEY (bookClubID)
);

CREATE TABLE Genres {
    genreID int(11) NOT NULL AUTO_INCREMENT,
    genre varchar(255) NOT NULL
} 