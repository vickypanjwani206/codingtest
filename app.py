import json
import requests
from flask import Flask, render_template, request
import pymongo
client=pymongo.MongoClient('mongodb://localhost:27017/')
#https://itunes.apple.com/lookup?id=284910350
# 1538107216
# 1533629863

#Description, artistId, artistName, price, genre
db=client['mydb']


app=Flask(__name__,template_folder='templates')

@app.route('/',methods=['GET','POST'])
def Home():
    if request.method=="POST":
        id=request.form['id']
        base_url='https://itunes.apple.com/lookup?id='
        url=base_url+id
        try:
            data=requests.get(url)
            print(data)
            json_data=data.json()
            print(json_data)

            genre=json_data['results'][0]['genres']
            description=json_data['results'][0]['description']
            artistid=json_data['results'][0]['artistId']
            artistname=json_data['results'][0]['artistName']
            search_id=db.itune.find_one({'ID':id})
            if search_id is None:
                db.itune.insert_one({'ID':id,'genre':genre,'description':description,'artistid':artistid,'artistname':artistname})
                dict = {'genre':genre,'description':description,'artistid':artistid,'artistname':artistname}
                return render_template('home.html',data=dict)
            else:

                dict = {'genre': search_id['genre'], 'description': search_id['description'], 'artistid': search_id['artistid'], 'artistname': search_id['artistname']}
                return render_template('home.html', data=dict)
        except:
            msg={'message':"Id not found"}
            return render_template('home.html', message=msg)


    return render_template('home.html')

if __name__=="__main__":
    app.run(host='127.0.0.1',port=8000)
