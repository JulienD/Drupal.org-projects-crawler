-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le : Ven 18 Avril 2014 à 13:34
-- Version du serveur: 5.5.35
-- Version de PHP: 5.3.10-1ubuntu3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: `drupal_projects`
--

-- --------------------------------------------------------

--
-- Structure de la table `maintainers`
--

CREATE TABLE IF NOT EXISTS `maintainers` (
  `maintainer_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `profile_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `projects`
--

CREATE TABLE IF NOT EXISTS `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `url` tinytext NOT NULL,
  `git_url` tinytext NOT NULL,
  `last_commit` varchar(100) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9423 ;

-- --------------------------------------------------------

--
-- Structure de la table `releases`
--

CREATE TABLE IF NOT EXISTS `releases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `version` varchar(50) DEFAULT NULL,
  `tag` varchar(50) DEFAULT NULL,
  `date` timestamp NULL DEFAULT NULL,
  `version_major` int(10) DEFAULT NULL,
  `version_patch` int(10) DEFAULT NULL,
  `version_extra` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`date`),
  KEY `project_id` (`project_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=35826 ;

-- --------------------------------------------------------

--
-- Structure de la table `statistics`
--

CREATE TABLE IF NOT EXISTS `statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `opened_issues` int(11) DEFAULT NULL,
  `total_issues` int(11) DEFAULT NULL,
  `opened_bugs` int(11) DEFAULT NULL,
  `total_bugs` int(11) DEFAULT NULL,
  `downloads` int(11) DEFAULT NULL,
  `installs` int(11) DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`opened_issues`,`total_issues`,`opened_bugs`,`total_bugs`,`downloads`,`installs`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9418 ;

-- --------------------------------------------------------

--
-- Structure de la table `versions`
--

CREATE TABLE IF NOT EXISTS `versions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `api_version` varchar(5) NOT NULL,
  `recommended_major` int(11) NOT NULL,
  `supported_majors` int(11) NOT NULL,
  `default_major` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`api_version`,`recommended_major`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10144 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
