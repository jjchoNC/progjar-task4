import sys
import os.path
import uuid
from glob import glob
from datetime import datetime

class HttpServer:
	def __init__(self):
		self.sessions={}
		self.types={}
		self.types['.pdf']='application/pdf'
		self.types['.jpg']='image/jpeg'
		self.types['.txt']='text/plain'
		self.types['.html']='text/html'
	def response(self,kode=404,message='Not Found',messagebody=bytes(),headers={}):
		tanggal = datetime.now().strftime('%c')
		resp=[]
		resp.append("HTTP/1.0 {} {}\r\n" . format(kode,message))
		resp.append("Date: {}\r\n" . format(tanggal))
		resp.append("Connection: close\r\n")
		resp.append("Server: myserver/1.0\r\n")
		resp.append("Content-Length: {}\r\n" . format(len(messagebody)))
		for kk in headers:
			resp.append("{}:{}\r\n" . format(kk,headers[kk]))
		resp.append("\r\n")

		response_headers=''
		for i in resp:
			response_headers="{}{}" . format(response_headers,i)
		#menggabungkan resp menjadi satu string dan menggabungkan dengan messagebody yang berupa bytes
		#response harus berupa bytes
		#message body harus diubah dulu menjadi bytes
		if (type(messagebody) is not bytes):
			messagebody = messagebody.encode()

		response = response_headers.encode() + messagebody
		#response adalah bytes
		return response

	def proses(self,data):
		requests = data.split(b"\r\n")
		#print(requests)

		baris = requests[0]
		#print(baris)

		all_headers = [n for n in requests[1:] if n!='']
		j = baris.split(b" ")
		try:
			method=j[0].upper().strip()
			if (method==b'GET'):
				object_address = j[1].strip()
				return self.http_get(object_address, all_headers)
			elif (method==b'POST'):
				object_address = j[1].strip()
				return self.http_post(object_address, all_headers)
			elif (method==b'DELETE'):
				object_address = j[1].strip()
				print("object_address: ", object_address)
				return self.http_delete(object_address, all_headers)
			else:
				return self.response(400,'Bad Request','',{})
		except IndexError:
			return self.response(400,'Bad Request','',{})

	def http_get(self,object_address,headers):
		files = glob('./*')
		#print(files)
		thedir='./'
		if (object_address == b'/'):
			return self.response(200,'OK','Ini Adalah web Server percobaan',dict())
		if (object_address == b'/video'):
			return self.response(302,'Found','',dict(location='https://youtu.be/katoxpnTf04'))
		if (object_address == b'/santai'):
			return self.response(200,'OK','santai saja',dict())
		if (object_address == b'/list'):
			files_list = '\n'.join(files)
			return self.response(200,'OK',files_list,{'Content-type': 'text/plain'})

		object_address=object_address[1:]
		object_address = object_address.decode('utf-8')
		if thedir+object_address not in files:
			return self.response(404,'Not Found','',{})
		fp = open(thedir+object_address,'rb') #rb => artinya adalah read dalam bentuk binary
		#harus membaca dalam bentuk byte dan BINARY
		isi = fp.read()
		
		fext = os.path.splitext(thedir+object_address)[1]
		content_type = self.types[fext]
		
		headers={}
		headers['Content-type']=content_type
		
		return self.response(200,'OK',isi,headers)

	def http_post(self,object_address,headers):
		filename = headers[0].split(b':')[1].strip().decode('utf-8')
		body = headers[2]
		thedir='./'
		if (object_address == b'/upload'):
			try:
				fp = open(thedir+filename,'wb')
				fp.write(body)
				return self.response(200,'OK','File Created',{'Content-type': 'text/plain'})
			except Exception as e:
				return self.response(500,'Internal Server Error',str(e),{'Content-type': 'text/plain'})
		else:
			return self.response(400,'Bad Request','',{'Content-type': 'text/plain'})
		
	def http_delete(self,object_address,headers):
		files = glob('./*')
		print(object_address[1:])
		#print(files)
		thedir='./'
		if (object_address == b'/'):
			return self.response(400,'Bad Request','',{})
		if (object_address == b'/video'):
			return self.response(400,'Bad Request','',{})
		if (object_address == b'/santai'):
			return self.response(400,'Bad Request','',{})
		object_address=object_address[1:]
		object_address = object_address.decode()
		print(thedir+object_address)
		if thedir+object_address not in files:
			return self.response(404,'Not Found','',{})
		try:
			os.remove(thedir+object_address)
			return self.response(200,'OK','File Deleted',{'Content-type': 'text/plain'})
		except Exception as e:
			return self.response(500,'Internal Server Error',str(e),{'Content-type': 'text/plain'})

#>>> import os.path
#>>> ext = os.path.splitext('/ak/52.png')

if __name__=="__main__":
	httpserver = HttpServer()
	d = httpserver.proses('GET testing.txt HTTP/1.0')
	print(d)
	d = httpserver.proses('GET donalbebek.jpg HTTP/1.0')
	print(d)
	#d = httpserver.http_get('testing2.txt',{})
	#print(d)
#	d = httpserver.http_get('testing.txt')
#	print(d)















