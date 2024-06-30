from flask import Flask,render_template, request, url_for, redirect ,session ,flash,send_file
import pymysql
import time
import re
import hashlib
import html
import pandas as pd
import random, os, string
from function import *
from waitress import serve
from generateApiKey import generateApiKey
from vars.sql import *
from datetime import datetime
from datetime import date
from flask_mysqldb import MySQL
from jinja2 import Template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_csp import csp
from flask_sslify import SSLify

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='arron'
app.config['MYSQL_PASSWORD'] ='arron2030'
app.config['MYSQL_DB'] ='pwc'
# mysql = MySQL()
# mysql.init_app(app)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'your_csrf_secret_key'


mysql = pymysql.connect(
    host = app.config['MYSQL_HOST'],
    user = app.config['MYSQL_USER'],
    password= app.config['MYSQL_PASSWORD'],
    db = app.config['MYSQL_DB']
)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
login_manager.login_message = "請先登入"

dd =""
r=""
class User(UserMixin):
    pass

def database_connect(sql,value):
    cursor = mysql.cursor()
    cursor.execute(sql,value)
    return cursor
def con(sql):
    cursor  = mysql.cursor()
    cursor.execute(sql)
    return cursor
def fetchall(cursor):
    return cursor.fetchall()
def fetchone(cursor):
    return cursor.fetchone()

@login_manager.user_loader
def user_loader(userid):  
    user = User()
    user.id = userid
    cursor = database_connect(sql_search_all_user_by_id,(userid,))
    result_user = fetchone(cursor)
    user.name = result_user[1]
    user.token = result_user[3]
    user.hash_id = result_user[4] 
    return user

@app.route('/')
def index():
    return render_template('index.html')

# 登入
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST' and 'account' in request.form and 'password' in request.form:
        account = request.form['account']
        input_password = request.form['password']
    
        result = fetchone(database_connect(sql_select_all_user_by_name,(account,)))
        check_token =result[3]
        
        user = User()
        user.id = result[0]
        # api_key = out_words()
       
        # token = hash_text(str(api_key))
        hash_id = hash_text(str(user.id))
        # hash_password =  hash_text(result[2],salt)
        password_hash=result[2]
        if len(result)>0:
            if verify_text(password_hash,input_password)==True:
                login_user(user)
                # if check_token=="":     
                #     database_connect(sql_update_token,(password_hash,token,hash_id,result[0]))
                #     mysql.connection.commit()
                return redirect(url_for('search'))
            else:
                flash('帳號或密碼錯誤')
                return redirect(url_for('login'))
    return render_template('index.html')    
# 有問題
def get_api_key(input):
    seed='16'
    api_key = generateApiKey(input,seed)
    return api_key

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# 產生hash
def gernerate_hash(input_string):
    hash_result = generate_password_hash(input_string, method="pbkdf2:sha256", salt_length=8)
    return hash_result
# 確認hash

    
# password hash
def hash_text(password):
    salt = 'pwcprj'
    password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return password_hash
def verify_text(stored_password, input_password):
    salt = 'pwcprj'
    password_hash = hashlib.sha256((input_password + salt).encode('utf-8')).hexdigest()
    return password_hash == stored_password    

