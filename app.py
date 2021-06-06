
from flask import render_template
from flask import Flask, request, make_response ,redirect
from flask import url_for
import vector

app = Flask(__name__)
key = ""
result = []
sum = 0.0 #分数列表
score = []
@app.route('/')
def hello():
    return render_template('Search.html')

@app.route('/keywords',methods=["GET","POST"])
def keywords():
    global key,result,sum
    temp=key
    key=request.form.get('keywords')
    if key == None:
        key = temp
        return render_template("result.html",keywords=key,result=result,sum=sum )
#TODO---try to get result by the keywords
    result = vector.vector(key)
    return render_template("result.html",keywords=key,result=result,sum=sum )

#This function works on page 404.
@app.errorhandler(404)
def page_not_found(e):
    user = "Asshole"
    return render_template("404.html",user=user), 404

@app.route('/judge',methods=["GET","POST"])
def judge():
    global score
    global sum
    sum = 0.0
    temp = request.form.get('score')
    if temp != None:
        sc = int(temp)
        score.append(sc)
    for i in score:
        sum += i
    sum=round(sum/len(score),2)
    print("->>>>>>>>>",sum,"%")

    #TODO 处理提交的评价
    return redirect(url_for('keywords'))