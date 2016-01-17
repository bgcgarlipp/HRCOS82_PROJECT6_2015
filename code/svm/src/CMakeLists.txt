
IF (MSVC)
  # Setting the xecutables as console applications
  SET (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /SUBSYSTEM:CONSOLE")
ENDIF (MSVC)

include_directories(${SRCDIR}/training)
include_directories(${SRCDIR}/facedetector)
include_directories(${SRCDIR}/gaborbank)
include_directories(${SRCDIR}/utils)
include_directories(${SRCDIR}/detector)

SET(AUTIME_LIB_FILES "")
SET(AUTIME_H_FILES "")

add_subdirectory(training)
add_subdirectory(facedetector)
add_subdirectory(gaborbank)
add_subdirectory(dataset)
add_subdirectory(utils)
add_subdirectory(detector)

find_package(OpenCV COMPONENTS opencv_core opencv_ml opencv_imgproc
  opencv_highgui opencv_objdetect REQUIRED)

# AUtime library
add_library(autime SHARED  facedetector/FaceDetector.cpp
                            detector/GenDetector.cpp
                            detector/BoostGenDetector.cpp
                            detector/SVMGenDetector.cpp
                            training/Classifier.cpp
                            training/AdaBoostClassifier.cpp
                            training/SVMClassifier.cpp
                            training/FacePreProcessor.cpp
                            gaborbank/GaborBank.cpp
                            gaborbank/GaborKernel.h
                            utils/matrix_io.cpp
                            utils/string_utils.cpp
                                                  )

target_link_libraries(autime ${OpenCV_LIBS})

INSTALL(TARGETS autime DESTINATION ${ASSETDIR})

INSTALL(FILES facedetector/FaceDetector.h
               utils/matrix_io.h 
               utils/string_utils.h
               gaborbank/GaborBank.h 
               gaborbank/GaborKernel.h
               detector/GenDetector.h 
               detector/BoostGenDetector.h 
               detector/SVMGenDetector.h 
               detector/ConfusionMatrix.h
               training/FacePreProcessor.h 
       DESTINATION "${HEADERDIR}")

