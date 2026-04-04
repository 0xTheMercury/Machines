### Machine Name: Facts
### Difficulty: Easy
### OS: Linux

### Scanning And Identify The Target:
- The result of NMAP scanning show me ssh and http server `http://facts.htb/`.
- When i was trying to identify what that domain is, I discovered that it's like blog post or something like that.
- ![alt text](pics/Screenshot%20From%202026-03-05%2017-32-34.png)

### Website Enumeration And Creating Admin Account:
- I runned gobuster to enumerate the hidden directories on the server and found an admin path and i could creat account with limited permissions.
- ![alt text](pics/Screenshot%20From%202026-03-05%2017-48-33.png)
- ![alt text](pics/Screenshot%20From%202026-03-05%2017-58-30.png)
- ![alt text](pics/Screenshot%20From%202026-03-05%2018-00-35.png)
- ![alt text](pics/Screenshot%20From%202026-03-06%2015-55-14.png)
- I noticed that this website is running on service called `Camaleon CMS` and it's version is `2.9.0` and this version is vulnerable to `Mass Assignment vulnerability`.

- *NOTE*: This vulnerability makes me inject my special paramter in vulnerable backend object to get higher privileges "You should read more about this vulnerability".

- The vulnerability is in change password feature, I will inject paramter "role" and set a value "admin" to it and send the request to get administrator privileges.

- *NOTE*: This application's backend is running `Ruby on Rails` framework, This backend analyze the parameters like object.
- ![alt text](pics/Screenshot%20From%202026-03-06%2016-44-38.png)

- *Exploit*: I went profile page and change password button and send the request, intercept the request with 'Burpsuit' and inject my paramter, forward the request to the backend, gain administrator privileges.
- ![alt text](pics/Screenshot%20From%202026-03-06%2016-47-05.png)

### Discover S3 bucket Security Credintials --> Protected SSH key:
- I found S3 bucket security credintials in settings page, I logged in to S3 bucket endpoint, Found file called `internal`, and there SSH private key inside this file.
- ![alt text](pics/Screenshot%20From%202026-03-06%2017-11-45.png)
- ![alt text](pics/Screenshot%20From%202026-03-09%2019-05-52.png)
- ![alt text](pics/Screenshot%20From%202026-03-09%2019-49-38.png)
- ![alt text](pics/Screenshot%20From%202026-03-09%2019-48-39.png)
- Now i have private key but i still need a username.
- After little bit research and help from AI, if this private key is protected with passphrase (it's like password) and i found it, i can decrypt the private key and get a username.

- *NOTE*: this algorithm `ssh-ed25519`, This algorithm leaves username@host like comment sometimes.

- I converted this private key file to '.hash' format with `ssh2john` and decrypt the hash file with `JohnTheRipper` to get SSH private key's passphrase.
- ![alt text](pics/Screenshot%20From%202026-03-09%2019-58-02.png)
- ![alt text](pics/Screenshot%20From%202026-03-11%2016-56-20.png)
- I logged in with ssh and got User.txt "User Flag".
- ![alt text](pics/Screenshot%20From%202026-03-11%2017-14-32.png)
- ![alt text](pics/Screenshot%20From%202026-03-11%2017-27-21.png)

### Privilege Escalation To Get Root Access:
- I runned `cat /etc/passwd` to identify the users on the machine.
- ![alt text](pics/Screenshot%20From%202026-03-11%2017-23-36.png)
- I runned `sudo -l` to know if there's tool can run with root/sudo privileges, and i found tool called `facter`.
- ![alt text](pics/Screenshot%20From%202026-03-11%2017-22-48.png)

- *NOTE*: This is linux built-in tool gives you very detailed information about your machines, and you can also customize it using Ruby scripts.

- I created very simple Ruby script to execute "/bin/bash", once i give the directory the contains my script to this tool and run the command, it'll give me root shell, and then i can get Root.txt (Root Flag).
- ![alt text](pics/Screenshot%20From%202026-03-12%2015-57-54.png)
- ![alt text](pics/Screenshot%20From%202026-03-12%2015-56-12.png)