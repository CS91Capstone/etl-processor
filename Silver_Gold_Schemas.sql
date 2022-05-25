CREATE TABLE `Campsites` (
  `campsite_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `facility_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `campsite_name` varchar(100) NOT NULL,
  `campsite_type` varchar(100) NOT NULL,
  `type_of_use` varchar(100) NOT NULL,
  `campsite_accessible` varchar(100) NOT NULL,
  `campsite_reservable` varchar(100) NOT NULL,
  `campsite_longitude` varchar(100) NOT NULL,
  `campsite_latitude` varchar(100) NOT NULL,
  PRIMARY KEY (`campsite_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Campsites_Access` (
  `campsite_id` varchar(100) NOT NULL,
  `campsite_accessible` varchar(100) DEFAULT NULL,
  `campsite_reservable` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Campsites_Coordinates` (
  `campsite_id` varchar(100) NOT NULL,
  `campsite_longitude` varchar(100) DEFAULT NULL,
  `campsite_latitude` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Campsites_Location` (
  `campsite_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `campsite_country` varchar(100) DEFAULT NULL,
  `campsite_state` varchar(100) DEFAULT NULL,
  `campsite_city` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Campsites_Name` (
  `campsite_id` varchar(100) NOT NULL,
  `facility_id` varchar(100) DEFAULT NULL,
  `campsite_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `Campsites_Type` (
  `campsite_id` varchar(100) NOT NULL,
  `campsite_type` varchar(100) DEFAULT NULL,
  `type_of_use` varchar(100) DEFAULT NULL,
  KEY `campsite_id` (`campsite_id`),
  CONSTRAINT `Campsites_Type_ibfk_1` FOREIGN KEY (`campsite_id`) REFERENCES `Campsites` (`campsite_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci