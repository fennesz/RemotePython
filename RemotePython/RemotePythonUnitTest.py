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
# LOCAL_UNAME should be the result you get from running 'uname -s' on your local machine
LOCAL_UNAME = 'Darwin'

class Test(unittest.TestCase):
    ''' Class containing unittests for the RemotePython module '''

    def testRunScript(self):
        ''' Test execution of a python script on a remote machine'''
#         print self.testRunScript.__doc__
        obj = RemotePython('remote_script.py', ip=IP, user=USER)
        ret = obj.runScript()
        self.assertIn('the call worked', ret)

    def testRunCommand(self):
        ''' Run uname on localhost, for OSX this is Darwin'''
        obj = RemotePython()
        ret = obj.runCommand('uname', '-s')
        self.assertEqual(ret, LOCAL_UNAME)

    def testRemoveScript(self):
        ''' Test if hidden function '__removeScript' works '''
#         print self.testRemoveScript.__doc__
        obj = RemotePython()
        before = int(obj.runCommand('ls', '-l', '|', 'wc', '-l'))
        obj.runCommand('touch', 'test.txt')
        middle = int(obj.runCommand('ls', '-l', '|', 'wc', '-l'))
        self.assertEqual(middle, before+1, "No file created, file already existed") # Check if we created a new file
        obj._RemotePython__removeScript('test.txt')
        after = int(obj.runCommand('ls', '-l', '|', 'wc', '-l'))
        self.assertEqual(before, after) # Check if we removed the created file

    def testPrint(self):
        ''' Print the default object '''
#         print self.testPrint.__doc__
        print RemotePython()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMain']
    unittest.main()
