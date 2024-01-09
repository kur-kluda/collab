SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gp`
--

-- 
-- ---------------------------------------
CREATE TABLE `s_7` (
  `time` datetime NOT NULL,
  `rcv` datetime NOT NULL,
  `1` float NOT NULL,
  `2` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `s_7`
  ADD KEY `time_index` (`time`);


-- ---------------------------------------
CREATE TABLE `s_8` (
  `time` datetime NOT NULL,
  `rcv` datetime NOT NULL,
  `1` float NOT NULL,
  `2` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `s_8`
  ADD KEY `time_index` (`time`);


-- ---------------------------------------
CREATE TABLE `s_9` (
  `time` datetime NOT NULL,
  `rcv` datetime NOT NULL,
  `1` float NOT NULL,
  `2` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `s_9`
  ADD KEY `time_index` (`time`);


-- ---------------------------------------
CREATE TABLE `s_10` (
  `time` datetime NOT NULL,
  `rcv` datetime NOT NULL,
  `1` float NOT NULL,
  `2` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `s_10`
  ADD KEY `time_index` (`time`);

-- ---------------------------------------
CREATE TABLE `s_11` (
  `time` datetime NOT NULL,
  `rcv` datetime NOT NULL,
  `1` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `s_11`
  ADD KEY `time_index` (`time`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