@app.route('/search', methods = ['POST','GET'])
@login_required 
def search(): 
    global r 
    idz = current_user.id
    name = current_user.name
    date_format = '%Y-%m-%d'
    date_check_pattern = r'^\d{4}-\d{2}-\d{2}$'
    table_df = pd.read_csv('table.csv')
    table_df[['n','code', 'name']] = table_df['table_name'].apply(lambda x: pd.Series(x.split('_')))
    table_df.drop(['table_name','n','Unnamed: 0'], axis=1, inplace=True)
    table_df['code'] = table_df['code'].str.lower()
    my_dict = dict(zip(table_df['name'], table_df['code']))
   
    if request.method == 'POST':
        target_company = html.escape(request.values.get('company').strip().replace(" ",""))
        start_time =request.values.get('start_date')
        end_time = request.values.get('end_date')
        file_type = request.values.get('file_type')
        
        if re.fullmatch(date_check_pattern,start_time) and re.fullmatch(date_check_pattern,end_time):
            start_date_obj = datetime.strptime(start_time, date_format) 
            end_date_obj = datetime.strptime(end_time, date_format) 
            if(start_time !="" and end_time!="" and end_date_obj>start_date_obj):
                # 如果輸入公司名稱
            
                if target_company in my_dict:
                    code_value = my_dict[target_company]
                    # table =code_value
                    code = code_value
                    sql_search_stock_id =f'SELECT Code FROM `{code}` WHERE Code = "{code}"' 
                    print(target_company)
                    search_result = fetchall(con(sql_search_stock_id))
                else:
                    # table = target_company.lower()
                    code  = target_company.lower()
                    sql_search_stock_id =f'SELECT Code FROM `{code}` WHERE Code = "{code}"' 
                    try:
                    # print(sql_search_stock_id)
                        search_result = fetchall(con(sql_search_stock_id))
                    except Exception as error:
                        flash('查無此公司資料')
                        print(error)
                        return redirect(url_for('search'))
                if len(search_result) >0:
                    rs = fetchall(database_connect(sql_search_tmp,(idz,)))
                    if len(rs) < 1:
                        if target_company in my_dict:
                            code_value = my_dict[target_company]
                            
                            database_connect(sql_insert_tmp,(idz,start_time,end_time,code_value))
                        else:
                            database_connect(sql_insert_tmp,(idz,start_time,end_time,target_company))
                    else:
                        if target_company in my_dict:
                            code_value = my_dict[target_company]
                            database_connect(sql_update_tmp,(start_time,end_time,code_value,idz))
                        else:
                            database_connect(sql_update_tmp,(start_time,end_time,target_company,idz))   
                    mysql.commit()
                    if target_company in my_dict:
                        code_value = my_dict[target_company]
                        bgtime = start_time
                        endtime = end_time
                        code = code_value
                        sql_select_all = f'SELECT * FROM `{code}` WHERE DataDate BETWEEN "{bgtime}" AND "{endtime}" LIMIT 50'
                        show_table_result = fetchall(con(sql_select_all))
                    else:
                        bgtime = start_time
                        endtime = end_time
                        code = target_company.lower()
                        sql_select_all = f'SELECT * FROM `{code}` WHERE DataDate BETWEEN "{bgtime}" AND "{endtime}" LIMIT 50'
                        show_table_result = fetchall(con(sql_select_all))  
                    if len(show_table_result)>1:
                        if target_company in my_dict:
                            code_value = my_dict[target_company]
                            bg =start_time
                            end = end_time
                            code = code_value
                            sql_select_all_without_limit_dataframe = f'SELECT * FROM `{code}` WHERE DataDate BETWEEN "{bg}" AND "{end}"'

                            install_result = fetchall(con(sql_select_all_without_limit_dataframe))
                        else:
                            bg =start_time
                            end = end_time
                            sql_select_all_without_limit_dataframe = f'SELECT * FROM `{code}` WHERE DataDate BETWEEN "{bg}" AND "{end}"'

                            install_result = fetchall(con(sql_select_all_without_limit_dataframe))   
                        
                        show_data_frame = pd.DataFrame(show_table_result,columns=['DataDate','Code','Name','TradeVolume','TradeValue','OpeningPrice','HighestPrice','LowestPrice','ClosingPrice','Change','Transaction','FiveDayMovingAverage','TenDayMovingAverage','TwentyDayMovingAverage','SixtyDayMovingAverage','TradeVolumeTwentyDayMovingAverage','TradeVolumeFiveDayMovingAverage','TradeVolumeTenDayMovingAverage','TradeVolumeSixtyDayMovingAverage'])
                        download_data_frame = pd.DataFrame(install_result,columns=['DataDate','Code','Name','TradeVolume','TradeValue','OpeningPrice','HighestPrice','LowestPrice','ClosingPrice','Change','Transaction','FiveDayMovingAverage','TenDayMovingAverage','TwentyDayMovingAverage','SixtyDayMovingAverage','TradeVolumeTwentyDayMovingAverage','TradeVolumeFiveDayMovingAverage','TradeVolumeTenDayMovingAverage','TradeVolumeSixtyDayMovingAverage'])

                        global dd
                        if(file_type == "csv"):
                            result = start_time+"_to_"+end_time+".csv"
                            download_data_frame.to_csv(result,index=False)
                            dd = result
                        elif(file_type == "excel"):
                            result =start_time+"_to_"+end_time+".xlsx"
                            download_data_frame.to_excel(result)
                            dd =result
                        return render_template('main.html',tables=[show_data_frame.to_html(classes='data')],titles=show_data_frame.columns.values,file_name=dd,name=name)
                    else:
                        flash('此區間查無資料')
                        return redirect(url_for('search'))
                else:
                    flash('請輸入有效的公司')
                return redirect(url_for('search'))
            else:
                flash('請輸入正確的日期區間')
                return redirect(url_for('search'))
        else:
            flash('請輸入正確的日期格式')
            return redirect(url_for('search'))
    elif request.method=='GET':
        pass
          
    return render_template('main.html', name = name)  

@app.route('/getdata')
def get_data():

    if request.method=='GET':
        
        user_id = html.escape(request.args.get('userid'))
        token = html.escape(request.args.get('token'))
        data = fetchone(database_connect(sql_get_user,(user_id,)))
        verify_token = hash_text(token)
        if len(data) > 0 and verify_token==data[0]:
            output = fetchone(database_connect(sql_join_table,(verify_token,user_id)))
            if len(output) > 0:
                result_date = fetchone(database_connect(sql_select_date,(output[0],)))
                code = result_date[2]
                resbg = result_date[0]
                endresult = result_date[1]
                sql_select_all_data_stock =f'SELECT * FROM `{code}` WHERE DataDate BETWEEN "{resbg}" AND "{endresult}"'

                result = fetchall(con(sql_select_all_data_stock))
                data_frame = pd.DataFrame(result,columns=['DataDate','Code','Name','TradeVolume','TradeValue','OpeningPrice','HighestPrice','LowestPrice','ClosingPrice','Change','Transaction','FiveDayMovingAverage','TenDayMovingAverage','TwentyDayMovingAverage','SixtyDayMovingAverage','TradeVolumeTwentyDayMovingAverage','TradeVolumeFiveDayMovingAverage','TradeVolumeTenDayMovingAverage','TradeVolumeSixtyDayMovingAverage'])
                return render_template('getdata.html',tables=[data_frame.to_html(classes='data')],titles=data_frame.columns.values)
        else:     
            flash('網址有誤，請重新輸入')
            return render_template('getdata.html')
            
    return render_template('getdata.html')
@app.route('/download')
def download():
    return send_file(dd, as_attachment=True)
  
if __name__ == '__main__':
    app.run(debug=True)
    # serve(app,host="0.0.0.0",port=8080,threads=2)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()