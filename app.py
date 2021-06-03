
from flask import render_template
from flask import Flask, request, make_response
from flask import url_for
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('Search.html')
@app.route('/<name>/test')
def name_test(name):
    print("Your name is",name)
    print(url_for('name_test',name='Me'))
    print(url_for('name_test',name='You'))
    return 'Test Page, your name is %s' % name
@app.route('/keywords',methods=["GET","POST"])
def keywords():
    key=request.form.get('keywords')
    print(key)

#TODO---try to get result by the keywords
    result = [
        {"FirstPart":"位于阿肯色州和密西西比州交界处的密西西比河","SecondPart":"2021-04-04"},
        {"FirstPart":"文斯利代尔，英格兰约克郡谷地国家公园","SecondPart":"2021-04-13"},
        {"FirstPart":"宇航员杰夫·威廉姆斯在国际空间站拍摄到的地球","SecondPart":"2021-04-25"},
        {"FirstPart":"米斯巴赫的郁金香田，德国巴伐利亚州","SecondPart":"2021-05-08"},
        {"FirstPart":"飘落的杜鹃花瓣铺在Grassy Ridge Bald山的小径上，北卡罗莱纳州皮斯加国家森林","SecondPart":"2021-05-09"}
    ]

    return render_template("result.html",keywords=key,result=result )

@app.errorhandler(404)
def page_not_found(e):
    user = "Asshole"
    return render_template("404.html",user=user), 404

