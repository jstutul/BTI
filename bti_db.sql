-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 11, 2026 at 11:08 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bti_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_balancetransaction`
--

CREATE TABLE `accounts_balancetransaction` (
  `id` bigint(20) NOT NULL,
  `transaction_type` varchar(10) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `note` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_balancetransaction`
--

INSERT INTO `accounts_balancetransaction` (`id`, `transaction_type`, `amount`, `note`, `created_at`, `user_id`) VALUES
(1, 'credit', 499.98, 'DEPOSIT', '2026-05-11 17:37:37.000000', 18);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_certificate`
--

CREATE TABLE `accounts_certificate` (
  `id` bigint(20) NOT NULL,
  `cert_id` varchar(30) NOT NULL,
  `serial_no` varchar(50) NOT NULL,
  `issue_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `result_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_certificate`
--

INSERT INTO `accounts_certificate` (`id`, `cert_id`, `serial_no`, `issue_date`, `created_at`, `result_id`) VALUES
(2, 'BTI-CERT-4K90Q6N2IZ', '509652', '2026-05-07', '2026-05-05 20:28:55.136069', 4),
(3, 'BTI-CERT-1C6O2PHZVW', '872725', '2026-05-28', '2026-05-08 15:40:03.041905', 6);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_course`
--

CREATE TABLE `accounts_course` (
  `id` bigint(20) NOT NULL,
  `name` varchar(500) NOT NULL,
  `duration` varchar(20) NOT NULL,
  `exam_fee` decimal(10,2) NOT NULL,
  `description` varchar(5000) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `cert_type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_course`
--

INSERT INTO `accounts_course` (`id`, `name`, `duration`, `exam_fee`, `description`, `created_at`, `is_active`, `user_id`, `cert_type`) VALUES
(1, 'Computer Basic', '1_year', 150.00, '', '2026-05-02 11:23:17.222070', 1, 4, 'course'),
(2, 'Engine Mechanic', '3_years', 1200.00, '', '2026-05-02 11:23:36.813728', 1, 4, 'it_program'),
(14, 'Graphic Design', '1_year', 200.00, '', '2026-05-03 20:13:23.765350', 1, 4, 'course'),
(15, 'Web Development', '2_years', 2000.00, '', '2026-05-03 20:13:46.971311', 1, 4, 'both'),
(16, 'Electrical Wiring', '1_year', 200.00, '', '2026-05-03 20:14:04.749144', 1, 4, 'course'),
(17, 'Mobile Servicing', '6_months', 250.00, '', '2026-05-03 20:14:23.770894', 1, 4, 'course');

-- --------------------------------------------------------

--
-- Table structure for table `accounts_institution`
--

CREATE TABLE `accounts_institution` (
  `id` bigint(20) NOT NULL,
  `name` varchar(500) NOT NULL,
  `branch_code` varchar(50) NOT NULL,
  `director` varchar(200) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `district` longtext NOT NULL,
  `upazila` longtext NOT NULL,
  `address` longtext NOT NULL,
  `profile_id` bigint(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_institution`
--

INSERT INTO `accounts_institution` (`id`, `name`, `branch_code`, `director`, `mobile`, `email`, `district`, `upazila`, `address`, `profile_id`, `is_active`) VALUES
(16, 'BTI Dhaka Main Campus', 'BR-7421813247', 'Jafor Sadik Tutul', '01817552828', 'jstutul33@gmail.com', 'Dhaka', 'Dhakad', '241/A North Kazipara Mirpur-10\r\n241/A North Kazipara Mirpur-10', 19, 1),
(20, 'BTI Chittagong Technical Hub', 'BR-7202915196', 'Abdul Alim', '01817552828', 'jstutul33@gmail.com', 'Rajshahi', 'Rajshahi', '241/A north kazipara\r\ndhaka', 23, 1),
(21, 'Rajshahi IT Training Center', 'BR-7696244577', 'Rayhan Mahmud', 'dddddddddd', 'jstutul30@gmail.com', 'Dhaka', 'Pabna', '241/A North Kazipara Mirpur-10', 24, 1),
(22, 'Barishal Skill Center', 'BR-3078673288', 'Sirajul Islam', 'dddddddddd', 'jstutul30@gmail.com', 'Dhaka', 'Pabna', '241/A North Kazipara Mirpur-10', 25, 1);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_paymentdeposit`
--

CREATE TABLE `accounts_paymentdeposit` (
  `id` bigint(20) NOT NULL,
  `payment_id` varchar(100) DEFAULT NULL,
  `trx_id` varchar(100) DEFAULT NULL,
  `base_amount` decimal(12,2) NOT NULL,
  `extra_charge` decimal(12,2) NOT NULL,
  `paid_amount` decimal(12,2) NOT NULL,
  `gateway` varchar(30) NOT NULL,
  `status` varchar(20) NOT NULL,
  `raw_create_response` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`raw_create_response`)),
  `raw_execute_response` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`raw_execute_response`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_paymentdeposit`
--

