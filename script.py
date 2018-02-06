import sys
import csv
import ldap
import ldap.modlist as modlist
import string
import random
import MySQLdb
import smtplib

def validin():
	if len(sys.argv) <= 1:
		print "usage: $python file.csv"
		exit(1)

def readcsv(csvfile):
	reader = csv.reader(open(csvfile, "rb"), delimiter=',')
	return reader

def adduser(con, user, sname, pwd):
	dn = "uid="+str(user)+",dc=example,dc=org"
	modlist = {
	  "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
	  "uid": [str(user)],
	  "sn": [str(sname)],
	  "givenName": [str(user)],
	  "uidNumber": ["5000"],
	  "gidNumber": ["10000"],
	  "loginShell": ["/bin/bash"],
	  "cn": [str(user)+" "+str(sname)],
	  "homeDirectory": ["/home/"+str(user)],
	  "displayName": [str(user)+" "+str(sname)],
	  "userPassword": [str(pwd)]
	}

	result = con.add_s(dn, ldap.modlist.addModlist(modlist))
	return result

def removeuser(con, user):
	dn = 'uid='+str(user)+',dc=example,dc=org'
	print dn
	con.delete_s(dn)
	
	return True

def finduser(con, user):
	ldap_base = "dc=example,dc=org"
	query = "(uid="+str(user)+")"
	
	result = con.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)
	return result

def pwd_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def inserdb(cur, user, pwd):
	sql = """INSERT INTO user(uid,pwd) VALUES ('"""+user+"""', md5('"""+pwd+"""'));"""
	print sql
	
	try:
		cur.execute(sql)
		db.commit()
	except:
		db.rollback()

def sendmail(server, user, pwd, destination):
	msg = "User Name:"+user+" "+"Password:"+pwd
	server.sendmail("admin@admin.com", destination, msg)




if __name__=='__main__':
	validin()
	itens = readcsv(sys.argv[1])

	db = MySQLdb.connect(host="127.0.0.1",  
                         user="root",      
                         passwd="secret",    
                         db="app")
	cur = db.cursor()
	# cur.execute("CREATE TABLE IF NOT EXISTS user(id int(11) NOT NULL AUTO_INCREMENT, uid varchar(45) NOT NULL, pwd varchar(255) NOT NULL, PRIMARY KEY (id))")  

	con = ldap.initialize('ldap://127.0.0.1')
	con.simple_bind_s("cn=admin,dc=example,dc=org","admin")

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("admin@admin.com", "YOUR PASSWORD")

	for coluns in itens:
		# removeuser(con, coluns[0])
		if finduser(con, coluns[0]) == []:
			tmp_pwd=pwd_generator()
			adduser(con, coluns[0], coluns[1], tmp_pwd)
			inserdb(cur, coluns[0], tmp_pwd)
			sendmail(server,coluns[0],tmp_pwd,coluns[2])


