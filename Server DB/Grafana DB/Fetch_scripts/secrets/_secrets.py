import json
import os

def tell_the_secrets():
	thesecfile = os.path.abspath(os.path.join(f"./", "../../../../graf_secrets.json"))
	print(thesecfile)
	with open(thesecfile) as f:
		return json.load(f)

"""
	return {
"pathToGrafanaDB": ""
}
"""