INSERT INTO `accounts_paymentdeposit` (`id`, `payment_id`, `trx_id`, `base_amount`, `extra_charge`, `paid_amount`, `gateway`, `status`, `raw_create_response`, `raw_execute_response`, `created_at`, `updated_at`, `user_id`) VALUES
(1, NULL, NULL, 10.00, 0.50, 10.50, 'bkash', 'pending', NULL, NULL, '2026-05-07 20:59:02.142057', '2026-05-07 20:59:02.142057', 4),
(2, NULL, NULL, 10.00, 0.50, 10.50, 'bkash', 'pending', NULL, NULL, '2026-05-07 20:59:55.540735', '2026-05-07 20:59:55.540735', 4),
(3, NULL, NULL, 10.00, 0.50, 10.50, 'bkash', 'pending', NULL, NULL, '2026-05-07 21:00:52.919928', '2026-05-07 21:00:52.919928', 4),
(4, NULL, NULL, 10.00, 0.50, 10.50, 'bkash', 'pending', NULL, NULL, '2026-05-07 21:02:09.281950', '2026-05-07 21:02:09.297573', 4),
(5, NULL, NULL, 10.00, 0.50, 10.50, 'bkash', 'pending', NULL, NULL, '2026-05-07 21:02:54.850999', '2026-05-07 21:02:54.850999', 4),
(6, 'TR0011tMRYkfj1778187821596', NULL, 10.00, 0.50, 10.50, 'bkash', 'pending', '{\"paymentID\": \"TR0011tMRYkfj1778187821596\", \"bkashURL\": \"https://payment.bkash.com/?paymentId=TR0011tMRYkfj1778187821596&hash=WaG9u5nYDzSRqHxnB0mMmShh!7ok!5nqgCfnLf!A7vwGo(vxn3iIrUgaidp8t*ny.ZMy15u9BxqmXVxufGDYl5EQ43c4fGIzCzw01778187821596&mode=0011&apiVersion=v1.2.0-beta/\", \"callbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/\", \"successCallbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/?paymentID=TR0011tMRYkfj1778187821596&status=success&signature=PsLyzpuhwc\", \"failureCallbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/?paymentID=TR0011tMRYkfj1778187821596&status=failure&signature=PsLyzpuhwc\", \"cancelledCallbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/?paymentID=TR0011tMRYkfj1778187821596&status=cancel&signature=PsLyzpuhwc\", \"amount\": \"10.50\", \"intent\": \"sale\", \"currency\": \"BDT\", \"paymentCreateTime\": \"2026-05-08T03:03:41:596 GMT+0600\", \"transactionStatus\": \"Initiated\", \"merchantInvoiceNumber\": \"DEP4\", \"statusCode\": \"0000\", \"statusMessage\": \"Successful\"}', NULL, '2026-05-07 21:03:39.294773', '2026-05-07 21:03:39.294773', 4),
(7, 'TR0011i8mQzv41778529599027', NULL, 10.00, 0.50, 10.50, 'bkash', 'failed', '{\"paymentID\": \"TR0011i8mQzv41778529599027\", \"bkashURL\": \"https://payment.bkash.com/?paymentId=TR0011i8mQzv41778529599027&hash=aNNlOAmX4z)soCzrd-PLf)qeg_G4FARhPsn-9VP1wg6j)GrnWn!vD.)6NhGZyArxpBn-0c6_0KVc)9U9CVEIbv4qxgqL(5jQ02eV1778529599027&mode=0011&apiVersion=v1.2.0-beta/\", \"callbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/\", \"successCallbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/?paymentID=TR0011i8mQzv41778529599027&status=success&signature=UZKvQ96vOr\", \"failureCallbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/?paymentID=TR0011i8mQzv41778529599027&status=failure&signature=UZKvQ96vOr\", \"cancelledCallbackURL\": \"http://127.0.0.1:8000/dashboard/deposit/callback/?paymentID=TR0011i8mQzv41778529599027&status=cancel&signature=UZKvQ96vOr\", \"amount\": \"10.50\", \"intent\": \"sale\", \"currency\": \"BDT\", \"paymentCreateTime\": \"2026-05-12T01:59:59:027 GMT+0600\", \"transactionStatus\": \"Initiated\", \"merchantInvoiceNumber\": \"DEP18\", \"statusCode\": \"0000\", \"statusMessage\": \"Successful\"}', NULL, '2026-05-11 19:59:57.390585', '2026-05-11 19:59:57.390585', 18);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_profile`
--

CREATE TABLE `accounts_profile` (
  `id` bigint(20) NOT NULL,
  `role` varchar(20) NOT NULL,
  `balance` decimal(12,2) NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `create_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `sign_image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_profile`
--

