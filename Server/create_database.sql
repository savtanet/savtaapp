drop database development;
create database development;
use development;
create table Haver (facebook_id varchar(63) primary key);
create table HaverCertified (name varchar(63) not null, location varchar(255) not null, phone varchar(15) unique not null, facebook_id varchar(63) primary key, email varchar(127) unique not null, occupation varchar(255) default NULL, spoken_languages varchar(255) not null);
