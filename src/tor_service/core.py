"""Tor Hidden Service Core"""
import subprocess,os,json,time,socket,hashlib
from datetime import datetime

class TorController:
    def __init__(self,control_port=9051,password=None):
        self.control_port=control_port
        self.password=password
    
    def get_circuit_info(self):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(("127.0.0.1",self.control_port))
            if self.password:
                s.send(f'AUTHENTICATE "{self.password}"\r\n'.encode())
                s.recv(256)
            s.send(b"GETINFO circuit-status\r\n")
            response=s.recv(4096).decode()
            s.send(b"QUIT\r\n")
            s.close()
            return {"circuits":response.count("BUILT"),"raw":response[:500]}
        except: return {"circuits":0,"error":"Cannot connect to Tor control port"}
    
    def new_circuit(self):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(("127.0.0.1",self.control_port))
            if self.password:
                s.send(f'AUTHENTICATE "{self.password}"\r\n'.encode())
                s.recv(256)
            s.send(b"SIGNAL NEWNYM\r\n")
            resp=s.recv(256).decode()
            s.close()
            return "250 OK" in resp
        except: return False

class HiddenService:
    def generate_torrc(self,service_dir,virtual_port=80,target_port=8080):
        return f"""HiddenServiceDir {service_dir}
HiddenServicePort {virtual_port} 127.0.0.1:{target_port}
"""
    
    def get_onion_address(self,service_dir):
        hostname_file=os.path.join(service_dir,"hostname")
        if os.path.exists(hostname_file):
            return open(hostname_file).read().strip()
        return None

class TorChecker:
    def check_tor_running(self):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(3)
            result=s.connect_ex(("127.0.0.1",9050))
            s.close()
            return result==0
        except: return False
    
    def check_exit_node(self):
        try:
            import urllib.request
            proxy=urllib.request.ProxyHandler({"http":"socks5h://127.0.0.1:9050","https":"socks5h://127.0.0.1:9050"})
            opener=urllib.request.build_opener(proxy)
            resp=opener.open("https://check.torproject.org/api/ip",timeout=15)
            data=json.loads(resp.read())
            return data
        except Exception as e: return {"IsTor":False,"error":str(e)}