INSERT INTO `accounts_profile` (`id`, `role`, `balance`, `profile_image`, `is_active`, `create_at`, `update_at`, `user_id`, `sign_image`) VALUES
(5, 'admin', 0.00, 'profile_images/default.png', 1, '2026-05-01 17:31:12.084511', '2026-05-01 17:31:12.084511', 4, 'sign_images/default.png'),
(6, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 14:38:44.976270', '2026-05-02 14:38:44.976270', 5, 'sign_images/default.png'),
(7, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 14:43:56.901780', '2026-05-02 14:43:56.901780', 6, 'sign_images/default.png'),
(8, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 14:51:23.078850', '2026-05-02 14:51:23.078850', 7, 'sign_images/default.png'),
(9, 'institution', 0.00, 'profile_images/default.png', 1, '2026-05-02 14:53:22.811116', '2026-05-02 14:53:22.811116', 8, 'sign_images/default.png'),
(10, 'institution', 0.00, 'profile_images/default.png', 1, '2026-05-02 14:54:13.778134', '2026-05-02 14:54:13.778134', 9, 'sign_images/default.png'),
(11, 'institution', 0.00, 'profile_images/default.png', 1, '2026-05-02 14:54:34.514767', '2026-05-02 14:54:34.515766', 10, 'sign_images/default.png'),
(12, 'institution', 0.00, 'profile_images/default.png', 1, '2026-05-02 14:55:38.672799', '2026-05-02 14:55:38.672799', 11, 'sign_images/default.png'),
(19, 'institution', 0.00, 'profile_images/logo-removebg-preview_1_3fmnPtr.png', 1, '2026-05-02 15:21:58.695763', '2026-05-04 21:15:10.430240', 18, 'sign_images/default.png'),
(23, 'institution', 0.00, 'profile_images/default.png', 1, '2026-05-02 15:54:28.069378', '2026-05-02 15:54:28.069378', 22, 'sign_images/default.png'),
(24, 'institution', 0.00, 'profile_images/default.png', 1, '2026-05-02 15:58:24.436592', '2026-05-02 15:58:24.436592', 23, 'sign_images/default.png'),
(25, 'institution', 0.00, 'profile_images/default.png', 1, '2026-05-02 15:58:56.397441', '2026-05-02 15:58:56.397441', 24, 'sign_images/default.png'),
(26, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 20:29:41.141923', '2026-05-02 20:29:41.141923', 25, 'sign_images/default.png'),
(27, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 20:41:07.060110', '2026-05-02 20:41:07.060110', 31, 'sign_images/default.png'),
(28, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 20:46:20.861185', '2026-05-02 20:46:20.861185', 32, 'sign_images/default.png'),
(29, 'student', 0.00, 'profile_images/bangladesh_govt_logo_lhxUEX4.png', 1, '2026-05-02 20:47:06.676882', '2026-05-05 19:19:04.249764', 33, 'sign_images/default.png'),
(30, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 20:55:41.837203', '2026-05-02 20:55:41.837203', 34, 'sign_images/default.png'),
(31, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 21:00:04.840533', '2026-05-02 21:00:04.840533', 35, 'sign_images/default.png'),
(32, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 21:01:20.453097', '2026-05-02 21:01:20.453097', 36, 'sign_images/default.png'),
(33, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 21:03:48.946088', '2026-05-02 21:03:48.946088', 37, 'sign_images/default.png'),
(34, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 21:11:42.566145', '2026-05-02 21:11:42.566145', 38, 'sign_images/default.png'),
(35, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 21:12:02.138318', '2026-05-02 21:12:02.138318', 39, 'sign_images/default.png'),
(36, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-02 21:12:29.142326', '2026-05-02 21:12:29.142326', 40, 'sign_images/default.png'),
(37, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-03 17:55:23.534191', '2026-05-03 17:55:23.534191', 41, 'sign_images/default.png'),
(38, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-03 18:20:46.293519', '2026-05-03 18:20:46.293519', 42, 'sign_images/default.png'),
(39, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-03 18:22:11.836733', '2026-05-03 18:22:11.836733', 43, 'sign_images/default.png'),
(40, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-03 18:23:34.105275', '2026-05-03 18:23:34.105275', 44, 'sign_images/default.png'),
(41, 'student', 0.00, 'profile_images/default.png', 1, '2026-05-03 18:24:55.008728', '2026-05-03 18:24:55.008728', 45, 'sign_images/default.png'),
(42, 'student', 0.00, 'profile_images/khotiyan_6.png', 1, '2026-05-03 18:28:16.814356', '2026-05-03 18:28:16.819626', 46, 'sign_images/default.png'),
(43, 'student', 0.00, 'profile_images/khotiyan_7_2.png', 1, '2026-05-03 18:31:42.099684', '2026-05-03 18:31:42.104410', 47, 'sign_images/default.png'),
(44, 'student', 0.00, 'profile_images/khotiyan_7_2_WsJid7E.png', 1, '2026-05-03 18:34:45.625301', '2026-05-03 18:34:45.625301', 48, 'sign_images/default.png'),
(45, 'student', 0.00, 'profile_images/khotiyan_7_2_kLkxX3T.png', 1, '2026-05-03 18:37:32.802924', '2026-05-03 18:37:32.811787', 49, 'sign_images/default.png'),
(46, 'student', 0.00, 'profile_images/bangladesh_govt_logo.png', 1, '2026-05-03 18:38:36.716213', '2026-05-03 19:41:03.059758', 50, 'sign_images/default.png');

-- --------------------------------------------------------

--
-- Table structure for table `accounts_result`
--

CREATE TABLE `accounts_result` (
  `id` bigint(20) NOT NULL,
  `written_mark` decimal(5,2) NOT NULL,
  `practical_mark` decimal(5,2) NOT NULL,
  `viva_mark` decimal(5,2) NOT NULL,
  `total_mark` decimal(5,2) NOT NULL,
  `grade` varchar(5) NOT NULL,
  `exam_date` date NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `course_id` bigint(20) NOT NULL,
  `session_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_result`
--

INSERT INTO `accounts_result` (`id`, `written_mark`, `practical_mark`, `viva_mark`, `total_mark`, `grade`, `exam_date`, `is_published`, `created_at`, `course_id`, `session_id`, `student_id`) VALUES
(4, 45.00, 15.00, 10.00, 70.00, 'A-', '2026-05-05', 1, '2026-05-04 19:28:51.382328', 17, 1, 1),
(5, 42.00, 12.00, 8.00, 62.00, 'B', '2026-05-05', 0, '2026-05-04 19:29:12.876004', 16, 1, 1),
(6, 50.00, 15.00, 10.00, 75.00, 'A', '2026-05-08', 1, '2026-05-08 15:39:18.801816', 14, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_session`
--

CREATE TABLE `accounts_session` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `exam_date` date NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_session`
--

INSERT INTO `accounts_session` (`id`, `name`, `start_date`, `end_date`, `exam_date`, `status`) VALUES
(1, '2025-2026', '2025-01-01', '2025-12-31', '2026-12-10', 'upcoming'),
(2, '2024-2025', '2026-12-01', '2026-12-31', '2026-12-20', 'completed'),
(3, '2026-2027', '2026-01-01', '2026-12-31', '2026-12-22', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `accounts_student`
--

CREATE TABLE `accounts_student` (
  `id` bigint(20) NOT NULL,
  `reg_no` varchar(30) NOT NULL,
  `roll_no` varchar(30) NOT NULL,
  `reg_book_no` varchar(30) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `father_name` varchar(150) NOT NULL,
  `mother_name` varchar(150) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(20) NOT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `nid_no` varchar(30) DEFAULT NULL,
  `religion` varchar(30) DEFAULT NULL,
  `nationality` varchar(50) DEFAULT NULL,
  `present_address` varchar(300) DEFAULT NULL,
  `permanent_address` varchar(300) DEFAULT NULL,
  `education` varchar(300) DEFAULT NULL,
  `admissionDate` date DEFAULT NULL,
  `create_at` date DEFAULT NULL,
  `institution_id` bigint(20) NOT NULL,
  `profile_id` bigint(20) NOT NULL,
  `session_id` bigint(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `courses_id` bigint(20) NOT NULL,
  `email` varchar(200) NOT NULL,
  `district` varchar(300) DEFAULT NULL,
  `thana` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_student`
--

INSERT INTO `accounts_student` (`id`, `reg_no`, `roll_no`, `reg_book_no`, `full_name`, `father_name`, `mother_name`, `dob`, `gender`, `blood_group`, `mobile`, `nid_no`, `religion`, `nationality`, `present_address`, `permanent_address`, `education`, `admissionDate`, `create_at`, `institution_id`, `profile_id`, `session_id`, `is_active`, `courses_id`, `email`, `district`, `thana`) VALUES
(1, 'REG-000004', 'RL-000001', '12154', 'jafor sadik tutul', 'Abdul Jabbar', 'Hafiza Khatun', '2026-05-08', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 16, 29, 1, 1, 1, 'jstutul33@gmail.com', 'Pabna', 'Santhia'),
(2, 'REG-000005', 'RL-000002', '12154', 'ASA', 'AF', 'AM', '2026-05-03', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 30, 1, 1, 2, 'jstutul30@gmail.com', 'Pabna', 'Santhia'),
(3, 'REG-000006', 'RL-000003', '12154', 'ASAAA', 'AF', 'AM', '2026-05-03', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 31, 1, 1, 1, 'jstutul30@gmail.com', 'Pabna', 'Santhia'),
(4, 'REG-000007', 'RL-000004', '12154', 'Alif', 'Alif Fathger', 'Aif mother', '2026-05-03', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 32, 1, 1, 2, 'jstutul33@gmail.com', 'Pabna', 'Santhia'),
(5, 'REG-000008', 'RL-000005', '12154', 'Shoaib', 'AF', 'AM', '2026-05-03', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 33, 2, 1, 2, 'jstutul30@gmail.com', 'Pabna', 'Santhia'),
(6, 'REG-000009', 'RL-000006', '12154', 'A B', 'AF', 'Aif mother', '2026-05-03', 'Male', 'A-', '01817552828', '121212', NULL, NULL, '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 34, 1, 1, 2, 'a', 'Pabna', 'Santhia'),
(7, 'REG-000010', 'RL-000007', '12154', 'A Bffdf', 'AF', 'Aif mother', '2026-05-03', 'Male', 'A-', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 35, 1, 1, 2, 'a', 'Pabna', 'Santhia'),
(8, 'REG-000011', 'RL-000008', '12154', 'jafor sadik tutul', 'AF', 'Aif mother', '2026-05-03', 'Male', 'A-', '01817552828', '121212', NULL, 'Bangladeshi', '241/A north kazipara', 'dhaka', 'Bsc In CSE', NULL, NULL, 21, 36, 1, 1, 2, 'jstutul30@gmail.com', 'Pabna', 'Santhia'),
(9, 'REG-000012', 'RL-000009', '12154', 'Nahida Sultana', 'AF', 'AM', '2026-05-03', 'Female', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 37, 3, 1, 1, 'jstutul33@gmail.com', 'Pabna', 'Santhia'),
(10, 'REG-000013', 'RL-000010', '12154', 'Sirajul Islam', 'Alif Fathger', 'Aif mother', '2026-05-04', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 38, 1, 1, 2, 'jstutul26@gmail.com', 'Pabna', 'Santhia'),
(11, 'REG-000014', 'RL-000011', '12154', 'Sirajul Islam', 'Alif Fathger', 'Aif mother', '2026-05-04', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 39, 1, 1, 2, 'jstutul26@gmail.com', 'Pabna', 'Santhia'),
(12, 'REG-000015', 'RL-000012', '12154', 'Sirajul Islam', 'Alif Fathger', 'Aif mother', '2026-05-04', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 40, 1, 1, 2, 'jstutul26@gmail.com', 'Pabna', 'Santhia'),
(13, 'REG-000016', 'RL-000013', '12154', 'Sirajul Islam', 'Alif Fathger', 'Aif mother', '2026-05-04', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 41, 1, 1, 2, 'jstutul26@gmail.com', 'Pabna', 'Santhia'),
(14, 'REG-000017', 'RL-000014', '12154', 'Shaheen', 'AF', 'AM', '2026-05-06', 'Male', 'A+', '01817552828', '121212', NULL, 'Bangladeshi', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 42, 1, 1, 2, 'jstutul33@gmail.com', 'Pabna', 'Santhia'),
(15, 'REG-000021', 'RL-000015', '12154', 'Firoz', 'Alif Fathger', 'Aif mother', '2026-05-04', 'Male', 'B+', '01817552828', '121212', NULL, 'Indian', '241/A North Kazipara Mirpur-10', '241/A North Kazipara Mirpur-10', 'Bsc In CSE', NULL, NULL, 21, 46, 1, 1, 2, 'jstutul30@gmail.com', 'Pabna', 'Santhia');

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user`
--

CREATE TABLE `accounts_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `accounts_user`
--

INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(4, 'pbkdf2_sha256$320000$vYLAkh1K8RBek71CPImHqz$9Xm+d22wN39g3oXWfKan6kC8b/sG+QeuQU0dByKcSxk=', '2026-05-07 20:35:27.623300', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2026-05-01 17:31:11.806300'),
(5, 'pbkdf2_sha256$320000$8lI36g1hOoVeG6IKmu9VP8$MnrB2YC1bD3Q+fCirU/gs0eT+gxvUfjBW3Xq7+S30nA=', NULL, 0, '3516036960', '', '', '', 0, 1, '2026-05-02 14:38:44.647035'),
(6, 'pbkdf2_sha256$320000$Emycrkl56uhCBz55Cw6yNO$2SQatP2KwSRb9l5LwSCME/ns/DfN4arsAk/l0b6sLBk=', NULL, 0, '9082154996', '', '', '', 0, 1, '2026-05-02 14:43:56.594556'),
(7, 'pbkdf2_sha256$320000$Xil4UTmCQRo24Y1ZQucRLp$oYRzFVmZnVE73MJOF8FJanXFT9PUJLV443+/A1m4VYI=', NULL, 0, '7361739987', '', '', '', 0, 1, '2026-05-02 14:51:22.771944'),
(8, 'pbkdf2_sha256$320000$SOHcUFUy0jrDcwILPGCfN4$6p+o/pD0x+xehEUMZBx/Ze+TEHcLxv0AG7FxvGkRVYQ=', NULL, 0, '9476132162', '', '', '', 1, 1, '2026-05-02 14:53:22.455158'),
(9, 'pbkdf2_sha256$320000$PA1JUN5WpfJjtoNofwAw1K$ogN5OjbvNf23yjSoseQs8V/Za+s8305t9XSuHiFJZpA=', NULL, 0, '7634181101', '', '', '', 1, 1, '2026-05-02 14:54:13.399216'),
(10, 'pbkdf2_sha256$320000$NgoOXCTu3O1kmNQTugnwiI$3VCGutHyqO3IDPh2Oaih6U4PNkelJBzx1QMSb+gdgEs=', NULL, 0, '8247861827', '', '', '', 1, 1, '2026-05-02 14:54:34.190018'),
(11, 'pbkdf2_sha256$320000$74xEdQG6VXorLYmcmM48lu$66Fdwu9157LQNb2Pu7KBq8gmYvN4Twjr42OLR5i6bFk=', NULL, 0, '1617013700', '', '', '', 1, 1, '2026-05-02 14:55:38.355782'),
(18, 'pbkdf2_sha256$320000$RgySByOlJEK1xDIUlnItep$B9BhyUJo77vNY4GcXKc+8KrJ640R7VvatYTG1RJfVzc=', '2026-05-11 17:45:11.195699', 0, 'BR-7421813247', '', '', 'jstutul33@gmail.com', 1, 1, '2026-05-02 15:21:58.396115'),
(22, 'pbkdf2_sha256$320000$rjb53vtJmbdlB2d49Fqv1O$+EGs+LGd/dnQ5Pjc0vooyJWmYgDu+5/jZmJE7Vtfh38=', '2026-05-05 17:31:13.300486', 0, 'BR-7202915196', '', '', 'jstutul33@gmail.com', 1, 1, '2026-05-02 15:54:27.752397'),
(23, 'pbkdf2_sha256$320000$TdTPA6Am1R3QXFtqar7bEJ$2yZJYe20Jt/qMJ9zbenVkprgNK+FiVEf9vIOZ2nVaOU=', '2026-05-02 20:02:28.430439', 0, 'BR-7696244577', '', '', 'jstutul30@gmail.com', 1, 1, '2026-05-02 15:58:24.077551'),
(24, 'pbkdf2_sha256$320000$85FiqUkVhEbggHAWyna61z$Qy0no3iEvyW/a0LBzjBSvCt7TFkT2dv8e/CG/u8kLDA=', '2026-05-02 20:00:35.636385', 0, 'BR-3078673288', '', '', 'jstutul30@gmail.com', 1, 1, '2026-05-02 15:58:56.121178'),
(25, 'pbkdf2_sha256$320000$q0O4L3Qw9YcXY5g9Lp78Yz$/mMt9u278FeO6pUNk3B05/8uLuhB+xHca9Tuf9AQTuU=', NULL, 0, 'REG-000001', '', '', '', 0, 1, '2026-05-02 20:29:40.775750'),
(31, 'pbkdf2_sha256$320000$Qst4ixXOj92RqfrBvDcxja$2xXV+A4ojwWgzk7mwlsOQW3K3UTxfuGdPrxkoUmM3E4=', NULL, 0, 'REG-000002', '', '', '', 0, 1, '2026-05-02 20:41:06.698534'),
(32, 'pbkdf2_sha256$320000$zvrqGRN3KGPOQucwc1clKN$9752VGVJMFnHlDj4/XB835qh/mTHbh5K5OFR2Ilzhko=', NULL, 0, 'REG-000003', '', '', '', 0, 1, '2026-05-02 20:46:20.595036'),
(33, 'pbkdf2_sha256$320000$6Rt6QF1v2e6znXrcH6Eyvc$vnS9sue1Jn9MnsWO+OYtcxFtQkR26GxK3Wt2Nuzg3x4=', NULL, 0, 'REG-000004', '', '', '', 0, 1, '2026-05-02 20:47:06.391151'),
(34, 'pbkdf2_sha256$320000$Cj1VTS84PTPkyUJOtVMxxS$F0Cb5+NPWZGEsid4wJ4yPnxan4pjiTYIY+i3jNeUeQs=', NULL, 0, 'REG-000005', '', '', '', 0, 1, '2026-05-02 20:55:41.520200'),
(35, 'pbkdf2_sha256$320000$TscUJgakS7xtYPO3UxX95e$mn4hHUkksprDGWR6V7EiRVw963QPhcT1QKXIR80+710=', NULL, 0, 'REG-000006', '', '', '', 0, 1, '2026-05-02 21:00:04.540577'),
(36, 'pbkdf2_sha256$320000$N7bcBcg976SMeYSLxY7M49$/v9lLYZi9EhtorCONvEL83y9/fwpS7gqQVNEEWLb5x0=', NULL, 0, 'REG-000007', '', '', '', 0, 1, '2026-05-02 21:01:20.108412'),
(37, 'pbkdf2_sha256$320000$IDsFzzLgf7Pd5LckFXo4ru$F5Y9W3RqRrcKjVZXDqhfT0OVmDeE4KckAjdaECh1xao=', NULL, 0, 'REG-000008', '', '', '', 0, 1, '2026-05-02 21:03:48.664736'),
(38, 'pbkdf2_sha256$320000$eeXz3W34Q5Dbto5QIIMBnS$O+IfqbVfsYcjQI/HivtUkN1uUlmfm6QPSxpi/nreH3I=', NULL, 0, 'REG-000009', '', '', '', 0, 1, '2026-05-02 21:11:42.228044'),
(39, 'pbkdf2_sha256$320000$jHqRM6QwGGcHdn7AOozxxG$lbMg+kFOB6K2tn8qfvwUpn4OC/8JtZQLaJjRmS/zKDM=', NULL, 0, 'REG-000010', '', '', '', 0, 1, '2026-05-02 21:12:01.828163'),
(40, 'pbkdf2_sha256$320000$5YtSN08RO1ghF70iRVBfFP$ITysDG+YnWSJVb+8G0yutIdFvyKFiHSrDvG7j2OdWZk=', NULL, 0, 'REG-000011', '', '', '', 0, 1, '2026-05-02 21:12:28.825234'),
(41, 'pbkdf2_sha256$320000$45Z8Twlqs6E9hEj69aQ6Ap$qdwG5z3BU6gRwxtGzyB4zkJb+eZBVqhpNy7TWk3Scgw=', NULL, 0, 'REG-000012', '', '', '', 0, 1, '2026-05-03 17:55:23.133209'),
(42, 'pbkdf2_sha256$320000$5sucqlljMOFF3RWH9znT7Q$uWI/gjOOt6yxMdLnbAIV8XMts9n6NuBchzOjm4tBagg=', NULL, 0, 'REG-000013', '', '', '', 0, 1, '2026-05-03 18:20:45.876823'),
(43, 'pbkdf2_sha256$320000$I1AgW0H9nS1Hu1RBUL0glc$NeLwXmnlEefaBPSVVR2N6d7xCquVKKJhfB+1jCqB+JI=', NULL, 0, 'REG-000014', '', '', '', 0, 1, '2026-05-03 18:22:11.482855'),
(44, 'pbkdf2_sha256$320000$9b0flIHky63Kf7iK1ZQNph$lum/g92A38BVE1DoZxWqWVvPWfOr620gCz36Lmg/6b4=', NULL, 0, 'REG-000015', '', '', '', 0, 1, '2026-05-03 18:23:33.824776'),
(45, 'pbkdf2_sha256$320000$NvobNiOWRYXch83bE11gy2$eZ/bUrLixE81EJpSoSt4IJ4j3+AlPq/KZjyVlapJ4Uc=', NULL, 0, 'REG-000016', '', '', '', 0, 1, '2026-05-03 18:24:54.657163'),
(46, 'pbkdf2_sha256$320000$ay4DsWLBPP7koQsXgwxba9$4aPwIQ2SCdCybGEG0PwuL0BQhsJ2w67JgZz4vX+HTrI=', NULL, 0, 'REG-000017', '', '', '', 0, 1, '2026-05-03 18:28:16.483899'),
(47, 'pbkdf2_sha256$320000$rznMuJq8VNNnidqEgtXcHl$vuJjxQgQtXSp9Q2Ze3Hk9M3hZWuyqEr8KmDd3vwyNLs=', NULL, 0, 'REG-000018', '', '', '', 0, 1, '2026-05-03 18:31:41.805624'),
(48, 'pbkdf2_sha256$320000$5Y0B8R9VfhFOzFN6gXa0m7$BrHsQ/Qambts03x/K9pE8g3NLQ1+/aDAM/nIhaAECDw=', NULL, 0, 'REG-000019', '', '', '', 0, 1, '2026-05-03 18:34:45.225295'),
(49, 'pbkdf2_sha256$320000$12nfaNM0A8F7bUW4T5okar$rrd+4Q0Eq7nUYMxh46tme2LLxsc52eLQXqJCmkb/PgY=', NULL, 0, 'REG-000020', '', '', '', 0, 1, '2026-05-03 18:37:32.505860'),
(50, 'pbkdf2_sha256$320000$ISJNQU7x78SNq4vav7TvO8$o8hCdneEOUnOPBgJ0v4Egj3LbuY3dr+wgPIi42zxz6A=', NULL, 0, 'REG-000021', '', '', '', 0, 1, '2026-05-03 18:38:36.404608');

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_groups`
--

CREATE TABLE `accounts_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_user_permissions`
--

CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add course', 7, 'add_course'),
(26, 'Can change course', 7, 'change_course'),
(27, 'Can delete course', 7, 'delete_course'),
(28, 'Can view course', 7, 'view_course'),
(29, 'Can add institution', 8, 'add_institution'),
(30, 'Can change institution', 8, 'change_institution'),
(31, 'Can delete institution', 8, 'delete_institution'),
(32, 'Can view institution', 8, 'view_institution'),
(33, 'Can add profile', 9, 'add_profile'),
(34, 'Can change profile', 9, 'change_profile'),
(35, 'Can delete profile', 9, 'delete_profile'),
(36, 'Can view profile', 9, 'view_profile'),
(37, 'Can add student', 10, 'add_student'),
(38, 'Can change student', 10, 'change_student'),
(39, 'Can delete student', 10, 'delete_student'),
(40, 'Can view student', 10, 'view_student'),
(41, 'Can add balance transaction', 11, 'add_balancetransaction'),
(42, 'Can change balance transaction', 11, 'change_balancetransaction'),
(43, 'Can delete balance transaction', 11, 'delete_balancetransaction'),
(44, 'Can view balance transaction', 11, 'view_balancetransaction'),
(45, 'Can add session', 12, 'add_session'),
(46, 'Can change session', 12, 'change_session'),
(47, 'Can delete session', 12, 'delete_session'),
(48, 'Can view session', 12, 'view_session'),
(49, 'Can add result', 13, 'add_result'),
(50, 'Can change result', 13, 'change_result'),
(51, 'Can delete result', 13, 'delete_result'),
(52, 'Can view result', 13, 'view_result'),
(53, 'Can add certificate', 14, 'add_certificate'),
(54, 'Can change certificate', 14, 'change_certificate'),
(55, 'Can delete certificate', 14, 'delete_certificate'),
(56, 'Can view certificate', 14, 'view_certificate'),
(57, 'Can add payment deposit', 15, 'add_paymentdeposit'),
(58, 'Can change payment deposit', 15, 'change_paymentdeposit'),
(59, 'Can delete payment deposit', 15, 'delete_paymentdeposit'),
(60, 'Can view payment deposit', 15, 'view_paymentdeposit');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-05-11 17:37:54.771909', '1', 'REG-000004 - credit - 499.98', 1, '[{\"added\": {}}]', 11, 4),
(2, '2026-05-11 17:40:13.590082', '1', 'BR-7421813247 - credit - 499.98', 2, '[{\"changed\": {\"fields\": [\"User\"]}}]', 11, 4);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(11, 'accounts', 'balancetransaction'),
(14, 'accounts', 'certificate'),
(7, 'accounts', 'course'),
(8, 'accounts', 'institution'),
(15, 'accounts', 'paymentdeposit'),
(9, 'accounts', 'profile'),
(13, 'accounts', 'result'),
(12, 'accounts', 'session'),
(10, 'accounts', 'student'),
(6, 'accounts', 'user'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-05-01 11:53:43.109458'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-05-01 11:53:43.183886'),
(3, 'auth', '0001_initial', '2026-05-01 11:53:43.524695'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-05-01 11:53:43.607148'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-05-01 11:53:43.609190'),
(6, 'auth', '0004_alter_user_username_opts', '2026-05-01 11:53:43.633294'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-05-01 11:53:43.641465'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-05-01 11:53:43.651044'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-05-01 11:53:43.659525'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-05-01 11:53:43.674361'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-05-01 11:53:43.685931'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-05-01 11:53:43.691601'),
(13, 'auth', '0011_update_proxy_permissions', '2026-05-01 11:53:43.708339'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-05-01 11:53:43.719982'),
(15, 'accounts', '0001_initial', '2026-05-01 11:53:44.822207'),
(16, 'admin', '0001_initial', '2026-05-01 11:53:44.954530'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-05-01 11:53:44.986830'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-01 11:53:44.993043'),
(19, 'sessions', '0001_initial', '2026-05-01 11:53:45.047500'),
(20, 'accounts', '0002_session_student_session', '2026-05-02 08:57:38.004310'),
(21, 'accounts', '0003_alter_course_duration', '2026-05-02 11:09:57.358659'),
(22, 'accounts', '0004_course_cert_type', '2026-05-02 11:15:15.611955'),
(23, 'accounts', '0005_alter_course_exam_fee', '2026-05-02 11:20:19.390731'),
(24, 'accounts', '0006_alter_session_name_alter_session_start_date_and_more', '2026-05-02 13:05:27.172546'),
(25, 'accounts', '0007_alter_institution_branch_code', '2026-05-02 14:34:44.106036'),
(26, 'accounts', '0008_institution_is_active', '2026-05-02 16:03:12.161509'),
(27, 'accounts', '0009_student_is_active', '2026-05-02 19:01:06.157129'),
(28, 'accounts', '0010_alter_student_blood_group', '2026-05-02 19:47:17.880249'),
(29, 'accounts', '0011_alter_student_nationality', '2026-05-02 19:50:23.378659'),
(30, 'accounts', '0012_remove_student_courses_student_courses', '2026-05-02 20:32:57.268680'),
(31, 'accounts', '0013_student_email', '2026-05-02 20:52:29.127542'),
(32, 'accounts', '0014_alter_student_courses', '2026-05-02 20:59:58.505535'),
(33, 'accounts', '0015_alter_student_session', '2026-05-03 18:34:19.244271'),
(34, 'accounts', '0016_result', '2026-05-04 18:49:20.272422'),
(35, 'accounts', '0017_result_unique_student_course_session_result', '2026-05-04 19:28:26.297474'),
(36, 'accounts', '0018_certificate', '2026-05-05 18:02:58.614750'),
(37, 'accounts', '0019_alter_certificate_issue_date', '2026-05-05 19:36:41.365831'),
(38, 'accounts', '0020_paymentdeposit', '2026-05-07 20:58:15.303151'),
(39, 'accounts', '0021_profile_sign_image', '2026-05-09 13:20:23.362257'),
(40, 'accounts', '0022_student_district_student_thana', '2026-05-11 03:35:20.990691');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2twmiksqg5ol1rd5e75q7xywkep6hmai', 'e30:1wIrdI:t2QKXBNuUWLjI75bJyL_y5ZLAaZaG6WThE5J-MQALQw', '2026-05-15 17:26:32.699790'),
('chp9gh3osif2nkf7tqhyxszvpbhmucq4', 'e30:1wJGVv:uPRjw9DMdS7eyw9tiOtFtkrEknvj3Hzql96og7VClak', '2026-05-16 20:00:35.625823'),
('kxf9yf33wdhrvv3nfbnh2husp3iwadn2', '.eJxllNmOozgUQP-lnqdKZg3MWxEIgQITCITlBYENYYcKFNto_n2c7lJrWi1LfvC9Pvf4WvY_L3HyNRXx15g94hK__P1CCS9__X8xTVCddc8IrpLu3r-hvpseZfr2THn7jo5vZo-zRvrO_Q1QJGNBdos8kyBwyLgky1NaFBgAcubApwmmEuGAEMWwdJagDCMxJxPiBJbhAYcFMaVzAeQEmtYEFU89qUGA2aY_Et8urVJX_ADzjieeMFNwNtPUzm2ZvU6PPEqykFpzpgIlu75J2TkCqTdSdmCzwVHsk1stauVShv7aaVVfeo25QTcsc_uN4HfsawSvAUibOxkAlgCYbtEYrlNFvjlZvraaR6qBu8JFrbmGlcJEMiqNo17gn2oP6FMrbPUm8UeQ-A4dyfWKZKfF6g2gc7g_y0dB1KSdk38fp41UbYW-t4QlWMw2ZAzX5kzam0IXtmFJNZbqNKGvl-ZeVBHRJfVASk9N2ogUor0nY4iO2qi1JwqrRY7VZoquGm-6iLFkb7Ncj7OOS5kEcH8eOzk7xMXkSUuQQcM5orkBq8JEfBejPS1GAGccOH3kn3Z8BCtZm8JgmNP2xKCNq1KaIvv-zAsoe7_Vkxztep9dnz6_2DwOYINarkj9p6-2mG5NeqvtsLIX64f7jUXHX86k_8pPZ_8EiPMKd8RCV-OgW7PkupLsoW_j9CmcLcMUwmT1-GyYgByaF49hD2Bm-uw1i9Oz9lC4IJyZwUNxFynJKUQ252yhwPZ7m1qmcVNmWfzo6CE8mBlaO0myN__O3lY2o-QxX3zhsnnLWbtUzmdx6R-h0MmDpnvHbEnzUmBWyYiU8H6i7eqVrhgNS0CK0PnMTAf4JakCVIQHDu_6dfx0vazvg9KK0-DV5636KvXsyrHyEM_LpjLvEggc-STe38H4eW-hpeUfvVjv_MEdBvRVeLZebWfFBEf7Y9YupanfYi-lb6XtvG8p0xbr3qyiQh-ji6Ue7AWH0mCUuTrHV2P91N6Vs6TObsQqMFkLJ26_Wn424qIGDlutjkvxNnl0Q7K1WTfFOBv6sZx-fBKHf_8DblRsAA:1wMWnG:vJTo6ugcFf4cfVr4iwkROZ-zgMLFOcjIto8ANwrwveQ', '2026-05-25 19:59:58.491531'),
('q7oo8oertwmnl48w2ks4027sc5gsbpjn', '.eJxVjDsOwjAQRO_iGln-xD9K-pzBWq_XOIAcKU4qxN1JpBTQTDHvzbxZhG2tceu0xCmzK5OeXX7LBPikdpD8gHafOc5tXabED4WftPNxzvS6ne7fQYVe93WwGlA4MkAlqeC1EEU7myBL8A5R6kERIGUMZQ80ftBWmOxDUsWLwj5fJs04_Q:1wKJmM:KmVoxlqrIDHiJ08jFYCoOZeb7C-TZXKftXK9q4FWSgs', '2026-05-19 17:41:54.868582'),
('u3mt9w2rg2zfk4fw2vzcdp358vcr3mcm', 'e30:1wJGXB:qGFqR8pHcCBWnBsvDTt35jhi9FYcFpEmmtaDR8pqpvg', '2026-05-16 20:01:53.357836'),
('umb5j2edaru0b0sgpmww928045r3pxyl', 'e30:1wIrcr:wPBUDCZ532fqkuphStwXSxwxys9QHUKp4nMKVhtRm80', '2026-05-15 17:26:05.564877');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts_balancetransaction`
--
ALTER TABLE `accounts_balancetransaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accounts_balancetransaction_user_id_a58534ce_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `accounts_certificate`
--
ALTER TABLE `accounts_certificate`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cert_id` (`cert_id`),
  ADD UNIQUE KEY `serial_no` (`serial_no`),
  ADD UNIQUE KEY `result_id` (`result_id`);

--
-- Indexes for table `accounts_course`
--
ALTER TABLE `accounts_course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accounts_course_user_id_25717967_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `accounts_institution`
--
ALTER TABLE `accounts_institution`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `profile_id` (`profile_id`),
  ADD UNIQUE KEY `accounts_institution_branch_code_099b1d9b_uniq` (`branch_code`);

--
-- Indexes for table `accounts_paymentdeposit`
--
ALTER TABLE `accounts_paymentdeposit`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `payment_id` (`payment_id`),
  ADD UNIQUE KEY `trx_id` (`trx_id`),
  ADD KEY `accounts_paymentdeposit_user_id_46aaec06_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `accounts_profile`
--
ALTER TABLE `accounts_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `accounts_result`
--
ALTER TABLE `accounts_result`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_student_course_session_result` (`student_id`,`course_id`,`session_id`),
  ADD KEY `accounts_result_course_id_6f9f68d7_fk_accounts_course_id` (`course_id`),
  ADD KEY `accounts_result_session_id_dc85f126_fk_accounts_session_id` (`session_id`);

--
-- Indexes for table `accounts_session`
--
ALTER TABLE `accounts_session`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `accounts_student`
--
ALTER TABLE `accounts_student`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reg_no` (`reg_no`),
  ADD UNIQUE KEY `profile_id` (`profile_id`),
  ADD KEY `accounts_student_institution_id_8937851b_fk_accounts_` (`institution_id`),
  ADD KEY `accounts_student_courses_id_3f3b872c` (`courses_id`),
  ADD KEY `accounts_student_session_id_2488af7d_fk_accounts_session_id` (`session_id`);

--
-- Indexes for table `accounts_user`
--
ALTER TABLE `accounts_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  ADD KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  ADD KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts_balancetransaction`
--
ALTER TABLE `accounts_balancetransaction`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `accounts_certificate`
--
ALTER TABLE `accounts_certificate`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `accounts_course`
--
ALTER TABLE `accounts_course`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `accounts_institution`
--
ALTER TABLE `accounts_institution`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `accounts_paymentdeposit`
--
ALTER TABLE `accounts_paymentdeposit`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `accounts_profile`
--
ALTER TABLE `accounts_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `accounts_result`
--
ALTER TABLE `accounts_result`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `accounts_session`
--
ALTER TABLE `accounts_session`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `accounts_student`
--
ALTER TABLE `accounts_student`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `accounts_user`
--
ALTER TABLE `accounts_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_balancetransaction`
--
ALTER TABLE `accounts_balancetransaction`
  ADD CONSTRAINT `accounts_balancetransaction_user_id_a58534ce_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_certificate`
--
ALTER TABLE `accounts_certificate`
  ADD CONSTRAINT `accounts_certificate_result_id_17a12025_fk_accounts_result_id` FOREIGN KEY (`result_id`) REFERENCES `accounts_result` (`id`);

--
-- Constraints for table `accounts_course`
--
ALTER TABLE `accounts_course`
  ADD CONSTRAINT `accounts_course_user_id_25717967_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_institution`
--
ALTER TABLE `accounts_institution`
  ADD CONSTRAINT `accounts_institution_profile_id_953573be_fk_accounts_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `accounts_profile` (`id`);

--
-- Constraints for table `accounts_paymentdeposit`
--
ALTER TABLE `accounts_paymentdeposit`
  ADD CONSTRAINT `accounts_paymentdeposit_user_id_46aaec06_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_profile`
--
ALTER TABLE `accounts_profile`
  ADD CONSTRAINT `accounts_profile_user_id_49a85d32_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_result`
--
ALTER TABLE `accounts_result`
  ADD CONSTRAINT `accounts_result_course_id_6f9f68d7_fk_accounts_course_id` FOREIGN KEY (`course_id`) REFERENCES `accounts_course` (`id`),
  ADD CONSTRAINT `accounts_result_session_id_dc85f126_fk_accounts_session_id` FOREIGN KEY (`session_id`) REFERENCES `accounts_session` (`id`),
  ADD CONSTRAINT `accounts_result_student_id_dc9a1530_fk_accounts_student_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_student` (`id`);

--
-- Constraints for table `accounts_student`
--
ALTER TABLE `accounts_student`
  ADD CONSTRAINT `accounts_student_courses_id_3f3b872c_fk_accounts_course_id` FOREIGN KEY (`courses_id`) REFERENCES `accounts_course` (`id`),
  ADD CONSTRAINT `accounts_student_institution_id_8937851b_fk_accounts_` FOREIGN KEY (`institution_id`) REFERENCES `accounts_institution` (`id`),
  ADD CONSTRAINT `accounts_student_profile_id_99148f8b_fk_accounts_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `accounts_profile` (`id`),
  ADD CONSTRAINT `accounts_student_session_id_2488af7d_fk_accounts_session_id` FOREIGN KEY (`session_id`) REFERENCES `accounts_session` (`id`);

--
-- Constraints for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  ADD CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  ADD CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
