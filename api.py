from flask import jsonify, Flask
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config["DEBUG"] = True

# test data
tpe = {
    "id": 0,
    "city_name": "Taipei",
    "country_name": "Taiwan",
    "is_capital": True,
    "location": {
        "longitude": 121.569649,
        "latitude": 25.036786
    }
}
nyc = {
    "id": 1,
    "city_name": "New York",
    "country_name": "United States",
    "is_capital": False,
    "location": {
        "longitude": -74.004364,
        "latitude": 40.710405
    }
}
ldn = {
    "id": 2,
    "city_name": "London",
    "country_name": "United Kingdom",
    "is_capital": True,
    "location": {
        "longitude": -0.114089,
        "latitude": 51.507497
    }
}
cities = [tpe, nyc, ldn]

def idenitfy_img(img):
	# Thresh_binary
	def convert_img(img,threshold):
		img = img.convert("L")
		pixels = img.load()
		for x in range(img.width): 
			for y in range(img.height): 
				if pixels[x, y] > threshold: 
					pixels[x, y] = 255
				else:
					pixels[x, y] = 0
		return img

	# Convert image to gray, direct tesseract and get value to fourth digits
	captcha = Image.open(img)
	Gray_captcha = captcha.convert('L')
	result = pytesseract.image_to_string(Gray_captcha, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')[:4]
	if len(result) > 3:
		pass
	# If not get 4 digits, then change threshold to get cleand img until idenitfy 4 digits
	else :
		threshold = 165
		thresh = convert_img(captcha, threshold)
		result = pytesseract.image_to_string(thresh, config='--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789')          
		for i in range(75):
			if len(result) < 4:
				threshold = threshold-1
				thresh = convert_img(captcha, threshold)
				result = pytesseract.image_to_string(thresh, config='--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789')[:4]
	return result




@app.route('/', methods=['GET'])
def home():
	return "<h1>Hello Flask</h1>"


@app.route('/data/', methods=['GET'])
def data():
	return jsonify(cities)


@app.route('/captcha/', methods=['POST'])
def captcha():
	return idenitfy_img('./captcha/0.png')


app.run()