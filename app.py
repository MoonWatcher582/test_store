from flask import Flask, render_template, request			#import flask
from twilio.rest import TwilioRestClient				#import Twilio SMS service
import random								#import use of random fct

account_sid = "AC6a2ed3970fc467269387ac7d044a498b"
auth_token = "cccc0ca6c80adb61d27ab2ec1ec0e9aa"
client = TwilioRestClient(account_sid, auth_token)			#ready twilio by authenticating account


app = Flask(__name__)							#declare flask
	
stock = [								#set up the items in stock in a list
	('toss', 'Tosservania'),
	('capital', 'Culture of Capital'),
	('finder', 'Finder Guy'),
	('collect', 'The Collector'),
	('ttog', 'The Trials and Tears of Gannon'),
	('ttg2', 'The Trials and Tears of Gannon II')
]

@app.route('/')								#route the default part of the website to what follows
def home():
	return render_template('index.html', stock=stock)		#render index.html, the html stock variable is the stock list

@app.route('/order')							#default webpage/order
def order():
	dict_stock = dict(stock)					#turn menu into a dictionary
	
	if request.args['games'] == "" or request.args['address'] == "" or request.args['phone'] == "":
                if request.args['games'] == "":
			nullitem="you've selected a game"
		elif request.args['address'] == "":
			nullitem="you've included your shipping address"
		elif request.args['phone'] == "":
			nullitem="you've included your phone number"
		return render_template('no_order.html', nullitem=nullitem, phone="")			#error page, go back and try again

	digits = string_cat(request.args['phone'])
	if digits.__len__() != 12:
		nullitem="you've included a proper phone number"
		return render_template('no_order.html', nullitem=nullitem, phone=digits)

	games = dict_stock[request.args['games']]			#use the 'games' arg to get the key-value pair of it from the dict
	time = random.choice(range(1, 8))				#randomize the time
	
	msg = "You just ordered  " + games + " from Raritanium Games. " 
	msg = msg + games + " will be shipped in " + str(time) +  " days to " + request.args['address'] + ". Thank you for your business!"

	message = client.messages.create(body=msg, to=digits, from_="+17328123770")
	print message.sid


	return render_template('order.html', games=games, time=time, address=request.args['address'], phone=request.args['phone'])	#render page

def string_cat(str):
	new_str = ""
	for c in str:
		if c.isdigit():
			new_str += c
	if new_str.__len__() == 11:
		return "+" + new_str
	elif new_str.__len__() == 10:
		return "+1" + new_str
	else:
		return new_str

if __name__ == '__main__':
	app.run('0.0.0.0', port=4000, debug=True)			#use port 4000
