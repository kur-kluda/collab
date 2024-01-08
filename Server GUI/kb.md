- Create model
- ensure app is registered @ settings (apps)
- if more than 1 db, a router is needed

- oddly enough router must not be written as is, it needs to be inside quotes.
'appName.router..etc'

- run 
```
manage.py makemigrations a
```
where a is appname specified in 2 (apps) @settings

then ensure db has user with db rights.

```
 CREATE USER 'a'@'%' IDENTIFIED BY 'a';
 ```
 OR localhost instead of %

```
 CREATE DATABASE aa;
```

and grant with grant:

```
GRANT ALL PRIVILEGES ON aa.* TO 'a'@'%' WITH GRANT OPTION;
```


then can run the magic.. migrations:

```
manage.py  migrate --database=howyounamed@settinhs.pu
OR
simply manage.py migrate
if router is fine.
```

hererererer

```
python ./manage.py makemigrations a

python ./manage.py migrate --database=meta-db

```
