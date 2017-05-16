
2042  sudo apt-get install python-dev libmysqlclient-dev
 2043  pip install MySQL-python
pip install xmltodict
pip install python-dateutil

mysql -uroot -p
2) Create user

CREATE USER 'user'@'%' IDENTIFIED BY 'password';
3) Grant permissions

 GRANT ALL PRIVILEGES ON \*.\* TO 'user'@'%' WITH GRANT OPTION;
4) Flush priviledges

FLUSH PRIVILEGES;

CREATE TABLE iplist (ip bigint(20) DEFAULT NULL, ipcount INT DEFAULT 1, lat decimal(10,7) DEFAULT NULL,
 lng decimal(10,7) DEFAULT NULL,
 rdap_name varchar(50) DEFAULT NULL,
  rdap_org_name varchar(100) DEFAULT NULL,
  city varchar(50) DEFAULT NULL, region varchar(50) DEFAULT NULL,
  regioncode varchar(3) DEFAULT NULL, country varchar(75) DEFAULT NULL, countrycode varchar(3) DEFAULT NULL
   ) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8 COLLATE=utf8_bin;

RDAP
net
    registrationDate
    name
    <orgRef handle="QCC-18" name

CREATE TABLE iplist (ip bigint(20) DEFAULT NULL);

 create table appstat (id INT DEFAULT 1 PRIMARY KEY, total INT DEFAULT 0);
requests
netaddr
MySQLdb