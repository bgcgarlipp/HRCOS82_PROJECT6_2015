import cherrypy
import json
import base64
import subprocess
import os

class AUserver(object):
    @cherrypy.expose
    def index(self):
        return "Nothing here"

    
    def pushImage(self,image):
        #data = json.loads(data)
        print("data to print")
        f =open("tes_raw.jpg","wb")
        f.write(image)
        f.close()
        jpg = base64.b64decode(image)
        f =open("/home/bernhardt/code/autime/assets/predictAU/image.jpg","wb")
        f.write(jpg)
        f.close()
        f =open("image.jpg","wb")
        f.write(jpg)
        f.close()
        os.chdir('/home/bernhardt/code/autime/assets/')
        #svm = subprocess.subprocess.check_output("cd /home/bernhardt/code/autime/assets/ && python parseAU.py", shell=True)
        os.chdir('/home/bernhardt/code/autime/assets/')
        p1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
        print p1.communicate()[0]
        p1 = subprocess.Popen(["python", "parseAU.py"], stdout=subprocess.PIPE)
        svm = p1.communicate()[0]
        os.chdir('/home/bernhardt/code/python_cnn_release')
        p1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
        print p1.communicate()[0]
        p1 = subprocess.Popen(['sudo',"python", "AU_CNN_evaluate_single.py","/home/bernhardt/code/autime/assets/predictAU/image1.jpg"], stdout=subprocess.PIPE)
        p1.wait()
        f = open("output.txt","r")
        cnn= f.read()
        print cnn,svm
        return json.dumps({"cnn":cnn,"emo":"SAD","svm":svm})
    pushImage.exposed = True


    @cherrypy.expose
    def test(self):
        print("Yaya")
        return json.dumps("yes")

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
if __name__ == '__main__':

    app = AUserver()
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
    cherrypy.quickstart(app, '/', {'global':{'server.socket_host': '0.0.0.0',
                        'server.socket_port': 6700,
                       },'/': {'tools.CORS.on': True},'/js':{'tools.staticdir.on': True,'tools.staticdir.dir': 'js'},'/html':{'tools.staticdir.on': True,'tools.staticdir.dir': 'html'}})
    cherrypy.config.update()
    

