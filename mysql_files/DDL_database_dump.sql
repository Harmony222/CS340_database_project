-- MariaDB dump 10.17  Distrib 10.4.11-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_scarleth
-- ------------------------------------------------------
-- Server version	10.4.13-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `BookClubs`
--

DROP TABLE IF EXISTS `BookClubs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BookClubs` (
  `bookClubID` int(11) NOT NULL AUTO_INCREMENT,
  `clubName` varchar(255) NOT NULL,
  `meetingFrequency` varchar(255) DEFAULT NULL,
  `clubGenreID` int(11) NOT NULL,
  `clubLeaderID` int(11) NOT NULL,
  PRIMARY KEY (`bookClubID`),
  UNIQUE KEY `clubName` (`clubName`),
  KEY `clubGenreID` (`clubGenreID`),
  KEY `clubLeaderID` (`clubLeaderID`),
  CONSTRAINT `BookClubs_ibfk_1` FOREIGN KEY (`clubGenreID`) REFERENCES `Genres` (`genreID`),
  CONSTRAINT `BookClubs_ibfk_2` FOREIGN KEY (`clubLeaderID`) REFERENCES `Members` (`memberID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BookClubs`
--

LOCK TABLES `BookClubs` WRITE;
/*!40000 ALTER TABLE `BookClubs` DISABLE KEYS */;
INSERT INTO `BookClubs` VALUES (1,'But I Progress Book Club','monthly',6,4),(2,'The Book Was Better','twice monthly',3,6),(3,'Get Lit Book Club','monthly',1,5),(4,'Beyond Words Book Club','weekly',8,7),(5,'Summer Book Club','twice monthly',5,10);
/*!40000 ALTER TABLE `BookClubs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Books`
--

DROP TABLE IF EXISTS `Books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Books` (
  `bookID` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `bookGenreID` int(11) NOT NULL,
  PRIMARY KEY (`bookID`),
  UNIQUE KEY `book_info` (`title`,`author`,`bookGenreID`),
  KEY `bookGenreID` (`bookGenreID`),
  CONSTRAINT `Books_ibfk_1` FOREIGN KEY (`bookGenreID`) REFERENCES `Genres` (`genreID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Books`
--

LOCK TABLES `Books` WRITE;
/*!40000 ALTER TABLE `Books` DISABLE KEYS */;
INSERT INTO `Books` VALUES (5,'A Farewell to Arms','Ernest Hemingway',1),(7,'Crime and Punishment','Fyodor Dostoevsky',1),(1,'Florida','Lauren Groff',6),(18,'Four Quartets','T.S. Eliot',8),(10,'Murder at the Vicarage','Agatha Christie',3),(2,'Nine Stories','J.D. Salinger',6),(16,'Owls and Other Fantasies: Poems and Essays','Mary Oliver',8),(6,'Pride and Prejudice','Jane Austen',1),(12,'Still Life','Louise Penny',3),(3,'Stone Mattress','Margaret Atwood',6),(17,'The Dream of a Common Language: Poems 1974-1977','Adrienne Rich',8),(11,'The Girl With the Dragon Tattoo','Stieg Larsson',3),(8,'The Grapes of Wrath','John Steinbeck',1),(13,'The Great Influenza: The Story of the Deadliest Pandemic in History','John M. Barry',5),(15,'The Poems of Robert Frost: Poetry for the Ages','Robert Frost',8),(9,'The Stranger','Albert Camus',1),(14,'This Republic of Suffering: Death and the American Civil War','Drew Gilpin Faust',5),(4,'Trigger Warning','Neil Gaiman',6);
/*!40000 ALTER TABLE `Books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ClubMeetings`
--

DROP TABLE IF EXISTS `ClubMeetings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ClubMeetings` (
  `meetingID` int(11) NOT NULL AUTO_INCREMENT,
  `dateTime` datetime NOT NULL,
  `bookClubID` int(11) NOT NULL,
  `meetingBookID` int(11) DEFAULT NULL,
  `meetingLeaderID` int(11) NOT NULL,
  PRIMARY KEY (`meetingID`),
  UNIQUE KEY `meetingBookID` (`meetingBookID`),
  KEY `meetingLeaderID` (`meetingLeaderID`),
  KEY `bookClubID` (`bookClubID`),
  CONSTRAINT `ClubMeetings_ibfk_1` FOREIGN KEY (`meetingBookID`) REFERENCES `Books` (`bookID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `ClubMeetings_ibfk_2` FOREIGN KEY (`meetingLeaderID`) REFERENCES `Members` (`memberID`),
  CONSTRAINT `ClubMeetings_ibfk_3` FOREIGN KEY (`bookClubID`) REFERENCES `BookClubs` (`bookClubID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ClubMeetings`
--

LOCK TABLES `ClubMeetings` WRITE;
/*!40000 ALTER TABLE `ClubMeetings` DISABLE KEYS */;
INSERT INTO `ClubMeetings` VALUES (1,'2020-06-20 19:30:00',1,3,4),(2,'2020-09-20 19:30:00',1,2,1),(3,'2020-08-20 19:30:00',1,1,2),(4,'2020-08-25 17:00:00',4,17,7),(5,'2020-08-27 18:00:00',3,5,3),(6,'2020-09-24 18:00:00',3,9,8);
/*!40000 ALTER TABLE `ClubMeetings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Genres`
--

DROP TABLE IF EXISTS `Genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Genres` (
  `genreID` int(11) NOT NULL AUTO_INCREMENT,
  `genre` varchar(255) NOT NULL,
  PRIMARY KEY (`genreID`),
  UNIQUE KEY `genre` (`genre`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Genres`
--

LOCK TABLES `Genres` WRITE;
/*!40000 ALTER TABLE `Genres` DISABLE KEYS */;
INSERT INTO `Genres` VALUES (7,'biography'),(9,'children'),(1,'classic'),(2,'graphic novel'),(5,'history'),(3,'mystery'),(8,'poetry'),(4,'science fiction'),(6,'short story');
/*!40000 ALTER TABLE `Genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Members`
--

DROP TABLE IF EXISTS `Members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Members` (
  `memberID` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`memberID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Members`
--

LOCK TABLES `Members` WRITE;
/*!40000 ALTER TABLE `Members` DISABLE KEYS */;
INSERT INTO `Members` VALUES (1,'Inigo','Montoya','inigo.montoya@florian.com'),(2,'Jay','Gatsby','jgats@westegg.org'),(3,'Veruca','Salt','veruca.salt@wonka.edu'),(4,'Atticus','Finch','attifinch@maycomb.com'),(5,'Hester','Prynne','h.prynne@pearl.edu'),(6,'John','Watson','watsonj@bakerst.net'),(7,'Annabel','Lee','ann.lee@poe.org'),(8,'Elizabeth','Bennet','lizzyb@longbourn.net'),(9,'Lyra','Belacqua','lyra@oxford.edu'),(10,'Ada','Lovelace','adalove@ae.org'),(11,'Charlie','Marlow','charlie.marlow@congo.com'),(12,'Molly','Bloom','mbloom@dublin.org');
/*!40000 ALTER TABLE `Members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meetings_members`
--

DROP TABLE IF EXISTS `meetings_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meetings_members` (
  `meetingID` int(11) NOT NULL,
  `memberID` int(11) NOT NULL,
  PRIMARY KEY (`meetingID`,`memberID`),
  KEY `memberID` (`memberID`),
  CONSTRAINT `meetings_members_ibfk_1` FOREIGN KEY (`meetingID`) REFERENCES `ClubMeetings` (`meetingID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `meetings_members_ibfk_2` FOREIGN KEY (`memberID`) REFERENCES `Members` (`memberID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings_members`
--

LOCK TABLES `meetings_members` WRITE;
/*!40000 ALTER TABLE `meetings_members` DISABLE KEYS */;
INSERT INTO `meetings_members` VALUES (1,4),(2,1),(3,1),(3,2),(4,1),(4,4),(4,7),(5,3),(6,8);
/*!40000 ALTER TABLE `meetings_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookclubs_members`
--

DROP TABLE IF EXISTS `bookclubs_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bookclubs_members` (
  `memberID` int(11) NOT NULL,
  `bookClubID` int(11) NOT NULL,
  PRIMARY KEY (`memberID`,`bookClubID`),
  KEY `bookClubID` (`bookClubID`),
  CONSTRAINT `bookclubs_members_ibfk_1` FOREIGN KEY (`memberID`) REFERENCES `Members` (`memberID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `bookclubs_members_ibfk_2` FOREIGN KEY (`bookClubID`) REFERENCES `BookClubs` (`bookClubID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookclubs_members`
--

LOCK TABLES `bookclubs_members` WRITE;
/*!40000 ALTER TABLE `bookclubs_members` DISABLE KEYS */;
INSERT INTO `bookclubs_members` VALUES (4,1),(5,3),(6,2),(7,4),(10,5);
/*!40000 ALTER TABLE `bookclubs_members` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-11 17:47:42
