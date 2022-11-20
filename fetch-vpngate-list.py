import pandas as pd
from urllib.request import urlopen
import base64

url = "http://www.vpngate.net/api/iphone/"
country="KR"
num_server_top = 15

with urlopen(url) as file:
	content = file.readlines()
	
	df = pd.DataFrame(columns = content[1].decode()[:-4].split(","))
	
	for server in content[2:-1]:
		df.loc[len(df)] = server.decode()[:-4].split(",")

# 	print(df.columns)

	df2 = df.loc[df.CountryShort == country]
	df2.Speed = df2.Speed.astype(float)
	df2.Speed = round(df2.Speed / 10**6,2)
	df2 = df2.sort_values(by="Speed",ascending=False)
	print(df2[["Speed","Ping","NumVpnSessions","TotalUsers"]].head(num_server_top).to_string(index=False))
	
	# download the fastest config
	ip = df2["IP"].iloc[0]
	b64_string = df2["OpenVPN_ConfigData_Base"].iloc[0]
	b64_string  += "=" * ((4 - len(b64_string) % 4) % 4)
	config = base64.b64decode(b64_string)
	f = open("vpngate-config-kr-"+ip+'.ovpn','wb')
	f.write(config)
	f.close()
