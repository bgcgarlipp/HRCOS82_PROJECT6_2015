import cv2
import sys

class FaceCrop:
    #class level paramters
    cascPath = 'haarcascade_frontalface_default.xml'
    eyecascpath = 'haarcascade_eye.xml'
    
    def __init__(self):
        # Create the haar cascade
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        
    def getCrop(self,filename):
        # Read the image
        image = cv2.imread(filename,0)
        return self._getFaces(image)
        
#     def _greyscaleImage(self,image):
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         return gray
    
    def _getFaces(self,image):
        # Detect faces in the image
        added = False
        faces = self.faceCascade.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        # Draw a rectangle around the faces
        _facelist = []
        print image        
        print "Faces found"
        print faces
        if len(faces) == 0 or len(faces) > 1:
            #print "no face"
            _facelist.append(image)
        else:
            for (x, y, w, h) in faces:
                #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #print image.shape
                #print x,w,x+w,y+h
                cropped = image[y:y+h,x:x+w]
                eyes = self.eye_cascade.detectMultiScale(cropped)
                # only append when eyes are found
                for (ex,ey,ew,eh) in eyes:
                    added = True
                    cropped = image[y:y+h,x:x+w]
                    _facelist.append(cropped)
                    break
            if not added:
                _facelist.append(cropped)

        #Assume first one is only face
        if _facelist:
            return _facelist[0]
        else:
            return None

