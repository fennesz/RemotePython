'''
Created on Mar 6, 2016

@author: allexveldman
'''
import unittest
from RemotePython import RemotePython
from getpass import getuser

# Change these to your remote machine keys to execute the testRunScript() test on your remote machine
IP = 'localhost'
USER = getuser()

# IP = '192.168.0.106'
# USER = 'allex'

# LOCAL_UNAME should be the result you get from running 'uname -s' on your local machine
LOCAL_UNAME = 'Darwin'

class Test(unittest.TestCase):
    ''' Class containing unittests for the RemotePython module '''

    def testRunScript(self):
        ''' Test execution of a python script on a remote machine'''
#         print self.testRunScript.__doc__
        obj = RemotePython('remote_script.py', ip=IP, user=USER)
        ret = obj.runScript(load_env=True)
        self.assertIn('the call worked', ret)

    def testRunCommand(self):
        ''' Run uname on localhost, for OSX this is Darwin'''
        obj = RemotePython()
        ret = obj.runCommand(['uname', '-s'])
        self.assertEqual(ret, LOCAL_UNAME)
        
    def testLoadEnv(self):
        ''' Run a command with loading the environment, needs a command named 'testCommand' on the target 
        I created a simlink in my /home/allex/bin to the ls command in /bin
        Also create a file or object called ArdPi in the user home dir.'''
        #TODO: change this test so it creates a file and cleans up afterward on the target machine
        obj = RemotePython(ip=IP, user=USER)
        if IP == 'localhost':
            print "Run command on a remote machine or create a simlink on your own machine"
        else:
            ret = obj.runCommand(['testCommand'],load_env=True)
            self.assertIn('ArdPi', ret)

    def testRemoveScript(self):
        ''' Test if hidden function '__removeScript' works '''
#         print self.testRemoveScript.__doc__
        obj = RemotePython()
        before = int(obj.runCommand(['ls', '-l', '|', 'wc', '-l']))
        obj.runCommand(['touch', 'test.txt'])
        middle = int(obj.runCommand(['ls', '-l', '|', 'wc', '-l']))
        self.assertEqual(middle, before+1, "No file created, file already existed") # Check if we created a new file
        obj._RemotePython__removeScript('test.txt')
        after = int(obj.runCommand(['ls', '-l', '|', 'wc', '-l']))
        self.assertEqual(before, after) # Check if we removed the created file

    def testPrint(self):
        ''' Print the default object '''
#         print self.testPrint.__doc__
        print RemotePython()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMain']
    unittest.main()
