import os
import sqlite3
import datetime
from googlesearch import search
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,session
app = Flask(__name__)


@app.route('/')
def show_entries():
    con = sqlite3.connect('todo.db')
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS message(data_id,msg,keyword,date_time)''')
    result = con.execute('''select * from message order by data_id desc''')
    return render_template('index.html',result = result)
    
# def show_url():
#     con = sqlite3.connect('url_result.db')
#     # d = con.cursor()
#     result_url = con.execute('''select * from search order by data_id desc''')
#     return render_template('index.html',result = result_url)



# com_list = ['三菱マテリアル','東レ']
#    # tbs ='qdr:d'


@app.route('/srch')
def googl_srch():
    import google  as goos
    goos.main()
    # return redirect('result.html')
    return redirect('/result')
# if __name__ == '__main__':
#     app.run()


# def google_search(query):
#     for url in search(query, lang='jp', num=3, stop= 5):
#         date_time = datetime.datetime.today()
#         data_id = date_time.strftime("%Y%m%d")
#         # print (url) #コマンドプロンプトの画面に記入する。
#         f = open('result.html','a',newline='\n')
#         f.write('<a href="'+ url +'">'+i +data_id +'不祥事'+'</a><br>')
#         f.close()
        

# @app.route('/srch')
# def main():
#     # com_list = ['三菱マテリアル','東レ']
#     global i
#     for i in com_list:
#                 google_search('"'+i+'　不祥事"')

# if __name__ == '__main__':
#     main()

@app.route('/result')
def read_url():
    con = sqlite3.connect('url_result.db')
    cursor = con.cursor()
    cursor.execute("select * from search where url !=',' ")
    result_srch = cursor.fetchall()
    # return render_template('index.html',result_srch = result_srch)
    return render_template('result.html',result_srch = result_srch)

@app.route('/delete_url_data',methods=['GET','POST'])
def delete_url():
    if request.method == 'POST':
        data_ids = request.form['action']
        con = sqlite3.connect('url_result.db')
        c = con.cursor()
        query = "DELETE FROM search WHERE url=? "
        c.execute(query,(data_ids,))
        con.commit()
        result_srch = con.execute('''select * from search order by data_id desc''')
        return render_template('result.html',result_srch=result_srch)
        


@app.route('/',methods=['GET','POST'])
def send():
    if request.method == 'POST':
        msg = request.form['msg']
        keyword = request.form['keyword']
        if not msg:
            alert = '入力してください'
            return render_template('index.html',alert=alert)
        if not keyword:
            keyword= '入力してください'
            return render_template('index.html',alert=alert)

        else:
            date_time = datetime.datetime.today()
            data_id = date_time.strftime("%Y%m%d%H%M")
            con = sqlite3.connect('todo.db')
            c = con.cursor()
            c.execute('INSERT INTO message VALUES(?,?,?,?)',(data_id,msg,keyword,date_time))
            con.commit()
            result = con.execute("""select * from message order by data_id desc""")
            return render_template('index.html',result = result)

@app.route('/delete_data',methods=['GET','POST'])
def delete_data():
    if request.method == 'POST':
        data_ids = request.form['action']
        con = sqlite3.connect('todo.db')
        c = con.cursor()
        query = "DELETE FROM message WHERE data_id=?"
        c.execute(query,(data_ids,))
        con.commit()
        result = con.execute('''select * from message order by data_id desc''')
        return render_template('index.html',result=result)

if __name__ == '__main__':
    app.debug = True
    app.run()


