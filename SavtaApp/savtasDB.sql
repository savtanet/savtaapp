CREATE DATABASE IF NOT EXISTS `pythonlogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pythonlogin`;

CREATE TABLE IF NOT EXISTS `savtas` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `birtday` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `street` varchar(255) NOT NULL,
    `house` varchar(3) NOT NULL,
    `appatrment` varchar(3) NOT NULL,
    `floor` char(2) NOT NULL,
    `elevator` BOOLEAN,
    `phone` varchar(20) NOT NULL,
    `limitations` varchar(20) NOT NULL,
    `livingwith` varchar(50) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `savtas` (`id`, `username`, `password`, `birtday`, `city`, `street`, `house`, `appatrment`, `floor`, `elevator`, `phone`, `limitations`, `livingwith`) 
VALUES (1, 'test', 'test', '110370', 'ashdod', 'main', '5', '3', '2', '0', '123123123', 'limit asdasdasd', 'aba' );
