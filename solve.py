import os
command='netstat -aon|findstr "13333"'
result=os.popen(command)
info=result.readlines()
port=info[0]
val=''
for i in range(len(port)-1,0,-1):
	if port[i]==' ':
		break
	val=port[i]+val
command='taskkill -f -im '+val
os.popen(command)
print(command)