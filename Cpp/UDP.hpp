#pragma once
#include <cstddef>
#include <cstring>
#include <stdio.h>
#include <string>
#include <sys/types.h>
#include <vector>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>  /* Needed for getaddrinfo() and freeaddrinfo() */
#include <unistd.h>
#include <iostream>
#include <chrono>

// needed OSI headers
#include "osi_groundtruth.pb.h"
#include "osi_version.pb.h"
#include "osi_common.pb.h"
#include "osi_object.pb.h"


#define OSIPORT 48198
#define RESPONSEPORT 53995
#define OSIMAXUDPSIZE 8208 

struct Buffer
//Buffer for individual datagrams comming in
{
	int counter;
	unsigned int datasize;
	char data[OSIMAXUDPSIZE];
};

struct OSItoDM
// Structure used to transfer needed data from OSI GT to DM
{
    double timestamp;
	int egoLane;
    double egoPosX;
    double egoSpeed;
    double egoAcc;
    double egoLength;
	int targetLane;
    double targetPosX;
    double targetSpeed;
    double targetAcc;
    double targetLength;
    double targetWidth;
};

struct DMMessage
// The used structure to respond to ESMINI
{   
    unsigned int version = 1;
    unsigned int inputMode = 1;
    unsigned int objectId = 0;
    unsigned int frameNumber = 0;
    double throttle;       // range [0, 1]
    double brake;          // range [0, 1]
    double steeringAngle;  // range [-pi/2, pi/2]
};


class UDP
{public:
    UDP(float timeout=2, std::string const& ip = "127.0.0.1");
    ~UDP(){}; // add close socket
    void respondToESMINI(int id = 0, double brakeresponse = 0.0, double throttle = 1.0, double steeringangle = 0.0);
    void receiveOSIGT();

//  protected:
    OSItoDM data;
    std::string ipAddress;
    int socketFD;
    // to receive OSI GT from ESMINI
    struct sockaddr_in receiverAddr;
    socklen_t receiverAddrSize;
    Buffer buffer;
    size_t bytesReceived;
    bool done = false;
    int counter,  headersize = 8;
    unsigned int size;
    std::vector<char> compMSG;
    osi3::GroundTruth GT;
  	struct sockaddr_in responseAddr;
    socklen_t responseAddrSize;
    DMMessage response;
    bool firstGTReceived = false;
};



