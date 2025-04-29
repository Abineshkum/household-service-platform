-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 12, 2024 at 06:03 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `household_service`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `rdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `name`, `mobile`, `email`, `address`, `city`, `uname`, `pass`, `rdate`) VALUES
(1, 'Ram', 9894918800, 'ram@gmail.com', '33,ss', 'Trichy', 'ram', '1234', '08-06-2022');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `service_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `service_name`) VALUES
(1, 'Painting Service'),
(2, 'Electrical Service');

-- --------------------------------------------------------

--
-- Table structure for table `service_booking`
--

CREATE TABLE `service_booking` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `sname` varchar(20) NOT NULL,
  `service` varchar(30) NOT NULL,
  `sdate` varchar(20) NOT NULL,
  `stime` varchar(20) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `service_booking`
--

INSERT INTO `service_booking` (`id`, `uname`, `sname`, `service`, `sdate`, `stime`, `rdate`, `status`) VALUES
(1, 'ram', 'dinesh', 'Painting Service', '2022-06-15', '10am', '12-06-2022', 2),
(2, 'ram', 'dinesh', 'Painting Service', '2022-06-14', '3pm', '12-06-2022', 0),
(3, 'ram', 'dinesh', 'Painting Service', '2022-06-13', '10am', '12-06-2022', 0);

-- --------------------------------------------------------

--
-- Table structure for table `service_provider`
--

CREATE TABLE `service_provider` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `service_name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `available_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `service_provider`
--

INSERT INTO `service_provider` (`id`, `name`, `service_name`, `mobile`, `email`, `location`, `city`, `latitude`, `longitude`, `uname`, `pass`, `status`, `rdate`, `available_st`) VALUES
(1, 'Dinesh', 'Painting Service', 9973471112, 'ram@gmail.com', 'SS Nagar', 'Trichy', '', '', 'dinesh', '1234', 1, '08-06-2022', 0),
(2, 'Suresh', 'Electrical Service', 9054621096, 'suresh@gmail.com', 'DD Nagar', 'Dindigul', '', '', 'suresh', '1234', 1, '08-06-2022', 0),
(3, 'Giri', 'Painting Service', 9054621096, 'giri@gmail.com', 'Anna nagar', 'Trichy', '', '', 'giri', '1234', 1, '12-06-2022', 0);

-- --------------------------------------------------------

--
-- Table structure for table `service_review`
--

CREATE TABLE `service_review` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `sname` varchar(20) NOT NULL,
  `review` varchar(100) NOT NULL,
  `rdate` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `service_review`
--

INSERT INTO `service_review` (`id`, `uname`, `sname`, `review`, `rdate`) VALUES
(1, 'ram', 'dinesh', 'good service', '12-06-2022');
