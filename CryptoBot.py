import requests
import telebot
import re
import json
TOKEN='##ENTER YOUR TELEGRAM KEY##'
bot = telebot.TeleBot(TOKEN)

#Send the bot the currency symbol, it sends you its price. Fun stuff.

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

cryptoregexprice=re.compile(r'(price)(\w\w\w)')
@bot.message_handler(regexp='price\w\w\w')
def bitprice(message):
	mess=str(message)
	mo = cryptoregexprice.search(mess)

	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
	parameters = {
		'symbol': mo.group(2)
	}
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': '##ENTER YOUR CRYPTO KEY##',
	}
	session = requests.Session()

	session.headers.update(headers)
	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
		final = data['data'][mo.group(2)]['quote']['USD']['price']
		bot.reply_to(message, round(final,2))
	#print(data['data'][symb]['quote']['USD']['price'])
	except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects, KeyError) as error:
		#bot.reply_to(message,error)
		bot.reply_to(message, "An error occurred: "+str(error))

cryptoregexchange=re.compile(r'(change)(\w\w\w)')
@bot.message_handler(regexp='change\w\w\w')
def bitchange(message):
	mess = str(message)
	mo = cryptoregexchange.search(mess)

	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
	parameters = {
		'symbol': mo.group(2)
	}
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': '##ENTER YOUR CRYPTO KEY##',
	}
	session = requests.Session()

	session.headers.update(headers)
	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
		final = data['data'][mo.group(2)]['quote']['USD']['percent_change_7d']
		bot.reply_to(message, '7 Day percent change for ' + str(mo.group(2))+ ' is ' +str(round(final, 2)))
	# print(data['data'][symb]['quote']['USD']['price'])
	except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects, KeyError) as error:
		# bot.reply_to(message,error)
		bot.reply_to(message, "An error occurred: " + str(error))

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()
