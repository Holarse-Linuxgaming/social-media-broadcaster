-- phpMyAdmin SQL Dump
-- version 4.5.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 20. Mrz 2016 um 22:00
-- Server-Version: 10.1.12-MariaDB
-- PHP-Version: 7.0.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `socialmediabroadcaster`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `broadcast`
--

CREATE TABLE `broadcast` (
  `id` bigint(20) NOT NULL,
  `id_modules` bigint(20) NOT NULL,
  `id_social` bigint(20) NOT NULL,
  `id_reference_modules` bigint(20) NOT NULL,
  `id_reference_social` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `modules`
--

CREATE TABLE `modules` (
  `id` bigint(20) NOT NULL,
  `table` text,
  `enabled` int(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `modules`
--

INSERT INTO `modules` (`id`, `table`, `enabled`) VALUES
(1, 'rss_holarse', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `rss_holarse`
--

CREATE TABLE `rss_holarse` (
  `id` bigint(20) NOT NULL,
  `title` text,
  `url` text,
  `time` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `social`
--

CREATE TABLE `social` (
  `id` bigint(20) NOT NULL,
  `table` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `social`
--

INSERT INTO `social` (`id`, `table`) VALUES
(1, 'social_twitter'),
(2, 'social_gnusocial');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `social_gnusocial`
--

CREATE TABLE `social_gnusocial` (
  `id` bigint(20) NOT NULL,
  `message` text NOT NULL,
  `time` datetime NOT NULL,
  `url` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `social_twitter`
--

CREATE TABLE `social_twitter` (
  `id` bigint(20) NOT NULL,
  `message` text NOT NULL,
  `time` datetime NOT NULL,
  `url` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `broadcast`
--
ALTER TABLE `broadcast`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indizes für die Tabelle `modules`
--
ALTER TABLE `modules`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indizes für die Tabelle `rss_holarse`
--
ALTER TABLE `rss_holarse`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indizes für die Tabelle `social`
--
ALTER TABLE `social`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indizes für die Tabelle `social_gnusocial`
--
ALTER TABLE `social_gnusocial`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indizes für die Tabelle `social_twitter`
--
ALTER TABLE `social_twitter`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `broadcast`
--
ALTER TABLE `broadcast`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT für Tabelle `modules`
--
ALTER TABLE `modules`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT für Tabelle `rss_holarse`
--
ALTER TABLE `rss_holarse`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT für Tabelle `social`
--
ALTER TABLE `social`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT für Tabelle `social_gnusocial`
--
ALTER TABLE `social_gnusocial`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
--
-- AUTO_INCREMENT für Tabelle `social_twitter`
--
ALTER TABLE `social_twitter`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
