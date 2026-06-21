### Step 1: Understand our target
- I found `ssh` and Next.js web application from my Nmap scanning.
- ![Scanning](<./Pics/Screenshot From 2026-05-31 04-04-46 1.png>)
- I accessed the website, After the first look at the GUI, It's a reactor state monitor.
- ![Website](<./Pics/Screenshot From 2026-05-31 04-27-12.png>)
- by Wappalyzer browser extension, I found that this website uses vulnerable version of Next.js (React2Shell vulnerability).
### Step 2: First foothold by React2Shell exploit
- I used script has been wrote in python to automate the React2Shell exploit and i've got shell on web server.
- ![React2Shell Exploit](<./Pics/Screenshot From 2026-05-31 05-02-25.png>)
- I found database file `reactor.db` on web server, i've downloaded on my local machine to browse it and i found hashed credentials inside.
- ![Database Credentials](<./Pics/Screenshot From 2026-05-31 12-37-53.png>)
### Step 3: Password cracking and gaining User Flag
- I tried to crack these credentials by john and cracking of user `engineer`'s password succeeded.
- ![Pass Cracking](<./Pics/Screenshot From 2026-05-31 12-47-37.png>)
- I logged with these cracked credentials and i've got User Flag.
- ![User Flag](<./Pics/Screenshot From 2026-05-31 12-50-39.png>)

### NodeJS command with root privilege lead to privilege escalation
- During enumeration of running process with root privilege on this machine, I've found node.js command
- ![NodeJS Command](<./Pics/Screenshot From 2026-06-05 15-11-52.png>)
- I've searched about the `--inspect` flag on this command, and found lots of features it provides, the most important one is that i can access the NodeJS runtime environment using chrome developer tools.
- I forwarded the traffic to my local machine using `ssh local port forwarding` and `ssh -L <ATTACKER_PORT>:localhost:<TARGET_PORT> engineer@<MACHINE_IP>`.
- After forwarding the traffic to my local machine, Now i can access the running NodeJS runtime environment on the target machine from my attacker machine and execute commands with root privileges and gain Root Flag.
- ![Root Flag](<./Pics/Screenshot From 2026-06-05 15-57-48.png>)
- ![Achievement](<./Pics/Screenshot From 2026-06-05 16-01-17.png>)