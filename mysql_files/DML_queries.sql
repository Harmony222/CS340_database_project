-- Note: The modulo operator, %, is used here to denote variables
--       holding data from the front-end

-- MEMBERS --------------------------------------------------------------------------
-- Select all members
SELECT * FROM Members;

-- Add a new member
INSERT INTO Members (firstName, lastName, email)
VALUES (%firstName_input, %lastName_input, %email_input);


-- BOOKCLUBS ------------------------------------------------------------------------
-- Select all book clubs plus the next book club meeting date
SELECT b.bookClubID, b.clubName, b.meetingFrequency, 
        g.genre, m.firstName, m.lastName, tmp.nextMeeting
FROM BookClubs as b
JOIN Genres as g ON b.clubGenreID = g.genreID
JOIN Members as m ON b.clubLeaderID = m.memberID
LEFT JOIN (
        SELECT tmp.bookClubID, MIN(tmp.dateTime) as nextMeeting
        FROM (SELECT cm2.bookClubID, cm2.dateTime
                FROM ClubMeetings as cm2
                WHERE cm2.dateTime > CURDATE()) as tmp
                GROUP BY tmp.bookClubID) as tmp 
        ON b.bookClubID = tmp.bookClubID;

-- Add new book club
INSERT INTO BookClubs (clubName, meetingFrequency, clubGenreID, clubLeaderID)
VALUES (%club_name, %meeting_frequency_dropdown, %genreID_dropdown, %leaderID_from_function_that_validates_email);

-- View members of a book club
SELECT m.firstName as `First Name`, m.lastName as `Last Name` 
FROM Members as m 
JOIN bookclubs_members as bcm 
ON m.memberID = bcm.memberID 
WHERE bcm.bookClubID = %bookClubID;


-- MEETINGS -------------------------------------------------------------------------
-- Select all future book club meetings
SELECT cm.meetingID, cm.dateTime, b.title, b.author, 
        bc.clubName, m.firstName, m.lastName
FROM ClubMeetings as cm
LEFT JOIN Books as b ON cm.meetingBookID = b.bookID
JOIN Members as m on cm.meetingLeaderID = m.memberID
JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
WHERE cm.dateTime >= CURDATE()
ORDER BY cm.bookClubID, cm.dateTime;

-- Schedule a new meeting
INSERT INTO ClubMeetings (`dateTime`, bookClubID, meetingBookID, meetingLeaderID)
VALUES (%dateTime, %clubID_dropdown, %bookID_dropdown, %leaderID_from_function_that_validates_email);

-- Member signup for a meeting
INSERT INTO meetings_members (meetingID, memberID) 
VALUES (%meetingID_dropdown, %memberID_get_from_email);

-- Used to validate member email
SELECT memberID FROM Members WHERE email = %email;

-- View attendees
SELECT mm.meetingID, m.memberID, m.firstName, m.lastName, m.email 
FROM Members m
JOIN meetings_members mm ON m.memberID = mm.memberID 
WHERE mm.meetingID = %meetingID_from_get_request;

-- Remove attendee from meeting
DELETE FROM meetings_members
WHERE meetingID = %meetingID_from_selection AND memberID = %memberID_from_selection;

-- Select all meetings for the specified book club
SELECT cm.meetingID, cm.dateTime, b.title, b.author, bc.clubName, m.firstName, m.lastName
FROM ClubMeetings as cm
LEFT JOIN Books as b ON cm.meetingBookID = b.bookID
JOIN Members as m on cm.meetingLeaderID = m.memberID
JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
WHERE cm.dateTime >= CURDATE() AND cm.bookClubID = %clubID_from_dropdown
ORDER BY cm.bookClubID, cm.dateTime;

-- Modify club meeting
UPDATE ClubMeetings
SET bookClubID = %bookClubID_dropdown, `dateTime` = %dateTime, meetingBookID = %bookID_dropdown, meetingLeaderID = %leaderID_from_email 
WHERE meetingID = %meetingID_from_selected_row;

-- Delete club meeting
DELETE FROM ClubMeetings
WHERE meetingID = %meetingID_from_selected_row;


-- BOOKS ----------------------------------------------------------------------------
-- Select all books and show the genre name
SELECT b.bookID, b.title, b.author, g.genre
FROM Books AS b
JOIN Genres AS g 
ON b.bookGenreID = g.genreID;

-- Add a new book
INSERT INTO Books (title, author, bookGenreID)
VALUES (%title_input, %author_input, %genreID_dropdown);

-- Delete a book
DELETE from Books WHERE bookID = %bookID_input;


-- GENRES ---------------------------------------------------------------------------
-- Select all genres and order alphabetically
SELECT * FROM Genres ORDER BY genre;

-- Add a new genre
INSERT INTO Genres (genre)
VALUES (%genre_input);



-- MISC -----------------------------------------------------------------------------

-- Get genre names - used for dropdown menus
SELECT * FROM Genres ORDER BY genre;

-- Get book club names - used for dropdown menus
SELECT bookClubID, clubName FROM BookClubs ORDER BY clubName;

-- Get books (title and author) - used for dropdown menu in meeting signup
-- and for dropdown menu in modify meeting. Only retrieves books in the 
-- specified genre and those that are not already assigned to a meeting
SELECT b.bookID, b.title, b.author
FROM Books b
WHERE b.bookID NOT IN (
    SELECT cm.meetingBookID 
    FROM ClubMeetings cm 
    WHERE cm.meetingBookID IS NOT NULL)
AND b.bookGenreID = (
    SELECT bc.clubGenreID 
    FROM BookClubs bc 
    WHERE bc.bookClubID = %bookClubID_dropdown);

-- Get selected book (title and author) - used to get the book info that is 
-- assigned to a particular meeting in order to add to modify drop down menu
SELECT b.bookID, b.title, b.author
FROM Books b
WHERE b.bookID = %bookID_from_selected_meeting;