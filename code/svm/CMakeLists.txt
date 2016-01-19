cmake_minimum_required(VERSION 2.8)

project(autime)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

set(ASSETDIR "${autime_SOURCE_DIR}/assets" )
set(HEADERDIR "${autime_SOURCE_DIR}/include" )
set(SRCDIR "${autime_SOURCE_DIR}/src" )

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage" )
add_definitions(-ggdb -gdwarf-2)

add_subdirectory(src)


