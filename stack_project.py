# Import dependencies
import subprocess
import pyperclip as cp
from tkinter import Tk, messagebox
from subprocess import Popen, PIPE
import requests
import webbrowser
import sys,os

err,erro,errmsg,errout="","","","";p,c,j=0,0,0
tag=""

def sliceErr(msg):
	print(str(msg).replace("\\r\\n",""))
	n=str(msg).find('error')
	emsg=str(msg)[n:]
	eout=emsg[:emsg.find('\\r\\n')]
	return eout

def execute_return(cmd):  #2
	args = cmd.split()
	proc = Popen(args, stdout=PIPE, stderr=PIPE)
	out, err = proc.communicate()
	return out, err

def mak_req(error):
	resp = requests.get("https://api.stackexchange.com/" +
						"/2.3/search?order=desc&sort=activity&tagged="+tag+"&intitle={}&site=stackoverflow".format(error))
	return resp.json( )

def get_urls(json_dict):
	c = 0
	for i in json_dict['items']:
		if i['is_answered'] and c<4:
			webbrowser.open(i['link'])
			c=c+1

Ftype = sys.argv[1]				#1
s=Ftype[Ftype.find('.'):]    

if(s=='.py'):
	p=1;tag="python"
	Fname = "python "+os.getcwd()+'\\'+sys.argv[1]
	out, err = execute_return(Fname)
	# This line is used to store that part of error we are interested in.
	if err:
		erro = err.decode("utf-8").strip().split("\r\n")[-1]
		errout =erro
		print(err)

elif(s=='.c'):
	c=1;tag="C"
	Fname = "gcc "+os.getcwd()+'\\'+sys.argv[1]
	out, err = execute_return(Fname)
	if err:
		errout =sliceErr(err)

elif(s=='.java'):
	j=1;tag="Java"
	Fname = "javac "+os.getcwd()+"\\"+sys.argv[1]
	out,err = execute_return(Fname)
	if err:
		errout = sliceErr(err)

window = Tk()
window.overrideredirect(1)
window.withdraw()

if errout:
	filter_error = errout.split(":")
	json = mak_req(filter_error[1])
	if messagebox.askyesno("Do you want to search about this error?",errout)==True:
		cp.copy(str(errout)+" "+tag)
		window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
		window.destroy()
		window.quit()
		get_urls(json)
else:
	if p:
		print(out.decode('utf-8'))
	elif c and errout=="":
		subprocess.call("a.exe")
	elif j and errout=="":
		subprocess.call("java "+Ftype[:Ftype.find('.')])
