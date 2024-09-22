# This is a minimalistic example of how to create build files for an application 
# making use of the esmini shared library.
# 
# Make sure that the headerfile esminiLib.hpp and library esminiLib 
# (exact filename depending on platform) is available, either in this folder or in 
# the original location (relative this folder).

cmake_minimum_required (VERSION 3.5.0 FATAL_ERROR)
set(CMAKE_CXX_FLAGS "-O3 ") #-Wall -Wpedantic") # -ggdb -falign-functions=1 -falign-jumps=1 -falign-loops=1 -falign-labels=1
set(TARGET DM)

include_directories(. ../resources/include)

link_directories(. ../resources/lib )


project(${TARGET})

# Windows: Uncomment next line to completely suppress the console
# set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")

# add_executable(${TARGET} DM.cpp UDP.cpp)
add_executable(${TARGET} DM.cpp UDP.cpp Benchmark.cpp)
target_link_libraries(${TARGET} esminiLib open_simulation_interface_pic protobuf )

# Copy the executable to the main folder
install(TARGETS ${TARGET} DESTINATION ..)

