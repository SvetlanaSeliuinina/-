import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import codecs
import folium
def get_data(url):
    page=pd.read_html(url,encoding='CP1251')
    header=page[6].drop(12).T
    header=header.iloc[1]
    header[0]='Номер УИК'
    data=page[7].drop(12).T
    data.columns=header
    data.reset_index()
    return data

def to_numeric(data):
    data.iloc[:,0]=[int(i.split()[1][1:]) for i in data.iloc[:,0]]
    for i in range(1,12):
        data.iloc[:,i]=pd.to_numeric(data.iloc[:,i])
    for i in range(12,15):
        l=[]
        perc=[]
        for a in data.iloc[:,i]:
            a=a.split()
            l.append(int(a[0]))
            perc.append(float(a[1][:-2]))
        data.iloc[:,i]=l
        data['%% за '+str(data.columns.values[i])]=perc
    return data

url17='http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217434&type=222'

data=get_data(url17)
data=to_numeric(data)

work = data.iloc[:, [0,1,3,4,15,16,17]]
work['Число избирательных бюллетеней, выданных избирателям'] = work.iloc[:,2:4].sum(axis=1)
work = work.drop(columns=['Число избирательных бюллетеней, выданных избирателям в помещении для голосования в день голосования','Число избирательных бюллетеней, выданных избирателям, проголосовавшим вне помещения для голосования'])
work['Явка на участке %'] = 100*np.round(work['Число избирательных бюллетеней, выданных избирателям'].div(work['Число избирателей, внесенных в список избирателей на момент окончания голосования'], axis=0),2)
group = work['Явка на участке %'].value_counts()

with pd.ExcelWriter('data.xlsx', engine='xlsxwriter') as writer:
    data.to_excel(writer, sheet_name='Изначальная_таблица')
    work.to_excel(writer, sheet_name='Рабочая_таблица')
    group.to_excel(writer, sheet_name='Рабочая_таблица', startrow=0, startcol=9, header=['Количество'], index=True)
    workbook = writer.book
    worksheet = writer.sheets['Рабочая_таблица']
    chart1 = workbook.add_chart({'type':'scatter'})
    for i in [3,4,5]:
        chart1.add_series({
            'name':     ['Рабочая_таблица', 0, i],
            'values':   ['Рабочая_таблица', 1, i, 47, i],
            'categories':   'Рабочая_таблица!$H$2:$H$48',
            'marker': {'type': 'circle', 'size': 7}
    })
    chart1.set_x_axis({'name': 'Явка на участке %'})
    chart1.set_y_axis({'name': '%% за кандитата'})
    chart2 = workbook.add_chart({'type':'scatter'})
    chart2.add_series({
        'values': 'Рабочая_таблица!$C$2:$C$48',
        'categories': 'Рабочая_таблица!$H$2:$H$48',
        'marker': {'type': 'circle', 'size': 7}
    })
    chart2.set_x_axis({'name': 'Явка на участке %'})
    chart2.set_y_axis({'name': 'Число избирателей на участке'})
    chart2.set_legend({'position': 'none'})
    chart3 = workbook.add_chart({'type':'scatter'})
    chart3.add_series({
        'values': 'Рабочая_таблица!$K$2:$K$20',
        'categories': 'Рабочая_таблица!$J$2:$J$20',
        'marker': {'type': 'circle', 'size': 7}
    })
    chart3.set_x_axis({'name': 'Явка на участке %'})
    chart3.set_y_axis({'name': 'Количество участков'})
    chart3.set_legend({'position': 'none'})
    worksheet.insert_chart('M1', chart1)
    worksheet.insert_chart('M16', chart2)
    worksheet.insert_chart('M31', chart3)
    writer.save()
file = codecs.open('lab3.kml', encoding='utf-8', mode='r')
html = file.read()
file.close()
bsoup = BeautifulSoup(html, 'lxml')
all = bsoup.kml.document.folder
folder = all.placemark
names = []
dolg = []
shir = []
while folder != None:
    if (folder.find("data", attrs={"name": "ТИК"})).value.text == "16.0":
        names.append(int(float((folder.find("name")).text)))
        dolg.append(float((folder.find("data", attrs={"name" : "Долгота"})).value.text))
        shir.append(float((folder.find("data", attrs={"name" : "Широта"})).value.text))
    folder = folder.find_next_sibling("placemark")
map = folium.Map(location=[59.94, 30.34], zoom_start = 13)
for i in range(len(names)):
    folium.Marker(
        location = [shir[i], dolg[i]],
        popup = 'УИК: ' + str(names[i]) +  ' Явка: '+ str(int(work.iloc[i, 6])) + '%'+ ' Амосов: ' + str(work.iloc[i, 2])+'%'+ ' Беглов: ' + str(work.iloc[i, 3])+'%'+ ' Тихонова: ' + str(work.iloc[i, 4])+'%'
    ).add_to(map)  
map.save("map.html")
