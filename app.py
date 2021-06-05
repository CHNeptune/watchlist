
from flask import render_template
from flask import Flask, request, make_response
from flask import url_for
import test

app = Flask(__name__)
key = ""
result = []
score = []#分数列表

@app.route('/')
def hello():
    return render_template('Search.html')

@app.route('/keywords',methods=["GET","POST"])
def keywords():
    global key,result
    key=request.form.get('keywords')
#TODO---try to get result by the keywords
    result = test.Search(key)
    return render_template("result.html",keywords=key,result=result )

#This function works on page 404.
@app.errorhandler(404)
def page_not_found(e):
    user = "Asshole"
    return render_template("404.html",user=user), 404

@app.route('/judge',methods=["GET","POST"])
def judge():
    global score
    sc = request.form.get('score')
    print("------------------>  ",sc)

    #TODO 处理提交的评价
    return render_template("result.html",keywords=key,result=result )