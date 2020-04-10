  CREATE TABLE `savtas` (
    `id` identity,
    `name` varchar(255) NOT NULL,
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
  )''' )
