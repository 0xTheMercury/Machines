### [*] Machine Name ==> Fluffy
### [*] Difficulty ==> Easy
### [*] OS ==> Windows
### [*] Points ==> 20 

#

### [*] Machine Description
  * As is common in real life Windows pentests, you will start the Fluffy box with credentials for the following account: `j.fleischman / J0elTHEM4n1990!`

#

### [*] Summary:
  * This machine talks about vulnerable version of windows lead to leaked credentials, And misconfigured active directory lead to shadow credentials attack of any user in specified group and getting user flag, And vulnerable AD CS (Active Directory Certificate Service) lead to privilege escalation to administrator and getting root flag. 

#

### [*] Scanning:
![alt text](Pics/Screenshot_2025-08-09_07-35-45.png)
  * Active Directory with Kerberos.
  * Domain Controllers `FLUFFY.HTB` & `DC01.FLUFFY.HTB`.
  * SMB is opened.

### [*] SMB Enumeration:
  * I used `smbmap` to know my permissions in SMB.
![alt text](Pics/Screenshot_2025-08-09_07-56-09.png)
  * I have `READ, WRITE` permissions on `IT` directory.
  * Log in SMB using `smbclient` to enumerate the directory.
![alt text](Pics/Screenshot_2025-08-09_07-56-49.png)
  * I found interesting PDF file `Upgrade_Notice.pdf`, I downloaded to discover what's inside.

### [*] PDF File Enumeration:
  * This file talks about high-impact CVEs publicly disclosed and Windows version that's running on this machine is vulnerable of them, And there's list of the CVEs inside the file.
![alt text](Pics/Screenshot_2025-08-09_08-19-02.png)
  * After spending few time to understand these CVEs, I decided to use this CVE `CVE-2025-24071`.

### [*] Used CVE Explaination `CVE-2025-24071`:
  * Hackers can use this CVE on vulnerable versions of windows to leak the credentials of the victim.
  * It works when you inject vulnerability's payload inside file with this extension `.library-ms` and compress it inside `ZIP` file and put the `ZIP` file on machine, Once the victim opened or decompressed it, You'll receive his credentials `NTLMv2 Hash` on your server (listener).

### [*] Leaking Credentials Steps:
  * I used this script to make vulnerable `ZIP` file.
![alt text](Pics/Screenshot_2025-08-10_12-51-52.png)
![alt text](Pics/Screenshot_2025-08-10_13-03-37.png)
  * Put the file on the machine using SMB.

![alt text](Pics/Screenshot_2025-08-10_13-33-01.png)
  * Wait for few time, Once the victim decompressed it, You'll receive his credentials `NTLMv2 Hash` on your listener (I used responder tool).

![alt text](Pics/Screenshot_2025-08-10_13-34-45.png)
![alt text](Pics/Screenshot_2025-08-10_13-33-56.png)
  * The victim's username is `p.agila`.
  * I cracked the hash with `john the ripper` and got a password.

![alt text](Pics/Screenshot_2025-08-10_13-57-05.png)

### [*] Active Directory Map:
  * Once i have credentials, I used `bloodhound-python` to get active directory data and details to upload it into `BloodHound` and see mape of active directory.
![alt text](Pics/Screenshot_2025-08-11_06-32-35.png)
  * I searched for username of our victim and put `Owning` mark on it.
![alt text](Pics/Screenshot_2025-08-11_06-41-57.png)
  * I enumerated the shortest path to `DOMAIN ADMINS` group using owned credentials and enumerated the users of `DOMAIN ADMINS` group and users of `SERVICE ACCOUNTS` group.
![alt text](Pics/Screenshot_2025-08-11_06-43-55.png)
![alt text](Pics/Screenshot_2025-08-11_07-02-30.png)
![alt text](Pics/Screenshot_2025-08-14_09-09-57.png)
  * When i was looking at reaching `DOMAIN ADMINS`'s map, I found that `SERVICE ACCOUNTS` group has `Generic Write` permission on `WINRM_SVC` user, I thought that maybe there's something useful on this user.

### Getting Access On `WINRM_SVC`:
  * First, I need to add myself to `SERVICE ACCOUNTS` group.
  * Perform shadow credentials attack to make another credential and get access on `WINRM_SVC` without knowing anyone.
  * And finally, Log in with shadow creds of this user by `evil-winrm`.
![alt text](Pics/Screenshot_2025-08-12_02-56-33.png)
![alt text](Pics/Screenshot_2025-08-13_15-30-09.png)
![alt text](Pics/Screenshot_2025-08-13_08-38-41.png)
  * BOOM, We got user flag

### [*] Privilege Escalation For Getting Root:
  * When i was enumerating users of `SERVICE ACCOUNTS` group, I discovered a user that manage certificate authority service `CA_SVC`, I tried to make shadow credentials on this user too and it works well and got credentials.
  * I thought maybe there's vulnerability in CA "Certificate Authorities" of active directory.
  * When i scanned vulnerabilities with `CA_SVC` credentials, I found that CA is vulnerable to `ESC16`.
![alt text](Pics/Screenshot_2025-08-13_16-02-41.png)
![alt text](Pics/Screenshot_2025-08-14_08-19-19.png)
![alt text](Pics/Screenshot_2025-08-14_08-19-38.png)

### [*] `ESC16` Vulnerability's Explaination:
  * This occures when security extension is disabled, This extension put Object's SIDs (Security Identifier) to make strong identity for users and services accounts, When it's disabled, Active Directory falls back to legacy mapping, typically using UPN (User Principle Name).
  * So hackers can manipulate UPN and get access on high-privilege users.

### [*] Steps To Exploit `ESC16` Vulnerability:
  * Change your victim's UPN to another user, `administrator` in this case.
  * Send request to get certificate as this user (administrator), You'll get administrator certificate.
  * Return UPN to the normal to avoid errors.
  * Request to get credentails by the certificate.
  * Log in as administrator with `evil-winrm`.

![alt text](Pics/Screenshot_2025-08-14_09-09-57.png)
![alt text](Pics/Screenshot_2025-08-14_09-30-48.png)
![alt text](Pics/Screenshot_2025-08-14_09-34-20.png)
![alt text](Pics/Screenshot_2025-08-14_10-00-00.png)
![alt text](Pics/Screenshot_2025-08-14_10-01-27.png)
![alt text](Pics/Screenshot_2025-08-14_17-04-21.png)
![alt text](Pics/Screenshot_2025-08-14_17-08-41.png)
  * BOOM, We got root flag.