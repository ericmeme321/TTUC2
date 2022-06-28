from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django import template

register = template.Library()

import datetime
import time
import sys

from .DataBase import SelectTable

def index(request):
    today_for_html = datetime.datetime.now().strftime('%Y-%m-%d')
    selectItem = ['PartitionKey', 'RowKey', 't0700', 't0720', 't0740', 't0800', 't0820', 't0840', 't0900', 't0920', 't0940', 't1000', 't1020', 't1040', 't1100', 't1120', 't1140', 't1200', 't1220', 't1240', 't1300', 't1320', 't1340', 't1400', 't1420', 't1440', 't1500', 't1520', 't1540', 't1600', 't1620', 't1640', 't1700', 't1720', 't1740', 't1800']

    selectDate = ['']
    recordDay = ''
    if request.method == 'POST':
        recordDay = request.POST['begin_date']
        startDay = datetime.datetime.strptime(request.POST['begin_date'].replace("-",""),'%Y%m%d')
        try:
            if request.POST['multiple']:
                yesterday = startDay + datetime.timedelta(days=-1)
                selectDate[0] = startDay.strftime('%Y%m%d')
                selectDate.append(yesterday.strftime('%Y%m%d'))
        except:
            selectDate[0] = startDay.strftime('%Y%m%d')
    else:
        recordDay = datetime.datetime.now().strftime('%Y-%m-%d')
        selectDate[0] = datetime.datetime.now().strftime('%Y%m%d')

    table1 = SelectTable()
    output = table1.selectOneDay(selectDate[0])
    
    if len(selectDate) == 1:
        selectItem[0] = "Gateway SN"
        
        selectItem.insert(1, "縣市")
        selectItem.insert(2, "連線型別")
        selectItem.insert(3, "斷線型別")
        selectItem.insert(4, "嚴重斷線")
        selectItem.insert(5, "曾經斷線超過一小時恢復")

        for i in range(6, len(selectItem) ):
            selectItem[i] = selectDate[0] + "\n" + selectItem[i]
        selectItem.pop(6)

        output = table1.judgeOneDay()
        
    if len(selectDate) == 2:
        table2 = SelectTable()
        output = table1.mergeTwoDay(table2.selectOneDay('20200730'))
        output = table1.judgeTwoDay()
        
        selectItem += selectItem
        selectItem[0] = "Gateway SN"
        selectItem.pop(36)
        selectItem.pop(36)
        selectItem[1] = "持續斷線"
        selectItem.insert(1, "縣市")

        for i in range(2, (int)(len(selectItem) / 2)  + 1 ):
            selectItem[i] = selectDate[1] + "\n" + selectItem[i]
        for i in range( (int)(len(selectItem) / 2) + 1, len(selectItem) ):
            selectItem[i] = selectDate[0] + "\n" + selectItem[i]

    if len(selectDate) > 1:
        filename = selectDate[1] + '~'+ selectDate[0]
    else:
        filename = selectDate[0]

    return render(request, 'index.html', locals())