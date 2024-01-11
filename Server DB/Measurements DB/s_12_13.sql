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

-- --------------------------------------------------------

--
-- Table structure for table `s_12`
--

CREATE TABLE `s_12` (
  `time` datetime NOT NULL,
  `rcv` datetime NOT NULL,
  `1` float NOT NULL,
  `2` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; /*'ENGINE=InnoDB' - Norāda tabulas storage engine (Tā ir pamatā esošās programmatūras komponente, ko datu bāzes pārvaldības sistēma (DBVS) izmanto, lai izveidotu, lasītu, atjauninātu un dzēstu (CRUD) datus no datu bāzes.).
                                                                      'DEFAULT CHARSET=utf8mb4' - Definē tabulas noklusējuma rakstzīmju kopu. Šajā gadījumā rakstzīmju kopa ir iestatīta uz utf8mb4, ko parasti izmanto, lai atbalstītu plašāku unikoda rakstzīmju klāstu.
                                                                      'COLLATE=utf8mb4_0900_ai_ci' - Norāda rakstzīmju kopas salīdzināšanu. Salīdzināšana nosaka rakstzīmju salīdzināšanas un šķirošanas noteikumus. Šajā gadījumā utf8mb4_0900_ai_ci apzīmē "utf8mb4" ar versiju "0900" (Unicode version 9.0) un "ai_ci" ( "accent-insensitive" and "case-insensitive") salīdzinājumu.*/
--
-- Indexes for dumped tables
--

--
-- Indexes for table `s_12`
--
ALTER TABLE `s_12`
  ADD KEY `time_index` (`time`);


CREATE TABLE `s_13` (
  `time` datetime NOT NULL,
  `rcv` datetime NOT NULL,
  `1` float NOT NULL,
  `2` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; /*'ENGINE=InnoDB' - Norāda tabulas storage engine (Tā ir pamatā esošās programmatūras komponente, ko datu bāzes pārvaldības sistēma (DBVS) izmanto, lai izveidotu, lasītu, atjauninātu un dzēstu (CRUD) datus no datu bāzes.).
                                                                      'DEFAULT CHARSET=utf8mb4' - Definē tabulas noklusējuma rakstzīmju kopu. Šajā gadījumā rakstzīmju kopa ir iestatīta uz utf8mb4, ko parasti izmanto, lai atbalstītu plašāku unikoda rakstzīmju klāstu.
                                                                      'COLLATE=utf8mb4_0900_ai_ci' - Norāda rakstzīmju kopas salīdzināšanu. Salīdzināšana nosaka rakstzīmju salīdzināšanas un šķirošanas noteikumus. Šajā gadījumā utf8mb4_0900_ai_ci apzīmē "utf8mb4" ar versiju "0900" (Unicode version 9.0) un "ai_ci" ( "accent-insensitive" and "case-insensitive") salīdzinājumu.*/
--
-- Indexes for dumped tables
--

--
-- Indexes for table `s_13`
--
ALTER TABLE `s_13`
  ADD KEY `time_index` (`time`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
