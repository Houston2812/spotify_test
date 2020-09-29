import argparse, random, socket, sys
from datetime import datetime
MAX_BYTES = 65535

class Server():
    interface = "0.0.0.0"
    port = 1060
    
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.interface, self.port))
        print(f'Listening at {sock.getsockname()}')

        while True:
            data, address = sock.recvfrom(MAX_BYTES)
            if random.random() < 0.5:
                print('Pretending to drop packet from {}'.format(address))
                continue
            text = data.decode('ascii')
            print(f'The client at {address} says {text}')

            text = f'Song {text} is delivered'
            data = text.encode('ascii')
            sock.sendto(data, address)

class Client():
    hostname = "0.0.0.0"
    port = 1060

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.hostname, self.port))
        print(f'Client socket name is {sock.getsockname()}')
        
        delay = 0.1
        text = 'AC/DC - Highway to Hell'
        data = text.encode('ascii')

        while True:
            sock.send(data)
            print(f'Waiting up to {delay} seconds for a reply')
            sock.settimeout(delay)
            try:
                data = sock.recv(MAX_BYTES)
            except socket.timeout as exc:
                time = datetime.now()
                time_in_mins = time.hour * 60 + time.minute
               

                if (time_in_mins >= 12*60 and time_in_mins <= 17*60) or (time_in_mins >= 0  and time_in_mins < 12*60):
                    delay *= 2
                elif time_in_mins > 17*60 and time_in_mins <= 23*60+59:
                    delay *= 3
               
                if time_in_mins >= 12*60 and time_in_mins <= 17*60:
                        if delay > 2.0:
                            raise RuntimeError('I think server is down') from exc
                if time_in_mins > 17*60 and time_in_mins <= 23*60+59:
                        if delay > 4.0:
                            raise RuntimeError('I think server is down') from exc   
                if time_in_mins >= 0  and time_in_mins < 12*60:
                        if delay > 1.0:
                            raise RuntimeError('I think server is down') from exc     
            else:
                break
        text = data.decode('ascii')
        print(f'The server says { text }')

if __name__ == "__main__":
    choices = {'client': Client, 'server': Server}
    parser = argparse.ArgumentParser(description = 'Test of the local spotify server')
    parser.add_argument('role', choices=choices, help = 'Which role to play')
    parser.add_argument('host', help='Interface the server listens at; host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')

    args = parser.parse_args()
    class_ = choices[args.role](args.host, args.p)
    class_.run()
 

