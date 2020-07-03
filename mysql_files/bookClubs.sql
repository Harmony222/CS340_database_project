CREATE TABLE `bookclubs` (
    `bookClubID` int(11) NOT NULL AUTO_INCREMENT,
    `clubName` varchar(255) NOT NULL,
    `meetingFrequency` int(11) DEFAULT NULL,
    `clubGenre` int(11) NOT NULL,
    `clubLeader` int(11) DEFAULT NULL,
    PRIMARY KEY (`bookClubID`)
) ENGINE=InnoDB;

