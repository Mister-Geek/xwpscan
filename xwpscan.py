#!/usr/bin/env python

#+--------------------------------------------------------------------+
# Wordpress scanner
# Copyright (c) 2013 4-Sectors
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#+--------------------------------------------------------------------+

import sys
import os
import httplib

class wordlist:
        '''Word_lists'''
        wpplugins = 'wp_plugins.txt'

def clear():
  '''Clear screen'''
        if os.name == 'posix':
                cmd = 'clear'
        else:
                cmd = 'cls'
        os.system(cmd)

def MSG(msg):
        if msg == 'wprun':
                print('[*] Starting Wordpress Scanner ...')
                print('[-] Enumerating... (-)> %s'%(sys.argv[2]))
                print('-===============================================================-')
        elif msg == 'plugfound':
                print('[!] Found Plugin page @> ')
		
def usage():
        print '''
:: Usage ::
      $ ./xwpscan.py -u <url>
      <url> in format -> http://www.wordpress.com

If the wordpress installed path is not in root directory, you have to supply the path with "-p" argument.
      E.g. If the wordpress path is http://www.site.com/blog/ , your cmd will be...
      $ ./xwpscan.py -u http://www.site.com -p /blog
        '''

def banner():
	print '''
 __      __          ____                               
/\ \  __/\ \        /\  _`\                             
\ \ \/\ \ \ \  _____\ \,\L\_\    ___     __      ___    
 \ \ \ \ \ \ \/\ '__`\/_\__ \   /'___\ /'__`\  /' _ `\  
  \ \ \_/ \_\ \ \ \L\ \/\ \L\ \/\ \__//\ \L\.\_/\ \/\ \ 
   \__\___x___/\ \ ,__/\ `\____\ \____\ \__/.\_\ \_\ \_\
      
                \ \_\                                  
                 \/_/beta v.0.1 (-) Mr.Geek (-) 4Sectors
	'''

class wpscan(object):
        def __init__(self,url,path,wordlist):
                self.url = url
                self.subpath = path
                self.wordlist = wordlist
                self.filecontent = self.readwl()
                self.count = 0
                self.foundplugins = []
                self.readme = "/readme.html"
                
        def readwl(self):
                try:
                    lines = [line.strip() for line in open(self.wordlist)]
                    return lines
                except IOError:
                    print 'couldn\'t open file...'
                    sys.exit(0)

        def enumer(self):
                try:
                        if self.subpath != 0: self.readme = self.subpath+self.readme
                        conn = httplib.HTTPConnection(self.url)
                        conn.request("GET",self.readme)
                        resp = conn.getresponse()
                        if resp.status == 200:
                                print '[!] Readme file found at %s'%(self.url+self.readme)
                                print '-=================================================-'
                        else:
                                pass

                except Exception,e:
                        print('[*] General Error occurs ...')
                        print('[-] Enumeration fails ...')
                        print('[-] Continue to plugin finder...')
                        pass
        
        def brute(self):
                try:
                        for path in self.filecontent:
                           try:
                                if self.subpath == 0: self.path = "/wp-content/plugins/"+path
                                else: self.path = self.subpath+"/wp-content/plugins/"+path
                                conn = httplib.HTTPConnection(self.url)
                                conn.request("GET",self.path)
                                resp = conn.getresponse()
                                if resp.status == 200:
                                        MSG('plugfound')
                                        print '[-]> %s%s'%(self.url,self.path)
                                        self.count += 1
                                        self.foundplugins.append('%s%s'%(self.url,self.path))                                
                                else:
                                        pass
                           except KeyboardInterrupt:
                                   print '[~] KeyboardInterrupt'
                                   print '[~] Exiting ...'
                                   self.printf()
                                   sys.exit(0)
                                   
                except Exception,e:
                                print('[*] General Error occurs ...')
                                print('[-] Terminating ...')
                                sys.exit(0)
                
        def run(self):
                MSG('wprun')

        def printf(self):
                print '=========================================='
                print '[*] Total Found wordpress Plugin page or pages (-)> %s'%(self.count)
                for pluginfound in self.foundplugins:
                    print pluginfound       

def WpScan(domain,path):
        '''Wordpress scanner function'''
        if '://' in domain:
                url = domain.replace("http://","")
        else: url = domain
        _path = path
        w = wpscan(url,_path,wordlist.wpplugins)
        w.run()
        w.enumer()
        w.brute()
        w.prinf()
        pass

def main():
	'''Main function'''
        if len(sys.argv) == 3 and sys.argv[1] == '-wp' and sys.argv[2].startswith('http://'):
                WpScan(sys.argv[2],0)

        elif len(sys.argv) == 5 and sys.argv[1] == '-wp' and sys.argv[2].startswith('http://') and sys.argv[3].startswith('-p'):
                WpScan(sys.argv[2],sys.argv[4])
        
        else:
                usage()

if __name__ == "__main__":
	clear()
	banner()
	main()
