#!/bin/python
#-*- coding:utf-8 -*-
import sys
import re
import pandas as pd
import numpy as np
from collections import deque
from flask import *
import xlwt
import StringIO

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
#url_for('static', filename='echarts.js')

option = {
            "title": {
                "text": 'ECharts 入门示例'
            },
            "tooltip": {},
            "legend": {
                "data":['销量']
            },
            "xAxis": {
                "data": ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
            },
            "yAxis": {},
            "series": [{
                "name": '销量', 
                "type": 'bar',
                "data": [5, 20, 36, 10, 10, 20]
            }]
        }

@app.route('/')
def index():
	return render_template('home.html', name="Hahaha")

@app.route('/test')
def test():
	global option
	lst = [5, 20, 36, 10, 10, 20]
	return render_template('show.html', mydata = option)


@app.route('/linebar')
def linebar():
	lst = [5, 20, 36, 10, 10, 20]
	return render_template('linebar.html')

@app.route('/heatmap')
def heatmap():
	lst = [5, 20, 36, 10, 10, 20]
	return render_template('heatmap.html')

@app.route('/heatmap2')
def heatmap2():
	lst = [5, 20, 36, 10, 10, 20]
	return render_template('heatmap2.html')

@app.route('/excel')
def excel():
	response = make_response()
	response.headers['Content-type'] = 'application/vnd.ms-excel'
	response.headers['Transfer-Encoding'] = 'chunked'
	response.headers['Content-Disposition'] = 'attachment;filename="export.xls"'
	wb=xlwt.Workbook()
	wb.encoding='gbk'
	ws=wb.add_sheet('1')
	ws.write(0,1,'123')  #如果要写中文请使用UNICODE
	sio=StringIO.StringIO()
	wb.save(sio)   #这点很重要，传给save函数的不是保存文件名，而是一个StringIO流
	return sio.getvalue()
#该代码片段来自于: http://www.sharejs.com/codes/python/7265

if __name__=="__main__":
	app.run(host='0.0.0.0', debug=True)

#for k,v in dic.items():
#	print "k=",k
#	printList(v)
