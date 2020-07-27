DROP TABLE IF EXISTS meetings_members;
DROP TABLE IF EXISTS bookclubs_members;
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
    VALUES ('Inigo', 'Montoya', 'inigo.montoya@florian.com'),
           ('Jay', 'Gatsby', 'jgats@westegg.org'),
           ('Veruca', 'Salt', 'veruca.salt@wonka.edu'),
           ('Atticus', 'Finch', 'attifinch@maycomb.com'),
           ('Hester', 'Prynne', 'h.prynne@pearl.edu'),
           ('John', 'Watson', 'watsonj@bakerst.net'),
           ('Annabel', 'Lee', 'ann.lee@poe.org'),
           ('Elizabeth', 'Bennet', 'lizzyb@longbourn.net'),
           ('Lyra', 'Belacqua', 'lyra@oxford.edu'),
           ('Ada', 'Lovelace', 'adalove@ae.org'),
           ('Charlie', 'Marlow', 'charlie.marlow@congo.com'),
           ('Molly', 'Bloom', 'mbloom@dublin.org');

CREATE TABLE Genres (
    genreID int(11) NOT NULL AUTO_INCREMENT,
    genre varchar(255) UNIQUE NOT NULL,
    PRIMARY KEY (genreID)
);

INSERT INTO Genres (genre) VALUES ('classic'),
                                  ('graphic novel'),
                                  ('mystery'),
                                  ('science fiction'),
                                  ('history'),
                                  ('short story'),
                                  ('biography'),
                                  ('poetry'),
                                  ('children');


CREATE TABLE BookClubs (
    bookClubID int(11) NOT NULL AUTO_INCREMENT,
    clubName varchar(255) NOT NULL UNIQUE,
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
            (SELECT memberID FROM Members WHERE email = 'attifinch@maycomb.com')),
            ('The Book Was Better',
            'twice monthly',
            (SELECT genreID FROM Genres WHERE genre = 'mystery'),
            (SELECT memberID FROM Members WHERE email = 'watsonj@bakerst.net')),
            ('Get Lit Book Club', 
            'monthly',
            (SELECT genreID FROM Genres WHERE genre = 'classic'),
            (SELECT memberID FROM Members WHERE email = 'h.prynne@pearl.edu')),
            ('Beyond Words Book Club',
            'weekly',
            (SELECT genreID FROM Genres WHERE genre = 'poetry'),
            (SELECT memberID FROM Members WHERE email = 'ann.lee@poe.org')),
            ('Summer Book Club',
            'twice monthly',
            (SELECT genreID FROM Genres WHERE genre = 'history'),
            (SELECT memberID FROM Members WHERE email = 'adalove@ae.org'));

CREATE TABLE Books (
    bookID int(11) NOT NULL AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    author varchar(255) NOT NULL,
    bookGenreID int(11) NOT NULL,
    PRIMARY KEY (bookID),
    FOREIGN KEY (bookGenreID)
        REFERENCES Genres(genreID),
    CONSTRAINT `book_info` UNIQUE (`title`, `author`, `bookGenreID`)
);

INSERT INTO Books (title, author, bookGenreID)
    VALUES ('Florida', 
            'Lauren Groff', 
            (SELECT genreID FROM Genres WHERE genre = 'short story')),
            ('Nine Stories',
            'J.D. Salinger',
            (SELECT genreID FROM Genres WHERE genre = 'short story')),
            ('Stone Mattress',
            'Margaret Atwood',
            (SELECT genreID FROM Genres WHERE genre = 'short story')),
            ('Trigger Warning',
            'Neil Gaiman',
            (SELECT genreID FROM Genres WHERE genre = 'short story')),
            ('A Farewell to Arms',
            'Ernest Hemingway',
            (SELECT genreID FROM Genres WHERE genre = 'classic')),
            ('Pride and Prejudice',
            'Jane Austen',
            (SELECT genreID FROM Genres WHERE genre = 'classic')),
            ('Crime and Punishment',
            'Fyodor Dostoevsky',
            (SELECT genreID FROM Genres WHERE genre = 'classic')),
            ('The Grapes of Wrath',
            'John Steinbeck',
            (SELECT genreID FROM Genres WHERE genre = 'classic')),
            ('The Stranger',
            'Albert Camus',
            (SELECT genreID FROM Genres WHERE genre = 'classic')),
            ('Murder at the Vicarage',
            'Agatha Christie',
            (SELECT genreID FROM Genres WHERE genre = 'mystery')),
            ('The Girl With the Dragon Tattoo',
            'Stieg Larsson',
            (SELECT genreID FROM Genres WHERE genre = 'mystery')),
            ('Still Life',
            'Louise Penny',
            (SELECT genreID FROM Genres WHERE genre = 'mystery')),
            ('The Great Influenza: The Story of the Deadliest Pandemic in History',
            'John M. Barry',
            (SELECT genreID FROM Genres WHERE genre = 'history')),
            ('This Republic of Suffering: Death and the American Civil War',
            'Drew Gilpin Faust',
            (SELECT genreID FROM Genres WHERE genre = 'history')),
            ('The Poems of Robert Frost: Poetry for the Ages',
            'Robert Frost',
            (SELECT genreID FROM Genres WHERE genre = 'poetry')),
            ('Owls and Other Fantasies: Poems and Essays',
            'Mary Oliver',
            (SELECT genreID FROM Genres WHERE genre = 'poetry')),
            ('The Dream of a Common Language: Poems 1974-1977',
            'Adrienne Rich',
            (SELECT genreID FROM Genres WHERE genre = 'poetry')),
            ('Four Quartets',
            'T.S. Eliot',
            (SELECT genreID FROM Genres WHERE genre = 'poetry'));


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
            (SELECT memberID FROM Members WHERE email = 'attifinch@maycomb.com')),
            ('2020-09-20 19:30',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'But I Progress Book Club'),
            (SELECT bookID FROM Books WHERE title = 'Nine Stories'),
            (SELECT memberID FROM Members WHERE email = 'inigo.montoya@florian.com')),
            ('2020-08-20 19:30',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'But I Progress Book Club'),
            (SELECT bookID FROM Books WHERE title = 'Florida'),
            (SELECT memberID FROM Members WHERE email = 'jgats@westegg.org')),
            ('2020-08-25 17:00',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'Beyond Words Book Club'),
            (SELECT bookID FROM Books WHERE title = 'The Dream of a Common Language: Poems 1974-1977'),
            (SELECT memberID FROM Members WHERE email = 'ann.lee@poe.org')),
            ('2020-8-27 18:00',
            (SELECT bookClubID FROM BookClubs WHERE clubName = 'Get Lit Book Club'),
            (SELECT bookID FROM Books WHERE title = 'A Farewell to Arms'),
            (SELECT memberID FROM Members WHERE email = 'veruca.salt@wonka.edu')),
            ('2020-9-24 18:00',
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
    VALUES  ('3', '1'),
            ('3', '2'),
            ('4', '1'),
            ('4', '4');

CREATE TABLE bookclubs_members (
    memberID int(11) NOT NULL,
    bookClubID int(11) NOT NULL,
    PRIMARY KEY (memberID, bookClubID),
    FOREIGN KEY (memberID)
        REFERENCES Members(memberID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (bookClubID)
        REFERENCES BookClubs(bookClubID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO bookclubs_members (memberID, bookClubID)
    VALUES  (4,1),
            (6,2), 
            (5,3), 
            (7,4), 
            (10,5);
          


