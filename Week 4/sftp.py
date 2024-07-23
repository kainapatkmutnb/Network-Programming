import paramiko

hostname = "172.27.118.48"
username = "kainapat"
passwd = "1234"
port = 22

try:

    p. connect(username=username, password=passwd)
    print("[*] Connected to " + hostname + "via SSH")
    sftp = paramiko.SFTPClient.from_transport(p)
    print("[*] Starting file download")
    sftp.get("/home/kainapat/test.txt","C:\Users\guy26\Downloads\d.txt")
    print("[*] File download complete")
    print("[*] Starting file upload")
    sftp.put("C:\Users\guy26\Downloads\d.txt","/home/kainapat/u.txt")
    print("[*] File upload complete")
    p.close()
    print("[*] Disconnected from server")

except Exception as err:
    print("[!] " +str(err))