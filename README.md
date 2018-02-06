#Description

Read a csv, insert in ldap, insert in mysql and send mail

#Before Start

1. Install S.O dependencies

```
sudo yum install python-devel openldap-devel mysql-devel
```

2. Install python libs
```
pip install -r requirements.txt
```

3. Docker openldap
```
docker run --name my-openldap-container -p 389:389 -p 636:636 --detach osixia/openldap:1.1.11
```

4. Docker mysql
```
docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 -d mysql:latest

```

5. Use Gmail
```
replace in line 88
"YOUR EMAIL LOGIN", "YOUR PASSWORD"
for your credencials
```

6. Run
```
python script.py planilha.csv
```