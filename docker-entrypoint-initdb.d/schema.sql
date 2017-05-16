CREATE DATABASE fbg;
USER fbg;
CREATE USER 'user'@'%' IDENTIFIED BY '78df46013';

GRANT ALL PRIVILEGES ON \*.\* TO 'user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

CREATE TABLE iplist (ip bigint(20) DEFAULT NULL, ipcount INT DEFAULT 1, lat decimal(10,7) DEFAULT NULL,
 lng decimal(10,7) DEFAULT NULL,
 rdap_name varchar(50) DEFAULT NULL,
  rdap_org_name varchar(100) DEFAULT NULL,
  city varchar(50) DEFAULT NULL, region varchar(50) DEFAULT NULL,
  regioncode varchar(3) DEFAULT NULL, country varchar(75) DEFAULT NULL, countrycode varchar(3) DEFAULT NULL
   ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8 COLLATE=utf8_bin;
   
create table appstat (id INT DEFAULT 1 PRIMARY KEY, total INT DEFAULT 0);