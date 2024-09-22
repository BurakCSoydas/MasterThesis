
from osi3.osi_groundtruth_pb2 import GroundTruth
from socket import socket, AF_INET, SOCK_DGRAM
import struct

osiPort = 48198
responsePort = 53995


class DMData:
    # DMData groups data the dm is making use of and  makes it easier to work with
    def __init__(self):
        self.timestamp: float
        self.egoLane: int
        self.egoPosX: float
        self.egoSpeed: float
        self.egoAcc: float
        self.egoLength: float
        self.targetLane: int
        self.targetPosX: float
        self.targetSpeed: float
        self.targetAcc: float
        self.targetLength: float
        self.targetWidth: float


class objectControlResponse:
    """objectControlResponse uses the following parameter to communicate to
    ESMINI how the external controller  of given object repsonds."""

    def __init__(self):
        self.version = 1
        self.inputMode = 1
        self.objectId = 0
        self.frameNumber = 0
        self.steeringAngle = None
        self.throttle = None
        self.brake = None


class UDP:
    """This class provides underlying functions to the driver model and
    enables the driver model to communicate with ESMINI using the
    open simulation interface standard and makes some data out of the
    simulation available for the driver model."""

    def __init__(self, ip="127.0.0.1", timeout=500):
        """Creates two UDP sockets for the driver model to use to communicate
        (receive and respond) with ESMINI.

        Arguments define timeout behaviour and ip to connec to.
        DEFAULT: timeout = 500, ip = local (127.00.0.1)"""
        # socket and attributes needed to receive
        self.socketFD = socket(AF_INET, SOCK_DGRAM)
        self.buffersize = 8208
        if timeout >= 0:
            self.socketFD.settimeout(timeout)
        self.socketFD.bind((ip, osiPort))
        self.osiMsg = GroundTruth()
        self.DMData = DMData()
        self.responseMSGAddr = (ip, responsePort)
        self.responseMSG = objectControlResponse()
        self.firstGTReceived = False

    def close(self):
        self.socketFD.close()

    def receiveOSIGT(self):
        """Receives the Open Simulation Interface data from ESMINI and stores
        needed parameters."""

        done = False
        nextIndex = 1
        completeMsg = b""

        # Large nessages might be split in multiple parts
        # esmini will add a counter to indicate sequence number 0, 1, 2...
        # negative counter means last part and message is now complete
        while not done:
            # receive header
            msg, _ = self.socketFD.recvfrom(self.buffersize)

            # extract message parts
            headerSize = 4 + 4  # counter(int) + size(unsigned int)
            counter, size, frame = struct.unpack(
                "iI{}s".format(len(msg) - headerSize), msg
            )

            if not (len(frame) == size == len(msg) - 8):
                print("Error: Unexpected invalid lengths")
                break

            if counter == 1:  # new message
                completeMsg = b""
                nextIndex = 1

            # Compose complete message
            if counter == 1 or abs(counter) == nextIndex:
                completeMsg += frame
                nextIndex += 1
                if counter < 0:
                    # negative counter number indicates end of message
                    done = True
            else:
                nextIndex = 1  # out of sync, reset

        # Parse Open Simulation Interface Data
        self.osiMsg.ParseFromString(completeMsg)

        # store needed data
        self.DMData.timestamp = round(
            float(
                str(self.osiMsg.timestamp.seconds)
                + "."
                + str(self.osiMsg.timestamp.nanos).zfill(9)
            ),
            2,
        )
        self.DMData.egoLane = self.osiMsg.moving_object[0].assigned_lane_id[0].value
        self.DMData.egoPosX = self.osiMsg.moving_object[0].base.position.x
        self.DMData.egoSpeed = self.osiMsg.moving_object[0].base.velocity.x
        self.DMData.egoAcc = self.osiMsg.moving_object[0].base.acceleration.x
        self.DMData.egoLength = self.osiMsg.moving_object[0].base.dimension.length
        self.DMData.targetLane = self.osiMsg.moving_object[1].assigned_lane_id[0].value
        self.DMData.targetPosX = self.osiMsg.moving_object[1].base.position.x
        self.DMData.targetSpeed = self.osiMsg.moving_object[1].base.velocity.x
        self.DMData.targetAcc = self.osiMsg.moving_object[1].base.acceleration.x
        self.DMData.targetLength = self.osiMsg.moving_object[1].base.dimension.length
        self.DMData.targetWidth = self.osiMsg.moving_object[1].base.dimension.width

        self.firstGTReceived = True

    def respondToESMINI(self, id=0, brake=0.0, throttle=1.0, steeringAngle=0.0):
        """Sends the driver model response to ESMINI. Data stored in
        responseMSG is converted into a C structure.
        Takes id of object to control, and brake, throttle as well
        steeringAngle. Default arguments are set to accelarate ego
        object to full speed"""

        self.responseMSG.objectId = id
        self.responseMSG.throttle = throttle
        self.responseMSG.brake = brake
        self.responseMSG.steeringAngle = steeringAngle

        # create temporary variable to as handle for C structure
        responseMSG = struct.pack(
            "iiiiddd",
            self.responseMSG.version,
            self.responseMSG.inputMode,
            self.responseMSG.objectId,
            self.responseMSG.frameNumber,
            self.responseMSG.throttle,
            self.responseMSG.brake,
            -self.responseMSG.steeringAngle,
        )

        # send message if C structure was created successfully
        if responseMSG is not None:
            self.socketFD.sendto(responseMSG, self.responseMSGAddr)
            self.responseMSG.frameNumber += 1
        else:
            print("responseMSG is None")

