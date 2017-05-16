# Introduction
This program is used to upload log data, and search for IP addresses and the GeoIP and RDAP 
info about them.  It is a web application written in Python2 using Flask, and MySql. It also
uses a Dockerized version of freegeoip since their site has a 15,000/hr restriction.  By using 
their Dockerfile, I'm able to still perform an API call, but without any restrictions.

# How to install
Installation is just a matter of downloading the git repo for this site and for freegeoip.  
This runs on a Ubuntu 16.04, and you will need to install Docker.  Here's a good site 
that tells you how to install it:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

## Installing IPSearch:

```
git clone https://github.com/tgruenewald/python_challenge.git
```

## Install MySql docker
From the directory that you just downloaded IPSearch, run the `setup_database.sh` script.  This will
setup a MySql container.


## Get the geoip 
Next you will want to find another directory to download freegeoip. 
```
git clone https://github.com/fiorix/freegeoip
docker build -t mygeoip .
docker run --name mygeogeo -d -p 8080:8080 -t mygeoip
```
## Install Flask and the IPSearch app
```
docker build -t ipfind .
docker run --name fbg3 --link mygeogeo --link some-mysql -d -p 8081:80 -t ipfind
```

When everything is run, it will look like this:
```bash
terryg@saturn2:~/share/flask$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                           NAMES
2f1d4bc4c2cf        ipfind              "/usr/bin/supervisord"   4 seconds ago       Up 3 seconds        443/tcp, 0.0.0.0:8081->80/tcp   fbg3
67f99038759b        mygeoip             "/go/bin/freegeoip"      23 minutes ago      Up 23 minutes       0.0.0.0:8080->8080/tcp          mygeogeo
4aa71f284288        mysql:5.7           "docker-entrypoint.sh"   47 minutes ago      Up 47 minutes       3306/tcp                        some-mysql
terryg@saturn2:~/share/flask$
```

# How to Use
Before you can search, you will need to upload some data. You can pick any file that contains
IP addresses.  At this time, the program only supports IPv4.  

## Uploading files
To upload a file, click "Choose File" and pick from a text file with IP addresses.  Then click "Upload". 
If you get a 502 Bad Gateway error, it means you clicked "Upload" before you clicked "Choose File". 
After clicking "Upload", click "Parse".  This will begin the parsing process.  While parsing is 
going on, you can still search. There will be a status that gets reported to let you know when the 
parsing is complete.


## Query language
The query language is fairly simple.  It is a field name is quotes followed by a comparison operator
and then a value in quotes.  These expressions can be separated by "and" or "or" and can be chained.

For example:
```
"city" = "austin" or "region" = "colorado"
```
If you click search with nothing in the field (a blank search), then all rows are 
returned.

Comparison operators that are supported are: `=, !=, >, <`
Note searches are case insensitive, and that unicode is fully supported.



