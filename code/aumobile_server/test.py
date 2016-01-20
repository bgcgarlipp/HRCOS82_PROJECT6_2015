import subprocess
import os
os.chdir('/home/bernhardt/code/python_cnn_release')
p1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
print p1.communicate()[0]
p1 = subprocess.Popen(['sudo',"python", "AU_CNN_evaluate_single.py","/home/bernhardt/code/autime/assets/predictAU/image.jpg"], stdout=subprocess.PIPE)
p1.wait()
f = open("output.txt","r")
print f.read()
f.close()

