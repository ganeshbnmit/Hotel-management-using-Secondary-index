from cgitb import reset
import csv
import os
from csv import writer
from flask import Flask, flash, render_template, request, url_for, redirect

open("d.csv","a") 
open("i.csv","a")
open("si.csv","a")


class product:
    """Pid,pname,desc,price,mname"""

class index_i():
    """Pid,iaddr"""
    def __init__(self,ipid,iaddr):
        self.ipid=ipid
        self.iaddr=iaddr

class sindex:
    """pname,Pid"""
    def __init__(self,sname,spid):
        self.sname=sname
        self.spid=spid
global i
global s
global p

global indsize
indsize=0
global sindsize
sindsize=0
global buffer

pos=-1
i=[]
s=[]
p=[]
buffer=[]


def initial():
        
        with open("i.csv") as ifile:
            reader_obj=csv.reader(ifile)
            for row in reader_obj:
                row=row[0]
                l=row.split('|')
                temp=(int(l[0]),int(l[1]))
                i.append(temp)
def sinitial():
    
    with open("si.csv") as sfile:
        reader_obj=csv.reader(sfile)
        for row in reader_obj:
            row=row[0]
            l=row.split('|')
            
            temp=((l[0]),int(l[1]))
            s.append(temp)
        

def iwrite():
    global i
    global indsize
    with open("i.csv","w",newline='') as write_obj:
        csv_writer=writer(write_obj,delimiter='|')
        for k in range(0,len(i)):
            csv_writer.writerow(i[k])
def swrite():
    global s
    global sindsize
    with open("si.csv","w",newline='') as write_obj:
        csv_writer=writer(write_obj,delimiter="|")
        for k in range(0,len(s)):
            csv_writer.writerow(s[k])
def search_product(fusn):
    low=0
    high=len(i)-1
    while(low<=high):
        mid=(low+high)//2
        
        if(fusn==i[mid][0]):
            return mid
        elif(fusn>i[mid][0]):
            low = mid + 1
            
        else:
            high=mid-1
            
    return -1
def sec_search(skey):
    global s
    flag=-1
    global sindsize
    
    
    for j in range(0,len(s)):
        if(skey==s[j][0]):
            print(s[j][1],s[j][0])
            flag=j
         
    return flag
global res
def ssearch(skey):
    global res
    res=[]
    
    for j in range(0,len(s)):
        if(skey==s[j][0]):
            
            for p in range(0,len(i)):
                if(s[j][1]==i[p][0]):
                    pos=i[p][1]
                    print("position",pos)
                    file=open("d.csv")
                    file.seek(pos)
                    line=file.readline()
                    file.close()
                    print(line)
                    res.append(line)
                    break
    return res
    
   
    
    
def pack(pid,name,desc,price,mname):
    buffer.append(pid)
    
    buffer.append(name)

    buffer.append(desc)
   
    buffer.append(price)
    
    buffer.append(mname)


def add(pid,r,desc,q,z):
    global indsize
    global sindsize
    global x
    global i
    global s
    x=0
    
    if(len(i)!=0):
        if(search_product(int(pid))>=0):
            print("Customer already exist")
            return False
            
    pid=int(pid)
    d=open("d.csv",'r',newline='')
    d.seek(0,2)
    k=int(d.tell())
    d.close()
   
    buffer.clear()
    pack(pid,r,desc,q,z)
    
    temp=(pid,k)
    i.append(temp)
    indsize=indsize+1
   
    with open("d.csv",'a+',newline='') as out:
        writer=csv.writer(out,delimiter='|')
        writer.writerow(buffer)
    tem=(r,pid)
    s.append(tem)
    sindsize=sindsize+1
    
    i.sort()
    s.sort()
    
    iwrite()
    swrite()
    return True
def delete_record(name,p):
    global sindsize
    global indsize
    p=int(p)
    if((name,p) in s):
        message="Element present deleteing and Rewriting the files"
        
        for h in range(0,len(i)):
            if(p==i[h][0]):
                offset=i[h][1]
               
                fread=open("d.csv","r")
            
                fread.seek(offset)
                line=fread.readline()
                print("Rewriting the file")
                Newline=line.replace(line[0],"$",1)
                fread.close()
                f =open("d.csv","r+")
                f.seek(offset)
                f.write(Newline)
                break
                
        s.remove((name,p))
        i.remove((p,offset))
        sindsize=sindsize-1
        indsize=indsize-1
        iwrite()
        swrite()
    else:
        message="Customer Name and ID do not match"
    return message
