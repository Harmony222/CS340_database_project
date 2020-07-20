DROP TABLE IF EXISTS meetings_members;
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
INSERT INTO Members (firstName, lastName, email)
    VALUES ('Atticus', 'Finch', 'attifinch@maycomb.com');
INSERT INTO Members (firstName, lastName, email)
    VALUES ('Hester', 'Prynne', 'h.prynne@pearl.edu');
INSERT INTO Members (firstName, lastName, email)
    VALUES ('John', 'Watson', 'watsonj@bakerst.net');
INSERT INTO Members (firstName, lastName, email)
    VALUES ('Annabel', 'Lee', 'ann.lee@poe.org');
INSERT INTO Members (firstName, lastName, email)
    VALUES ('Elizabeth', 'Bennet', 'lizzyb@longbourn.net');
INSERT INTO Members (firstName, lastName, email)
    VALUES ('Lyra', 'Belacqua', 'lyra@oxford.edu');


CREATE TABLE Genres (
    genreID int(11) NOT NULL AUTO_INCREMENT,
    genre varchar(255) UNIQUE NOT NULL,
    PRIMARY KEY (genreID)
);

INSERT INTO Genres (genre) VALUES ('classic');
INSERT INTO Genres (genre) VALUES ('graphic novel');
INSERT INTO Genres (genre) VALUES ('mystery');
INSERT INTO Genres (genre) VALUES ('science fiction');
INSERT INTO Genres (genre) VALUES ('history');
INSERT INTO Genres (genre) VALUES ('short story');
INSERT INTO Genres (genre) VALUES ('biography');
INSERT INTO Genres (genre) VALUES ('poetry');
INSERT INTO Genres (genre) VALUES ('children');


CREATE TABLE BookClubs (
    bookClubID int(11) NOT NULL AUTO_INCREMENT,
    clubName varchar(255) NOT NULL,
    meetingFrequency varchar(255),
    clubGenreID int(11) NOT NULL,
    clubLeaderID int(11) NOT NULL,
    PRIMARY KEY (bookClubID),
    FOREIGN KEY (clubGenreID)
        REFERENCES Genres(genreID),
    FOREIGN KEY (clubLeaderID)
        REFERENCES Members(memberID)
);

INSERT INTO BookClubs (clubName, meetingFrequency, clubGenreID, clubLeaderID)
    VALUES ('But I Progress Book Club', 
            'monthly', 
            (SELECT genreID FROM Genres WHERE genre = 'short story'),
            (SELECT memberID FROM Members WHERE email = 'attifinch@maycomb.com'));
INSERT INTO BookClubs (clubName, meetingFrequency, clubGenreID, clubLeaderID)
    VALUES ('The Book Was Better',
            'twice monthly',
            (SELECT genreID FROM Genres WHERE genre = 'mystery'),
            (SELECT memberID FROM Members WHERE email = 'watsonj@bakerst.net'));
INSERT INTO BookClubs (clubName, meetingFrequency, clubGenreID, clubLeaderID)
    VALUES ('Get Lit Book Club', 
            'monthly',
            (SELECT genreID FROM Genres WHERE genre = 'classic'),
            (SELECT memberID FROM Members WHERE email = 'h.prynne@pearl.edu'));
INSERT INTO BookClubs (clubName, meetingFrequency, clubGenreID, clubLeaderID)
    VALUES ('Beyond Words Book Club',
            'weekly',
            (SELECT genreID FROM Genres WHERE genre = 'poetry'),
            (SELECT memberID FROM Members WHERE email = 'ann.lee@poe.org'));


CREATE TABLE Books (
    bookID int(11) NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    author varchar(255) NOT NULL,
    bookGenreID int(11) NOT NULL,
    PRIMARY KEY (bookID),
    FOREIGN KEY (bookGenreID)
        REFERENCES Genres(genreID)
);

