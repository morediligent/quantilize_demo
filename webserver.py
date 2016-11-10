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
from collections import defaultdict
import random
import json
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
#url_for('static', filename='echarts.js')
fin=open("zhailist.csv", 'r')
fin.readline()

dic = defaultdict(dict)

for line in fin:
	#if N>=5:
	#	break
	lineu = line.strip().decode("gb18030")
	#print lineu
	#s = "startdate=2001-01-01;enddate=2016-09-19;windcode=%s" % lineu
	#d = w.wset("guaranteedbond",s)
	lines = lineu.split(",")
	zhaiid = lines[0]
	hangye1 = lines[1].strip()
	hangye2 = lines[2].strip()
	if hangye1 == "0":
		continue
	if hangye2 == "0":
		continue
	dic[hangye1][hangye2] = 1

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

def testdataGenerator(cur_date="2016-11-01", prev_date=None, level1=None, level2=None):
	"""
	生成测试数据
	"""
	if prev_date==None and level1==None and level2==None: #某一天所有行业的风险值
		# generator data sequence
		lst = []
		for hangye1 in dic.keys():
			dic_item = {}
			shu = round(random.uniform(1,100), 2)
			#outline = "%s,level1,%s,%.2f" % (dat, hangye1, shu)
			dic_item[u"date"] = cur_date
			dic_item[u"level1"] = hangye1
			dic_item[u"level2"] = u"全部"
			dic_item[u"value"] = shu
			lst.append(dic_item)
			
		for hangye1 in dic.keys():
			for hangye2 in dic[hangye1].keys():
				dic_item = {}
				shu = round(random.uniform(1,100), 2)
				#shu1 = "%.2f" % (shu,)
				#outline = "%s,level2,%s,%.2f,%s" % (dat, hangye2, shu, hangye1)
				dic_item[u"date"] = cur_date
				dic_item[u"level1"] = hangye1
				dic_item[u"level2"] = hangye2
				dic_item[u"date"] = shu	
				lst.append(dic_item)
		outstr = json.dumps(lst, ensure_ascii = False)#.encode("utf-8")
		return outstr
	elif prev_date == None and level2 == None and not level1 == None: #某一天某一级行业的风险值
		lst = []
		for hangye1 in dic.keys():
			if not hangye1 == level1:
				continue
			dic_item = {}
			shu = round(random.uniform(1,100), 2)
			#outline = "%s,level1,%s,%.2f" % (dat, hangye1, shu)
			dic_item[u"date"] = cur_date
			dic_item[u"level1"] = hangye1
			dic_item[u"level2"] = u"全部"
			dic_item[u"value"] = shu
			lst.append(dic_item)
			
		for hangye1 in dic.keys():
			if not hangye1 == level1:
				continue		
			for hangye2 in dic[hangye1].keys():

				dic_item = {}
				shu = round(random.uniform(1,100), 2)
				#shu1 = "%.2f" % (shu,)
				#outline = "%s,level2,%s,%.2f,%s" % (dat, hangye2, shu, hangye1)
				dic_item[u"date"] = cur_date
				dic_item[u"level1"] = hangye1
				dic_item[u"level2"] = hangye2
				dic_item[u"value"] = shu	
				lst.append(dic_item)
		outstr = json.dumps(lst, ensure_ascii = False)#.encode("utf-8")
		return outstr	
	elif prev_date == None and not level2 == None and not level1 == None: #某一天某一级和二级行业的风险值
		lst = []
		"""
		for hangye1 in dic.keys():
			if not hangye1 == level1:
				continue
			dic_item = {}
			shu = round(random.uniform(1,100), 2)
			#outline = "%s,level1,%s,%.2f" % (dat, hangye1, shu)
			dic_item[u"日期"] = cur_date
			dic_item[u"第一行业"] = hangye1
			dic_item[u"第二行业"] = u"全部"
			dic_item[u"数值"] = shu
			lst.append(dic_item)
		"""
			
		for hangye1 in dic.keys():
			if not hangye1 == level1:
				continue		
			for hangye2 in dic[hangye1].keys():
				if not hangye2 == level2:
					continue			
				dic_item = {}
				shu = round(random.uniform(1,100), 2)
				#shu1 = "%.2f" % (shu,)
				#outline = "%s,level2,%s,%.2f,%s" % (dat, hangye2, shu, hangye1)
				dic_item[u"date"] = cur_date
				dic_item[u"level1"] = hangye1
				dic_item[u"level2"] = hangye2
				dic_item[u"value"] = shu	
				lst.append(dic_item)
		outstr = json.dumps(lst, ensure_ascii = False)#.encode("utf-8")
		return outstr	
	elif not prev_date == None and not cur_date == None and not level1 == None and not level2 == None:
		lst = []
		beginTime = time.strptime(prev_date, "%Y-%m-%d")
		beginTimeStamp = int(time.mktime(beginTime))
		dt1 = datetime.datetime.utcfromtimestamp(beginTimeStamp)
		dt1 = dt1 + datetime.timedelta(hours = 8)
		
		endTime = time.strptime(cur_date, "%Y-%m-%d")
		endTimeStamp = int(time.mktime(endTime))
		dt2 = datetime.datetime.utcfromtimestamp(endTimeStamp)
		dt2 = dt2 + datetime.timedelta(hours = 8)
		
		lst_dt = []
		dt_n = dt1
		while dt_n <= dt2:
			lst_dt.append(dt_n)
			dt_n += datetime.timedelta(days = 1)
		print lst_dt
		
		for hangye1 in dic.keys():
			if not hangye1 == level1:
				continue		
			for hangye2 in dic[hangye1].keys():
				if not hangye2 == level2:
					continue
				for adate in lst_dt:
					dic_item = {}
					shu = round(random.uniform(1,100), 2)
					#shu1 = "%.2f" % (shu,)
					#outline = "%s,level2,%s,%.2f,%s" % (dat, hangye2, shu, hangye1)
					dic_item[u"date"] = adate.strftime("%Y-%m-%d")
					dic_item[u"level1"] = hangye1
					dic_item[u"level2"] = hangye2
					dic_item[u"value"] = shu	
					lst.append(dic_item)
		outstr = json.dumps(lst, ensure_ascii = False)#.encode("utf-8")
		return outstr		
	else:
		return "hello world!"
		#fout.write(json.dumps(dic_item, ensure_ascii=False).encode("utf-8") + ",\n" )	

	
@app.route('/')
def index():
	#return render_template('home.html', name="Hahaha")
	#return testdataGenerator(cur_date = "2016-11-02", level1 = u"房地产")
	#return testdataGenerator(cur_date = "2016-11-02", level1 = u"房地产", level2 = u"房地产开发")
	return testdataGenerator(cur_date = "2016-11-02", prev_date = '2016-10-01', level1 = u"房地产", level2 = u"房地产开发")

@app.route('/test', methods=['GET', 'POST'])
def test():
	#global option
	#lst = [5, 20, 36, 10, 10, 20]
	#return render_template('show.html', mydata = option)
	cur_date = request.form['cur_date'] | "2016-11-02"
	prev_date = request.form['prev_date'] | "2016-10-01"
	level1 = request.form['level1'] | u"房地产"
	level2 = request.form['level2'] | u"房地产开发"
	#return testdataGenerator(cur_date = cur_date, level1 = level1, level2 = level2)
	return testdataGenerator(cur_date = cur_date, prev_date = prev_date, level1 = level1, level2 = level2)
	
@app.route('/quantize')
def quantize():
	return render_template('quantize.html')

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