def unpack():
    global array
    ele=0
    with open("d.csv") as file_name:
        file_read = csv.reader(file_name)
        
        array = list(file_read)
        arrayOfProducts=[]
        
        for k in array:
            ele=k
            for j in ele:
                if(j[0]=='$'):
                    arrayOfProducts.append(["Record ","Deleted","-","-","-"])
                    continue
                sub=j.split('|')
                arrayOfProducts.append(sub)
        return arrayOfProducts  

def unpack_index():
    global arr
    ele=0
    with open("i.csv") as file_name:
        file_read = csv.reader(file_name)
        
        arr = list(file_read)
        arrayOfProducts=[]
        
        for k in arr:
            ele=k
            for j in ele:
                sub=j.split('|')
                arrayOfProducts.append(sub)
        return arrayOfProducts   
def unpack_sindex():
    global arr
    ele=0
    with open("si.csv") as file_name:
        file_read = csv.reader(file_name)
        
        arr = list(file_read)
        arrayOfProducts=[]
        
        for k in arr:
            ele=k
            for j in ele:
                sub=j.split('|')
                arrayOfProducts.append(sub)
        return arrayOfProducts 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
@app.route('/')
def index():
    
    print(i)
    print(s)
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_p():
    
   return render_template('add.html')


@app.route('/indexfileContents')
def u_i():
    arrayOfproducts=unpack_index()
    return render_template('indexfile.html',arrayOfproducts=arrayOfproducts)

@app.route('/secondaryfileContents')
def u_s():
    arrayOfproducts=unpack_sindex()
    return render_template('secondfile.html',arrayOfproducts=arrayOfproducts)    
@app.route('/search',methods=['GET', 'POST'])
def search_page():
    
    global s
    
    
    if(request.method=='POST'):
        skey=request.form.get('name')
        result=sec_search(skey)
        if(result==-1):
            
            message='Customer not present in the Hotel'
            return render_template('search.html',message=message)
        else:
            
            res=ssearch(skey)
         
            message='The Customers are:'
        return render_template('search.html',message=message,res=res)
    return render_template('search.html')

@app.route('/list',methods=['POST','GET'])
def listmethod():
        if(request.method=='POST'):
            name=request.form.get('name')
            ID=request.form.get('ID')
        
            desc=request.form.get('desc')
            price=request.form.get('price')
            mname=request.form.get('mname')
            
            
            result=add(ID,name,desc,price,mname)
            if(result==True):
                arrayOfproducts=unpack()
                message = "Customer added Sucessfully"
                
            else:
                message = "Customer ID cant be repeated."
                arrayOfproducts=unpack()
            return render_template('list.html',message=message,arrayOfproducts=arrayOfproducts)


            
        arrayOfproducts=unpack()
        print(arrayOfproducts)
        return render_template('list.html',arrayOfproducts=arrayOfproducts)

global name_to_delete
@app.route('/delete', methods=['GET', 'POST'])
def del_product():
    global name_to_delete
    if(request.method=='POST'):
            name_to_delete=request.form.get('name')
            result=sec_search(name_to_delete)
            if(result==-1):
            
                message='Customer not present in the hotel'
                return render_template('delete.html',message=message)
            else:
            
                res=ssearch(name_to_delete)
         
                message='Customer present are'
                return render_template('del_search.html',message=message,res=res)
           
            
            
    return render_template('delete.html')
@app.route('/del_search',methods=['GET', 'POST'])
def del_p():
    global name_to_delete
    if(request.method=='POST'):
        ID=request.form.get('id')
        message=delete_record(name_to_delete,ID)
        return render_template('delete.html',message=message)
    return render_template('del_search.html')


if __name__ == '__main__':
    app.run(debug=True)


###Python Functions To implement Secondary Indexing###


            
           
