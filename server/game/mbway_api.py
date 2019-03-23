import http.client
import json
import time

#numero: /purchase -> recebe transactionToken -> /inquiry com transactionToken
#QR: /generate -> recebe qrCodeImage em base64 e qrCodeToken -> /inquiry com qrCodeToken -> Recebe qrCodePaymentToken -> /purchase com qrCodePaymentToken -> recebe statusCode = APPR
	

def fg():
	print("asdadasd")

def check_status_code(code):
	print(code)
	if code == "000":
		return True
	else:
		return False

def generate(value):
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")
	payload = "{\"amount\":{\"value\":" + value + ",\"description\":\"Microtransaction igot.io\"}}"
	
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

	if data["statusCode"]=="APPR":
		return data
	
	else:
		print("Erro interno")

def inquiryQR(qrCodeToken):
	flag=False
	conn = http.client.HTTPSConnection("site1.sibsapimarket.com:8444")

	payload = "{\"qrCodeToken\":\""+qrCodeToken+"\"}"


	headers = {
    'x-ibm-client-id': "784d3d84-dd3c-4fb4-8157-dbf4e947fe3b",
    'content-type': "application/json",
    'accept': "application/json"
    }


	while(flag==False):
		conn.request("POST", "/pixelscamp/apimarket/mbwaypurchases/qrcode-pixelscamp/v1/inquiry", payload, headers)
		res = conn.getresponse()
		data = res.read()
		data = data.decode("utf-8")
		data = json.loads(data)
		if data["statusCode"]=="000":
			return purchaseQR(data["qrCodePaymentToken"])



def inquiry(transactionToken):
	print("entrou inquiry")
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
				return 200
			elif transactionStatusCode == "5":
				return 401
			elif transactionStatusCode == "9":
				return 408
			elif transactionStatusCode == "-1":
				return 500

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

	print(data)

	if data["statusCode"]=="APPR":
		return 200
	else:
		return 500



def purchase(identifier,number,value):
	print("entrou purchase com identifier="+identifier+" number="+number+" e value="+value)
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
		return inquiry(data["transactionToken"])
	else:
		return 500


def checkMBWay(identifier,number,value):
	print("entrou checkMBWay com identifier="+identifier+" number="+number+" e value="+value)
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
			return 400
		else:
			return purchase(identifier,number,value)
	else:
		return 500

def QR_code_option():
	generate(value)

def phone_number_option(data):
	return checkMBWay(data["identifier"], data["number"], data["value"])