INSERT INTO Books (title, author, bookGenreID)
    VALUES ('Florida', 
            'Lauren Groff', 
            (SELECT genreID FROM Genres WHERE genre = 'short story'));
INSERT INTO Books (title, author, bookGenreID)
    VALUES ('Nine Stories',
            'J.D. Salinger',
            (SELECT genreID FROM Genres WHERE genre = 'short story'));
INSERT INTO Books (title, author, bookGenreID)
    VALUES ('Stone Mattress',
            'Margaret Atwood',
            (SELECT genreID FROM Genres WHERE genre = 'short story'));
INSERT INTO Books (title, author, bookGenreID)
    VALUES ('A Farewell to Arms',
            'Ernest Hemingway',
            (SELECT genreID FROM Genres WHERE genre = 'classic'));
INSERT INTO Books (title, author, bookGenreID)
    VALUES ('The Stranger',
           'Albert Camus',
           (SELECT genreID FROM Genres WHERE genre = 'classic'));

CREATE TABLE ClubMeetings (
    meetingID int(11) NOT NULL AUTO_INCREMENT,
    `dateTime` datetime NOT NULL,
    bookClubID int(11) NOT NULL,
    meetingBookID int(11) UNIQUE,
    meetingLeaderID int(11) NOT NULL,
    PRIMARY KEY (meetingID),
    FOREIGN KEY (meetingBookID)
        REFERENCES Books(bookID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (meetingLeaderID)
        REFERENCES Members(memberID)
);

INSERT INTO ClubMeetings (`dateTime`, bookClubID, meetingBookID, meetingLeaderID)
    VALUES ('2020-06-20 19:30',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'But I Progress Book Club'),
            (SELECT bookID FROM Books WHERE title = 'Stone Mattress'),
            (SELECT memberID FROM Members WHERE email = 'attifinch@maycomb.com'));
INSERT INTO ClubMeetings (`dateTime`, bookClubID, meetingBookID, meetingLeaderID)
    VALUES ('2020-09-20 19:30',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'But I Progress Book Club'),
            (SELECT bookID FROM Books WHERE title = 'Nine Stories'),
            (SELECT memberID FROM Members WHERE email = 'inigo.montoya@florian.com'));
INSERT INTO ClubMeetings (`dateTime`, bookClubID, meetingBookID, meetingLeaderID)
    VALUES ('2020-08-20 19:30',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'But I Progress Book Club'),
            (SELECT bookID FROM Books WHERE title = 'Florida'),
            (SELECT memberID FROM Members WHERE email = 'jgats@westegg.org'));
INSERT INTO ClubMeetings (`dateTime`, bookClubID, meetingBookID, meetingLeaderID)
    VALUES ('2020-8-27 18:00',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'Get Lit Book Club'),
            (SELECT bookID FROM Books WHERE title = 'A Farewell to Arms'),
            (SELECT memberID FROM Members WHERE email = 'veruca.salt@wonka.edu'));
INSERT INTO ClubMeetings (`dateTime`, bookClubID, meetingBookID, meetingLeaderID)
    VALUES ('2020-9-24 18:00',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'Get Lit Book Club'),
            (SELECT bookID FROM Books WHERE title = 'The Stranger'),
            (SELECT memberID FROM Members WHERE email = 'lizzyb@longbourn.net'));
            

CREATE TABLE meetings_members (
    meetingID int(11) NOT NULL,
    memberID int(11) NOT NULL,
    PRIMARY KEY (meetingID, memberID),
    FOREIGN KEY (meetingID)
        REFERENCES ClubMeetings(meetingID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (memberID)
        REFERENCES Members(memberID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO meetings_members (meetingID, memberID)
    VALUES ('3', '1');
INSERT INTO meetings_members (meetingID, memberID)
    VALUES ('3', '2');
INSERT INTO meetings_members (meetingID, memberID)
    VALUES ('4', '1');
INSERT INTO meetings_members (meetingID, memberID)
    VALUES ('4', '4');

