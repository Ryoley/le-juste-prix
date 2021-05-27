from flask import Flask, url_for, render_template, request, flash, redirect
import pdb
import requests
import random

app = Flask(__name__)

apps = []
history = []
messageshistory = []

@app.route('/', methods=['GET', 'POST'])
def getapps():

    getlist = requests.get(
        'https://api.steampowered.com/ISteamApps/GetAppList/v2/')

    jsonlist = getlist.json()

    finallist = jsonlist['applist']['apps'][:20]

    for elem in finallist:
        urlgameinfos = 'http://store.steampowered.com/api/appdetails?appids=' + \
            str(elem['appid'])
        gameinfos = requests.get(urlgameinfos)
        jsongameinfos = gameinfos.json()
        if jsongameinfos[str(elem['appid'])]['success']:
            price = round(jsongameinfos[str(elem['appid'])]['data']['price_overview']['final'] /
                          100) if jsongameinfos[str(elem['appid'])]['data'].get('price_overview') else 0
            if price != 0:
                apps.append({'name': elem['name'], 'price': price})
    # Test history
    # apps = [{'name': 'Vacation Adventures: Park Ranger 10', 'price': 4}, {'name': 'Sweet F. Cake: Full Soundtrack', 'price': 4}, {'name': 'Lorera', 'price': 8}, {'name': 'Masters of Puzzle - Trip', 'price': 5}, {'name': 'Video Editor Tycoon', 'price': 1}, {'name': 'Elliot', 'price': 8}, {'name': 'Uranus', 'price': 2}, {'name': 'CORONAVIRUS BATTLEGROUNDS: Coronavirus News', 'price': 4}]
    
    if request.method == 'POST':
        random_nb = int(request.form.get('random_nb'))
        result = request.form['number']
        response= ''
        getgamename = apps[random_nb]['name']
        getgameprice = apps[random_nb]['price']
        try:
            if isinstance(float(result), float):
                if apps[random_nb]['price'] == int(result):
                    response = 'Vous avez gagné !'
                if apps[random_nb]['price'] > int(result):
                    history.append(result)
                    response = "C'est plus !"
                    messageshistory.append(response)
                if apps[random_nb]['price'] < int(result):
                    history.append(result)
                    response = "C'est moins !"
                    messageshistory.append(response)
        except ValueError:
            response = "Erreur, cette valeur n'est pas acceptée !"
            history.append(result)
            messageshistory.append(response)
        return render_template('index.html', random_nb=random_nb, response=response, getgamename=getgamename, getgameprice=getgameprice, history=history, messageshistory=messageshistory)
    else:
        random_nb = random.randint(0, len(apps))
        getgamename = apps[random_nb]['name']
        getgameprice = apps[random_nb]['price']
        history.clear()
        messageshistory.clear()
        return render_template('index.html', random_nb=random_nb, getgamename=getgamename, getgameprice=getgameprice)
    


if __name__ == '__main__':
    app.run(host="0.0.0.0")
