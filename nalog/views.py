from django.shortcuts import render
from django.http import HttpResponse
from nalog.NalogLoader import NalogLoader
from datetime import datetime, timezone, timedelta

# Create your views here.
from nalog.models import Nalog

INN1 = 10
INN2 = 12
OGRN = 13


def index(request):
    delete_old_letters()
    data = request.GET.get("data", "NULL")
    elements = []

    if (len(data) == INN1 or len(data) == INN2):
        nalogs = find_inn_in_database(data)
    elif (len(data) == OGRN):
        nalogs = find_ogrn_in_database(data)
    else:
        nalogs = []

    if len(nalogs) != 0:
        for nalog in nalogs:
            elements.append(nalog.letter)
    else:
        downloaded_data = NalogLoader().download_n_parse(data)
        if downloaded_data['rowCount'] == 0:
            elements = ["Not exits"]
        nalog_list = convert_data_to_nalog_list(downloaded_data)
        for nalog in nalog_list:
            elements.append(nalog.letter)
        #elements.append("UPDATED")
        add_nalog_list_to_database(nalog_list)

    return render(request, "nalog.html", context={"elements": elements, "request": data})


def delete_old_letters():  # TODO NOTE: Так лучше не делать, предпочтительнее закинуть в фоновую задачу, к примеру, через сельдерей. В C# умею, в питоне пока не научился
    nalogs = Nalog.objects.all()
    for nalog in nalogs:
        if datetime.now(timezone.utc) - nalog.time >= timedelta(minutes=5):
            nalog.delete()


def find_inn_in_database(inn):
    try:
        return Nalog.objects.filter(inn=inn)
    except:
        return None


def find_ogrn_in_database(ogrn):
    try:
        return Nalog.objects.filter(ogrn=ogrn)
    except:
        return None


def convert_data_to_nalog_list(data):
    nalog_list = []
    for raw_data in data['data']:
        nalog = Nalog()
        nalog.letter = raw_data
        nalog.inn = raw_data['inn']
        nalog.ogrn = raw_data['ogrn']
        nalog_list.append(nalog)
    return nalog_list


def add_nalog_list_to_database(nalog_list):
    for nalog in nalog_list:
        add_nalog_to_database(nalog)


def add_nalog_to_database(nalog):
    nalog.save()
