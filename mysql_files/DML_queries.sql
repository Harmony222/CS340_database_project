-- MEMBERS --------------------------------------------------------------------------




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
        ON b.bookClubID = tmp.bookClubID 

-- Add new book club
INSERT INTO BookClubs (clubName, meetingFrequency, clubGenreID, clubLeaderID)
VALUES (%club_name, %meeting_frequency_dropdown, %genreID_dropdown, %leaderID_from_function_that_validates_email)



-- MEETINGS -------------------------------------------------------------------------
-- Select all future book club meetings
SELECT cm.meetingID, cm.dateTime, b.title, b.author, 
        bc.clubName, m.firstName, m.lastName
FROM ClubMeetings as cm
LEFT JOIN Books as b ON cm.meetingBookID = b.bookID
JOIN Members as m on cm.meetingLeaderID = m.memberID
JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
WHERE cm.dateTime >= CURDATE()
ORDER BY cm.bookClubID, cm.dateTime

-- Schedule a new meeting
INSERT INTO ClubMeetings (`dateTime`, bookClubID, meetingBookID, meetingLeaderID)
VALUES (%dateTime, %clubID_dropdown, %bookID_dropdown, %leaderID_from_function_that_validates_email)

-- Member signup for a meeting
INSERT INTO meetings_members (meetingID, memberID) 
VALUES (%meetingID_dropdown, %memberID_get_from_email)

-- Used to validate member email
SELECT memberID FROM Members WHERE email = %email

-- View attendees
SELECT mm.meetingID, m.memberID, m.firstName, m.lastName, m.email 
FROM Members m
JOIN meetings_members mm ON m.memberID = mm.memberID 
WHERE mm.meetingID = %meetingID_from_get_request

-- Select all meetings for the specified book club
SELECT cm.meetingID, cm.dateTime, b.title, b.author, bc.clubName, m.firstName, m.lastName
FROM ClubMeetings as cm
LEFT JOIN Books as b ON cm.meetingBookID = b.bookID
JOIN Members as m on cm.meetingLeaderID = m.memberID
JOIN BookClubs as bc on cm.bookClubID = bc.bookClubID
WHERE cm.dateTime >= CURDATE() AND cm.bookClubID = %clubID_from_dropdown
ORDER BY cm.bookClubID, cm.dateTime



-- BOOKS ----------------------------------------------------------------------------





-- GENRES ---------------------------------------------------------------------------



-- MISC -----------------------------------------------------------------------------

-- Get genre names - used for dropdown menus
SELECT * FROM Genres ORDER BY genre

-- Get book club names - used for dropdown menus
SELECT bookClubID, clubName FROM BookClubs ORDER BY clubName

-- Get books (title and author) - used for dropdown menus in meeting signup
SELECT b.bookID, b.title, b.author
FROM Books b
WHERE b.bookGenreID = (SELECT bc.clubGenreID 
                        FROM BookClubs bc 
                        WHERE bc.bookClubID = %clubID_from_dropdown)  