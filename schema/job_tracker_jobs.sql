-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: job_tracker
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `job_title` varchar(100) NOT NULL,
  `job_description` text,
  `salary_min` decimal(10,2) DEFAULT NULL,
  `salary_max` decimal(10,2) DEFAULT NULL,
  `job_type` varchar(20) DEFAULT NULL,
  `posting_url` varchar(500) DEFAULT NULL,
  `date_posted` date DEFAULT NULL,
  `requirements` json DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`job_id`),
  KEY `idx_job_title` (`job_title`),
  KEY `idx_salary` (`salary_min`),
  KEY `idx_company_type` (`company_id`,`job_type`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,1,'Software Developer',NULL,70000.00,90000.00,'Full-time',NULL,'2025-01-15','[\"Python\", \"SQL\", \"Flask\"]',1,'2026-01-30 04:02:26'),(2,1,'Database Administrator',NULL,75000.00,95000.00,'Full-time',NULL,'2025-01-10',NULL,1,'2026-01-30 04:02:26'),(3,2,'Data Analyst',NULL,65000.00,85000.00,'Full-time',NULL,'2025-01-12','[\"Python\", \"SQL\", \"JavaScript\"]',1,'2026-01-30 04:02:26'),(4,3,'Cloud Engineer',NULL,80000.00,100000.00,'Full-time',NULL,'2025-01-08','[\"AWS\", \"Docker\", \"Kubernetes\"]',1,'2026-01-30 04:02:26'),(5,4,'Junior Developer',NULL,55000.00,70000.00,'Full-time',NULL,'2025-01-14',NULL,1,'2026-01-30 04:02:26'),(6,4,'Senior Developer',NULL,95000.00,120000.00,'Full-time',NULL,'2025-01-14',NULL,1,'2026-01-30 04:02:26'),(7,5,'ML Engineer',NULL,90000.00,115000.00,'Full-time',NULL,'2025-01-11','[\"Python\", \"Machine Learning\", \"SQL\"]',1,'2026-01-30 04:02:26'),(8,1,'QA Engineer',NULL,60000.00,80000.00,'Full-time',NULL,'2025-01-05','[\"Java\", \"Spring\", \"SQL\"]',1,'2026-02-10 23:24:09'),(9,2,'Business Analyst',NULL,65000.00,85000.00,'Full-time',NULL,'2025-01-06',NULL,1,'2026-02-10 23:24:09'),(10,2,'Data Scientist',NULL,85000.00,110000.00,'Full-time',NULL,'2025-01-07',NULL,1,'2026-02-10 23:24:09'),(11,3,'DevOps Engineer',NULL,80000.00,105000.00,'Full-time',NULL,'2025-01-08',NULL,1,'2026-02-10 23:24:09'),(12,3,'Security Analyst',NULL,75000.00,95000.00,'Full-time',NULL,'2025-01-09',NULL,1,'2026-02-10 23:24:09'),(13,4,'UI/UX Designer',NULL,60000.00,80000.00,'Full-time',NULL,'2025-01-10','[\"React\", \"JavaScript\", \"CSS\"]',1,'2026-02-10 23:24:09'),(14,5,'Product Manager',NULL,90000.00,120000.00,'Full-time',NULL,'2025-01-11',NULL,1,'2026-02-10 23:24:09'),(15,1,'Technical Writer',NULL,55000.00,75000.00,'Contract',NULL,'2025-01-12',NULL,1,'2026-02-10 23:24:09'),(16,2,'Intern - Data',NULL,30000.00,40000.00,'Internship',NULL,'2025-01-13',NULL,1,'2026-02-10 23:24:09'),(17,4,'Intern - Development',NULL,32000.00,42000.00,'Internship',NULL,'2025-01-14',NULL,1,'2026-02-10 23:24:09'),(18,7,'Software Architect',NULL,120000.00,150000.00,'Full-time',NULL,NULL,NULL,1,'2026-02-14 01:03:18');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-29 21:53:26
