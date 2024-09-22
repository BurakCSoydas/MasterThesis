#include "UDP.hpp"
#include <chrono>
#include <cstdio>
#include <cstring>


UDP::UDP(float timeout, std::string const& ip):ipAddress(ip)
{
  headersize = 2*sizeof(int);
  compMSG.reserve(OSIMAXUDPSIZE*10);
  receiverAddrSize = sizeof(receiverAddr);
  // std::cout << ipAddress << std::endl;
  if ((socketFD= socket(AF_INET,SOCK_DGRAM, IPPROTO_UDP)) < 0)
  {
      perror("Socket failed: ");
      exit(EXIT_FAILURE);
  }  
  // ESMINI sends datagrams to port 48198 and the provided IP when opening the OSI. Binding the socket to that address enables
  // receiving the sent datagrams.
  // prepare structaddr for binding to the address 
  memset((char*)&receiverAddr, 0, sizeof(receiverAddrSize));
	receiverAddr.sin_family = AF_INET;
	receiverAddr.sin_port = htons(OSIPORT);
  inet_pton(AF_INET, ipAddress.c_str(), &receiverAddr.sin_addr.s_addr);

	// binding socket to address (receive packages)
	if(bind(socketFD,(const sockaddr*) &receiverAddr, receiverAddrSize)<0)
	{
		perror("Binding failed: ");
		exit(EXIT_FAILURE);
	}
  // set up socket as sender
  responseAddrSize = sizeof(responseAddr);
	memset((char*)&responseAddr, 0, responseAddrSize);
	responseAddr.sin_family = AF_INET;
	responseAddr.sin_port = htons(RESPONSEPORT);
	inet_pton(AF_INET, ipAddress.c_str(), &responseAddr.sin_addr.s_addr);  
}

void UDP::receiveOSIGT()
{
  bytesReceived = 0; //received bytes
	done = false; //condition for composition of msg
	int next_index = 1; //index for composition of msg
	compMSG.clear(); //clear vector 
	//msg can and most likely will be split. With this while loop, we compose the whole msg
	while(not done)
	{	
		bytesReceived = recvfrom(socketFD, &buffer, OSIMAXUDPSIZE,0,nullptr,nullptr);
		if (bytesReceived < 0)
		{
			perror("Error receiving message");
			exit(EXIT_FAILURE);
		}
		
		if(( (bytesReceived - 2*sizeof(int)) != buffer.datasize)) //check if we received the right amount of data per split
		{
			perror("expected size and actual size don't match");
			exit(EXIT_FAILURE);
		}
		if (buffer.counter == 1) //new message
		{
			compMSG.clear();
			next_index = 1;
		}
		if (buffer.counter == 1 || abs(buffer.counter) == next_index) //finally compose the whole msg piece by piece
		{
			compMSG.insert(compMSG.end(), buffer.data, buffer.data + buffer.datasize);
			next_index += 1;
			if(buffer.counter < 0)
			{
				done = true;
			}
		}
		else
		{
			next_index = 1; //reset in case of uncaught error
		}
  }
  // std::cout << "RECEIVING OSI MSG LOOP DONE." << std::endl;
  GT.ParseFromArray(compMSG.data(),compMSG.size());
  std::cout << "GT PARSING DONE." << std::endl;

	// copying needed data into struct to pass into SUT
	std::string sec = std::to_string(GT.timestamp().seconds());
	std::string nano = std::to_string(GT.timestamp().nanos());
	std::string nano0 = std::string(9-nano.length(), '0').append(nano);
	// printf("sec: %s nano: %s  comb: %f\n", sec.c_str(), nano0.c_str(), stod(time));
	data.timestamp = stod(sec + "." + nano0);
	data.egoLane = GT.moving_object(0).assigned_lane_id(0).value();
	data.egoPosX = GT. moving_object(0).base().position().x();
  data.egoSpeed = GT.moving_object(0).base().velocity().x();
	data.egoAcc = GT.moving_object(0).base().acceleration().x();
	data.egoLength = GT.moving_object(0).base().dimension().length();
	data.targetLane = GT.moving_object(1).assigned_lane_id(0).value();
	data.targetPosX = GT.moving_object(1).base().position().x();
	data.targetSpeed = GT.moving_object(1).base().velocity().x();
	data.targetAcc = GT.moving_object(1).base().acceleration().x();
	data.targetLength = GT.moving_object(1).base().dimension().length();
	data.targetWidth = GT.moving_object(1).base().dimension().width();

  firstGTReceived = true;
}

void UDP::respondToESMINI(int id,double brakeresponse, double throttle, double steeringangle)
{
	// setting the response values in struct
  response.objectId = id;
	response.brake = brakeresponse;
	response.throttle = throttle;
	response.steeringAngle = -steeringangle;
  //sending struct as datagrams to 
  int size = sizeof(response);
	sendto(socketFD, (char*) &response, size, 0, (struct sockaddr*)&responseAddr, responseAddrSize);
  response.frameNumber++;
}
