'''with open ("twitter_data.txt", "r") as f:
	data=f.read()
data = unicode(data, "utf-8")
data=data.split("}\n")

co=0
err=0
with open("output.txt","w") as fil:
			fil.write('')
for i in data:
	print co
	co+=1
	try:
		j=i.split('"text":')[1]
		with open("output.txt","a") as fil:
			fil.write(j.split(', "created_at":')[0]+"\n@@@\n")
			#fil.write(j.split(', "created_at":')[1].split(',')[0]+"\n")
	except IndexError:
		err+=1
		print "no_of_errors="+str(err)
		print i'''

'''with open ("twitter_data.txt", "r") as f:
	data=f.read()
data2=data.replace("}\n","},\n")
data3="[\n"+data2+"\n]"
with open("Output.txt", "w") as text_file:
	text_file.write(data3)
	
import json
	f = open('Output.txt') 
data = json.load(f)'''

with open('output.txt','r') as f:
	data=f.read()

data=data.split('\n@@@\n')
with open('small.txt','w') as fi:
	fi.write('')
with open('small.txt','a') as fi:
	for i in xrange(30000):
		fi.write(data[i]+'\n@@@\n')

