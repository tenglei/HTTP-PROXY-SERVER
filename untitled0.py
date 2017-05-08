import socket
import thread
import urlparse
import select
import ssl
tag=0
addwebs = open('controlWeb.txt')
iptable = open('iptable.txt')
webs=[]
while 1:
    tmp = addwebs.readline().strip('\n')
    if not tmp:
        break
    webs.append(tmp)
iplist=[]
legalip=0
while 1:
    iptmp = iptable.readline().strip('\n')
    if not iptmp:
        break
    iplist.append(iptmp)
localip = socket.gethostbyname(socket.gethostname())
class GetImformation(object):
    def __init__(self,conn,addr):
        self.source=conn
        self.request=""
        self.headers={}
        self.destnation=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.run()
    def get_headers(self):
        header=''
        while True:
            header+=self.source.recv(20480)
            index=header.find('\n')
            if index >0:
                break
        firstLine=header[:index]
        self.request=header[index+1:]
        self.headers['method'],self.headers['path'],self.headers['protocol']=firstLine.split()
        
        
#        print 'first line:'
#        print firstLine
#        print '\n'
##        
#        print 'headers:'  
#        print self.headers
#        print '\n'
#        
#        print 'header:'
#        print header
#        print '\n'
        
#        print self.headers['path']
        
    def conn_destnation(self):
        tag=0
        legalip=0
        url=urlparse.urlparse(self.headers['path'])
        urltmp = url[2]
        dot = urltmp.find(':')
        if dot>0:
            hostname = urltmp
        else:
            hostname=url.hostname
#        print 'url:'
#        print url
#        print '\n'
#        print 'hostname:'
#        print hostname
#        print '\n'
        for web in webs:
            controlURL = {}
            controlURL['web'] = web
            control = urlparse.urlparse(controlURL['web'])
            controlHostName = control.hostname
            if hostname == controlHostName:
#                print 'controlHostName:'
#                print controlHostName
#                print '\n'
                tag=1
                break
#        while 1:
#            abandon = web.readline()
#            abandonurl = urlparse.urlparse(abandon)
#            print 'abandonurl:'
#            print abandonurl.hostname
#            print '\n'
#            
#            print 'hostname:'
#            print hostname
#            print '\n'
#            if abandonurl.hostname == hostname:
#                tag = 1
#                print 'find tag'
#                break
#            if not abandon:
#                break
        
        port="80"
        if hostname.find(':') >0:
            addr,port=hostname.split(':')
#            print 'addr port:'
#            print addr
#            print port
#            print '\n'
        else:
            addr=hostname
        port=int(port)
        
#        
#        print 'changeto:'
#        print changeto
#        print '\n'
#        
#        print 'headers[path]:'
#        print self.headers['path']
#        print '\n'
        for i in iplist:
            if localip == i:
                legalip=1
                break
            pass
        if legalip==0 and hostname!='today.hit.edu.cn':
            self.source.send('HTTP/1.1 302 Moved Temporarily\r\nLocation: http://today.hit.edu.cn\r\n\r\n')
            return
        if tag == 0 :
#            print 'addr:'
#            print addr
#            print '\n'
#            
#            print 'port:'
#            print port
#            print '\n'
            ip=socket.getaddrinfo(addr,port)
            
            print 'ip:'
            print ip[0][4][0]
            self.destnation.connect((ip[0][4][0],port))
            data="%s %s %s\r\n" %(self.headers['method'],self.headers['path'],self.headers['protocol'])
            print 'data:'
            print data+self.request
            print '\n'
            self.destnation.send(data+self.request)
        else:
            self.source.send('HTTP/1.1 302 Moved Temporarily\r\nLocation: http://www.tsinghua.edu.cn\r\n\r\n')
        #print data+self.request
    def renderto(self):
        readsocket=[self.destnation]
        while True:
            data=''
            (rlist,wlist,elist)=select.select(readsocket,[],[],2)
            if rlist:
                data=rlist[0].recv(20480)
                if len(data)>0:
                    self.source.send(data)
                else:
                    break
    def run(self):
        self.get_headers()
        self.conn_destnation()
        if tag==1:
            return
        self.renderto()
class startServer(object):
    def __init__(self,host,port,handler=GetImformation):
        self.host=host
        self.port=port
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host,port))
        self.server.listen(20)
        self.handler=handler
    def start(self):
        while True:
            try:
                conn,addr=self.server.accept()
                thread.start_new_thread(self.handler,(conn,addr))
            except:
                pass
if __name__=='__main__':
    s=startServer('127.0.0.1',8080)
    s.start()
            
