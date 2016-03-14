'''
Created on Mar 6, 2016

@author: allexveldman
'''
import unittest
from RemotePython import RemotePython

IP = '192.168.0.106'

class Test(unittest.TestCase):
    ''' Class containing unittests for the RemotePython module '''

    def testRunScript(self):
        ''' Test execution of a python script on a remote machine '''
#         print self.testRunScript.__doc__
        obj = RemotePython('remote_script.py')#, ip=IP, user='allex')
        ret = obj.runScript()
        self.assertIn('the call worked', ret)

    def testRunCommand(self):
        ''' Run uname on localhost, for OSX this is Darwin'''
#         print self.testRunCommand.__doc__
        obj = RemotePython()
        ret = obj.runCommand('uname', '-s')
        self.assertEqual(ret, 'Darwin\n')

#     def testRunCommandExcept(self):
#         ''' Run unknown command on localhost, should raise RemotePythonError'''
# #         print self.testRunCommandExcept.__doc__
#         obj = RemotePython()
#         self.assertRaises(obj.RemotePythonError, obj.runCommand, 'sshh', '-h')

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
#         print RemotePython()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMain']
    unittest.main()
