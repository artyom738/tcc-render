-- db/install.sql
-- DDL для развёртывания базы данных проекта tcc-render (MySQL / MariaDB)

CREATE DATABASE IF NOT EXISTS `tcc_render` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
USE `tcc_render`;

-- Таблица чарта
CREATE TABLE IF NOT EXISTS `charts` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `CHART_TYPE` VARCHAR(50) NOT NULL,
  `CHART_NUMBER` INT DEFAULT 0,
  `CHART_DATE` DATE DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `uk_chart_type_date` (`CHART_TYPE`, `CHART_DATE`),
  KEY `idx_chart_type` (`CHART_TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Таблица песен
CREATE TABLE IF NOT EXISTS `songs` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `EP_ID` VARCHAR(255) DEFAULT NULL,
  `ORIGINAL_ID` INT DEFAULT NULL,
  `AUTHORS` VARCHAR(512) NOT NULL,
  `NAME` VARCHAR(512) NOT NULL,
  `CLIP_PATH` VARCHAR(255) DEFAULT NULL,
  `CLIP_START_SEC` VARCHAR(255) DEFAULT NULL,
  `CLIP_END_SEC` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_ep_id` (`EP_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Позиции в чарте
CREATE TABLE IF NOT EXISTS `chart_positions` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `CHART_ID` INT NOT NULL,
  `SONG_ID` INT NOT NULL,
  `POSITION` INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `uk_chart_position` (`CHART_ID`, `POSITION`),
  KEY `idx_chart_id` (`CHART_ID`),
  KEY `idx_song_id` (`SONG_ID`),
  CONSTRAINT `fk_cp_chart` FOREIGN KEY (`CHART_ID`) REFERENCES `charts`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cp_song` FOREIGN KEY (`SONG_ID`) REFERENCES `songs`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Рубрики чарта
CREATE TABLE IF NOT EXISTS `chart_rubrics` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `CHART_ID` INT NOT NULL,
  `SONG_ID` INT NOT NULL,
  `RUBRIC_TYPE` CHAR(1) NOT NULL,
  `CHART_TYPE` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_cr_chart` (`CHART_ID`),
  KEY `idx_cr_song` (`SONG_ID`),
  CONSTRAINT `fk_cr_chart` FOREIGN KEY (`CHART_ID`) REFERENCES `charts`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cr_song` FOREIGN KEY (`SONG_ID`) REFERENCES `songs`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Дополнительно: рекомендуемые права/параметры
-- Пользователь проекта должен иметь права на CREATE, SELECT, INSERT, UPDATE, DELETE, ALTER для БД `tcc_render`.

-- Конец файла

