# This is a minimalistic example of how to create build files for an application 
# making use of the esmini shared library.
# 
# Make sure that the headerfile esminiLib.hpp and library esminiLib 
# (exact filename depending on platform) is available, either in this folder or in 
# the original location (relative this folder).

cmake_minimum_required (VERSION 3.5.0 FATAL_ERROR)
set(CMAKE_CXX_FLAGS "-O3")
set (CMAKE_CXX_STANDARD 17)
set(TARGET scenarioStart)

include_directories(. ../resources/include)

link_directories(. ../resources/lib )


project(${TARGET})
# Windows: Uncomment next line to completely suppress the console
# set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")

add_executable(${TARGET} scenarioStart.cpp Benchmark.cpp)

target_link_libraries(${TARGET} esminiLib open_simulation_interface_pic protobuf )

# Copy the executable to the main folder
install(TARGETS ${TARGET} DESTINATION ${CMAKE_HOME_DIRECTORY})

