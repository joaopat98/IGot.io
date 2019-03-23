import http.client
import json


def main():
	generate()
	
def check_status_code(code):
	if code == "000":
		return True
	else:
		return False

def generate():
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")
	payload = "{\"amount\":{\"value\":23.05,\"description\":\"Microtransaction igot.io\"}}"
	
	headers = {
    'x-ibm-client-id': "784d3d84-dd3c-4fb4-8157-dbf4e947fe3b",
    'content-type': "application/json",
    'accept': "application/json"
    }

	conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/qrcode-pixelscamp/v1/generate", payload, headers)

	res = conn.getresponse()
	data = res.read()

	data = data.decode("utf-8")
	data = json.loads(data)


	print(data)

	if data["statusCode"]=="APPR":
		inquiryQR(data["qrCodeToken"])
	else:
		print("Erro interno")

def inquiryQR(qrCodeToken):
	print("Entrou QRinquiry")
	print(qrCodeToken)
	flag=False
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")
	payload = "{\"qrCodeToken\":\""+qrCodeToken+"\"}"

	headers = {
    'x-ibm-client-id': "784d3d84-dd3c-4fb4-8157-dbf4e947fe3b",
    'content-type': "application/json",
    'accept': "application/json"
    }

	conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/qrcode-pixelscamp/v1/inquiry", payload, headers)

	res = conn.getresponse()
	data = res.read()

	data = data.decode("utf-8")
	data = json.loads(data)

	print(data)

	if check_status_code(data["statusCode"]):
		while(flag==False):
			conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/mbwayid-pixelscamp/v1/inquiry", payload, headers)

			res = conn.getresponse()
			data = res.read()

			data = data.decode("utf-8")
			data = json.loads(data)

			print("DATA 2"+data)

			transactionStatusCode = data["transactions"][0]["transactionStatusCode"]
			if transactionStatusCode == "4":
				flag = True
				print("Successful Transaction")
			elif transactionStatusCode == "5":
				flag = True
				print("Canceled: Financial operation canceled by user ")
			elif transactionStatusCode == "9":
				flag = True
				print("Registered: Financial operation registered to initiate authorization process")
				#Expired: Financial operation expired 
			elif transactionStatusCode == "-1":
				flag = True
				print("Registered: Financial operation registered to initiate authorization process")
				#Error: Financial operation ID not found

		if check_status_code(data["statusCode"]):
			purchaseQR(data["qrCodePaymentToken"])
		else:
			print("Erro interno")
	else:
		print("Erro interno")


def inquiry(transactionToken):
	flag = False
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")
	payload = "{\"transactionTokens\":[\""+transactionToken+"\"]}"

	headers = {
		'x-ibm-client-id': "784d3d84-dd3c-4fb4-8157-dbf4e947fe3b",
		'content-type': "application/json",
		'accept': "application/json"
	}

	conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/mbwayid-pixelscamp/v1/inquiry", payload, headers)

	res = conn.getresponse()
	data = res.read()

	data = data.decode("utf-8")
	data = json.loads(data)

	transactionStatusCode = data["transactions"][0]["transactionStatusCode"]

	if check_status_code(data["statusCode"]):
		while(flag==False):
			conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/mbwayid-pixelscamp/v1/inquiry", payload, headers)

			res = conn.getresponse()
			data = res.read()

			data = data.decode("utf-8")
			data = json.loads(data)

			transactionStatusCode = data["transactions"][0]["transactionStatusCode"]
			if transactionStatusCode == "4":
				flag = True
				print("Successful Transaction")
			elif transactionStatusCode == "5":
				flag = True
				print("Canceled: Financial operation canceled by user ")
			elif transactionStatusCode == "9":
				flag = True
				print("Registered: Financial operation registered to initiate authorization process")
				#Expired: Financial operation expired 
			elif transactionStatusCode == "-1":
				flag = True
				print("Registered: Financial operation registered to initiate authorization process")
				#Error: Financial operation ID not found

def purchaseQR(qrCodePaymentToken):
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")

	payload = "{\"qrCodePaymentToken\":\""+qrCodePaymentToken+"\"}"

	headers = {
    'x-ibm-client-id': "784d3d84-dd3c-4fb4-8157-dbf4e947fe3b",
    'content-type': "application/json",
    'accept': "application/json"
    }

	conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/qrcode-pixelscamp/v1/purchase", payload, headers)

	res = conn.getresponse()
	data = res.read()

	data = data.decode("utf-8")
	data = json.loads(data)

	if data["statusCode"]=="APPR":
		print("Transição efetuada")
	else:
		print("Erro interno")



def purchase(identifier,number,value):
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")
	payload = "{\"customer\":{\"customerIdentifier\":\""+identifier+"#"+number+"\"},\"amount\":{\"value\":"+value+",\"description\":\"Microtransaction igot.io\"}}"
	
	headers = {
		'x-ibm-client-id': "784d3d84-dd3c-4fb4-8157-dbf4e947fe3b",
		'content-type': "application/json",
		'accept': "application/json"
	}

	conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/mbwayid-pixelscamp/v1/purchase", payload, headers)

	res = conn.getresponse()
	data = res.read()

	data = data.decode("utf-8")
	data = json.loads(data)

	if check_status_code(data["statusCode"]):
		inquiry(data["transactionToken"])
	else:
		print("Erro interno")


def checkMBWay(identifier,number):
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")
	
	payload = "{\"customers\":[{\"identifier\":\""+identifier+"#"+number+"\"}]}"

	headers = {
		'x-ibm-client-id': "784d3d84-dd3c-4fb4-8157-dbf4e947fe3b",
		'content-type': "application/json",
		'accept': "application/json"
	}

	conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/mbwayidinformation-pixelscamp/v1/checkService", payload, headers)

	res = conn.getresponse()
	data = res.read()

	data = data.decode("utf-8")

	data = json.loads(data)

	if check_status_code(data["return"]["statusCode"]):
		if not data["return"]["customers"]:
			print("Nao tem MBWAY")
		else:
			purchase("351","910021662","20")
	else:
		print("Erro interno")

main()