CREATE DATABASE  IF NOT EXISTS `fiperobot` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci */;
USE `fiperobot`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `TabelaReferencia`;
CREATE TABLE `TabelaReferencia` (
  `codigoTabelaReferencia` int(11) NOT NULL DEFAULT '0',
  `codigoTipoVeiculo` int(11) NOT NULL DEFAULT '0',
  `titulo` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `hasCrawled` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codigoTabelaReferencia`,`codigoTipoVeiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
ALTER TABLE `TabelaReferencia` ADD INDEX (`hasCrawled`) using HASH;

DROP TABLE IF EXISTS `Marca`;
CREATE TABLE `Marca` (
  `codigoMarca` int(11) NOT NULL DEFAULT '0',
  `codigoTipoVeiculo` int(11) NOT NULL DEFAULT '0',
  `codigoTabelaReferencia` int(11) NOT NULL DEFAULT '0',
  `titulo` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `hasCrawled` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codigoMarca`,`codigoTipoVeiculo`,`codigoTabelaReferencia`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
ALTER TABLE `Marca` ADD INDEX (`hasCrawled`) using HASH;
ALTER TABLE `Marca` ADD INDEX `search` (`codigoTipoVeiculo` ASC, `codigoTabelaReferencia` ASC);

DROP TABLE IF EXISTS `Modelo`;
CREATE TABLE `Modelo` (
  `codigoModelo` int(11) NOT NULL DEFAULT '0',
  `codigoMarca` int(11) NOT NULL DEFAULT '0',
  `codigoTipoVeiculo` int(11) NOT NULL DEFAULT '0',
  `codigoTabelaReferencia` int(11) NOT NULL DEFAULT '0',
  `titulo` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `hasCrawled` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codigoModelo`,`codigoMarca`,`codigoTipoVeiculo`,`codigoTabelaReferencia`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
ALTER TABLE `Modelo` ADD INDEX (`hasCrawled`) using HASH;
ALTER TABLE `Modelo` ADD INDEX `search` (`codigoTipoVeiculo` ASC, `codigoTabelaReferencia` ASC, `codigoMarca` ASC);

DROP TABLE IF EXISTS `AnoModelo`;
CREATE TABLE `AnoModelo` (
  `codigoAnoModelo` varchar(255) NOT NULL DEFAULT '',
  `codigoModelo` int(11) NOT NULL DEFAULT '0',
  `codigoMarca` int(11) NOT NULL DEFAULT '0',
  `codigoTipoVeiculo` int(11) NOT NULL DEFAULT '0',
  `codigoTabelaReferencia` int(11) NOT NULL DEFAULT '0',
  `titulo` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `hasCrawled` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`codigoAnoModelo`,`codigoModelo`,`codigoMarca`,`codigoTipoVeiculo`,`codigoTabelaReferencia`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
ALTER TABLE `AnoModelo` ADD INDEX (`hasCrawled`) using HASH;
ALTER TABLE `AnoModelo` ADD INDEX `search` (`codigoTipoVeiculo` ASC, `codigoTabelaReferencia` ASC, `codigoMarca` ASC, `codigoModelo` ASC);

DROP TABLE IF EXISTS `Versao`;
CREATE TABLE `Versao` (
  `codigoFipe` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `codigoAnoModelo` varchar(255) NOT NULL DEFAULT '',
  `codigoModelo` int(11) NOT NULL DEFAULT '0',
  `codigoMarca` int(11) NOT NULL DEFAULT '0',
  `codigoTipoVeiculo` int(11) NOT NULL DEFAULT '0',
  `codigoTabelaReferencia` int(11) NOT NULL DEFAULT '0',
  `valor` decimal(12,2) COLLATE latin1_general_ci DEFAULT '0.00',
  `titulo` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`codigoFipe`,`codigoAnoModelo`,`codigoModelo`,`codigoMarca`,`codigoTipoVeiculo`,`codigoTabelaReferencia`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
ALTER TABLE `Versao` ADD INDEX `search` (`codigoTipoVeiculo` ASC, `codigoTabelaReferencia` ASC, `codigoMarca` ASC, `codigoModelo` ASC, `codigoAnoModelo` ASC);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;