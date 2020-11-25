from flask import Flask, render_template, redirect, url_for, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, inputs
import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
api = Api(app)

class Data_weather(db.Model):
    __tablename__ = "data_weather"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    ymd = db.Column(db.String(50), nullable=False)
    tianqi = db.Column(db.String(50), nullable=False)
    bWendu = db.Column(db.String(50), nullable=False)
    yWendu = db.Column(db.String(50), nullable=False)
    fenli = db.Column(db.String(50), nullable=False)
    fenxiang = db.Column(db.String(50), nullable=False)
    yer = db.Column(db.String(50), nullable=False)
    month = db.Column(db.String(50), nullable=False)

@app.route("/")
def index():
    city = Data_weather.query.all()
    # print("----",city)
    li = []
    for i in city:
        li.append(i.city)
    li = set(li)
    # dd = []
    # for j in li:
    #     dd.append({"city":j})
    # print(dd)
    return render_template("index.html",li = li)

class LoginView(Resource):
    city = '西安'
    yer = '2017'
    mon = '01'
    # 接受传过来的ajax数据
    def post(self):
        # 获取这些数据
        parser = reqparse.RequestParser()

        # 发过来的数据必须是city yer和mon的键
        parser.add_argument("city", required=True)
        parser.add_argument("yer",required = True)
        parser.add_argument("mon",required = True)

        # 整理数据
        args = parser.parse_args()
        # 获取真正的username和password
        city = args.get("city")
        yer = args.get("yer")
        mon = args.get("mon")
        # print(city,yer,mon)
        # if u =="wakaka" and p=="123456":
        # weather=db.session.query(Data_weather).filter(Data_weather.city==city,Data_weather.yer==yer,Data_weather.month==mon).all()
        weather=Data_weather.query.filter(Data_weather.city==city).filter(Data_weather.yer==yer).filter(Data_weather.month==mon).all()
        # print(weather)
        li=[]
        for i in range(len(weather)):
            print(weather[i])
            li.append(
                {'id':weather[i].id,'city':weather[i].city,'ymd':weather[i].ymd,
                 'tianqi':weather[i].tianqi,'bWendu':weather[i].bWendu,'yWendu':weather[i].yWendu,
                 'fenli':weather[i].fenli,'fenxiang':weather[i].fenxiang,'yer':weather[i].yer,
                 'mon':weather[i].month}
            )
        # print(li)
            # return {"login_data_succes":""}
        return {"li":li}
api.add_resource(LoginView,"/tijiao/")

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    app.run(debug=True,port=8848)