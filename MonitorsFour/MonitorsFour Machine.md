# Stage1: Recon
- HTTP web server on port 80 `monitorsfour.htb`.
- WinRM on port 5985.
- ![alt text](<Pics/Screenshot From 2026-04-23 11-40-38.png>)

### Website Enumeration
- I discover website manually:
	- No Signup, only login page, So i need a valid account.
- After Files and Directories enumeration, I found `/user` page that takes me parameter `/user?token=` to render the user profile.
- ![](<./Pics/Screenshot From 2026-04-23 11-44-05.png>)
- ![](<Pics/Screenshot From 2026-04-23 11-44-59.png>)
- ![](<./Pics/Screenshot From 2026-04-23 11-45-48.png>)
### Subdomain Enumeration
- After subdomain enumeration i found the subdomain `cacti.monitorsfour.htb`.
- ![](<./Pics/Screenshot From 2026-04-23 12-03-30.png>)
- ![](<./Pics/Screenshot From 2026-04-23 12-05-52.png>)
- Subdomain is running on this version `cacti v1.2.28`.
- It also has no signup page, so i need a valid account to access this service.
*NOTE*: `cacti` is network management service running on SNMP (Simple Network Management Protocol), you can use this service to manage everything on your network.
- All CVEs in this version `cacti v1.2.28` need valid account, which is the issue we need to handle.

## Stage2: ATO (Account Take Over) to gain access on `cacti` service:
- From my small experience in web development, when i'm creating login system, I identify the user by `ID` (Identifier), I take this ID to render the profile data  in user's profile page.
-  If `monitorsfour.htb/user?token=` doesn't have security mechanism to prevent IDOR (Insecure Direct Object Reference), i can take over another account.
- I tried `/user?token=0` because 0 is usually admin's ID, And i got JSON object contains a lot of emails with their passwords.
- ![[./Pics/Screenshot From 2026-04-23 12-13-56.png]]
- I put all these encrypted passwords in file to crack and got only one password.
- ![[./Pics/Screenshot From 2026-04-24 13-49-32.png]]
- These credentials worked on `monitorsfour.htb`, but it didn't work on `cacti.monitorsfour.htb`.
- I stucked here for sometime thinking in something else i didn't do.
	- Is there information i didn't notice?
	- Is there enumeration technique i didn't perform?
- I logged in to `monitorsfour.htb` with cracked credentials, when i was browsing the site, I found users page `/users`, I looked at this page for some minutes and got idea:
	- What if i used the same password with the real name of the user to login `cacti.monitorsfour.htb`?
- It worked, i logged in `cacti.monitorsfour.htb` with user `Marcus`.
- ![](<./Pics/Screenshot From 2026-04-24 14-30-27.png>)
- ![](<./Pics/Screenshot From 2026-04-24 14-31-17.png>)
- ![](<./Pics/Screenshot From 2026-04-24 14-31-47.png>)
- all CVEs i've searched about need valid account and now i have, So let's exploit the service.
- I'll use this `CVE-2025-24367`.

## Stage4: Getting shell on the server
*NOTE*: `CVE-2025-24367` is command injection in graphs feature, the security mechanism in this part doesn't protect the software from newlines `\n` which is lead to RCE via command injection vulnerability.
- [Technical report](https://github.com/Cacti/cacti/security/advisories/GHSA-fxrq-fr7h-9rqq)

### Steps of exploit:
1. Preparing the payload and encode it, i will inject my php shell instead of `phpinfo();`.
2. Using graph creation/template functionality to inject my payload in vulnerable paramter `--right-axis-label`.
3. Start my listener, Trigger the exploit by accessing the file `http://cacti.monitorsfour.htb/cacti/<FILE_NAME>`.
4. [Automated POC](https://github.com/SoftAndoWetto/CVE-2025-24367-PoC-Cacti/blob/main/exploit.py)
5. [Manual POC](https://medium.com/@929319519qq/cve-2025-24367-exploit-no-code-59aff124d547).
6. ![[./Pics/Screenshot From 2026-04-26 08-58-54.png]]
7. Get user flag `user.txt`.

## Getting root flag
- I spend sometime thinking here after a lot of trials of privilege escalation to root, I got shell on linux web server and this machine is windows, Am i in docker container or what?
- I run this command to check `ls -la /.dockerenv`, And i found this file existed on the server, i'm in container.
- So i targeted what am i going to do, it's `Docker Escaping`.
- two ports of docker APIs are filtered, i can't do anything externally  (recon, exploitation, ....).
### Docker container escaping
- I'm in docker container, The IP address i have is container's, I need to know the docker engine's IP to start my recon about docker.
- I tried this command to give gateway connection `curl -v http://host.docker.internal:2375/info`, It's DNS trick to know gateway connections of docker engine because the i don't know engine's IP and the ports are filtered which is i can't scan them externally.
- I found this IP address but the connection is refused.
- ![[./Pics/Screenshot From 2026-04-29 03-50-15.png]]
- I spend sometime thinking util i got simple idea, If this IP is refused, maybe another one in the same range i can connect, so i used this simple bash script to scan IP's range.

```bash
  for i in $(seq 1 254); do (curl -s --connect-timeout 1 http://192.168.65.$i:2375/version 2>/dev/null | grep -q "ApiVersion" && echo "192.168.65.$i:2375 OPEN") & done; wait 192.168.65.7:2375 OPEN
```

- ![](<./Pics/Screenshot From 2026-04-29 03-55-35.png>)
- Docker engine's version is `28.3.2`
- ![](<./Pics/Screenshot From 2026-04-29 03-57-12.png>)
- After some research i found this container escaping CVE `CVE-2025-9074`, I used this script to exploit. [Docker escaping POC](https://github.com/zaydbf/CVE-2025-9074-Poc)
- ![](<./Pics/Screenshot From 2026-04-29 04-26-36.png>)