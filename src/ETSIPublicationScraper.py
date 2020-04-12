from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd


# Primera extracción de la web
def primeraextracción (web):
    response = get(web)
    web_soup=BeautifulSoup(response.text, 'html.parser')
    type(web_soup)
    return web_soup

# Construcción de los enlaces a utilizar después
def extraccion (web_soup):
    anames = []
    alinks = []
    
    ases=web_soup.findAll('a')
    for a in ases:
        specnumber=a.text
        anames.append(specnumber)
    
        speclink=a['href']
        alinks.append(speclink)
    
    # Construimos los enlaces
    urls=[]

    for aname in anames:
        urla=web+aname
        if "[To Parent Directory]" in urla:
            pass
        else:
            urls.append(urla)

    # Scrape de cada URL generada en las líneas anteriores y extracción de Nombre de specificación, fecha, Release y version
    specs=[]
    dates=[]
    contents = []    
    for url in urls:
        responsess=get(url)
        allweb_soup=BeautifulSoup(responsess.text,'html.parser')
        type(allweb_soup)
        for i in range(len(allweb_soup)):
            versions=allweb_soup.findAll('a')
            for version in versions:
                
                specs.append(url)
                
                content=version.text
                if content == "[To Parent Directory]":
                    pass
                else:
                    if '0' in content:
                        contents.append(content)
                    elif '1' in content:
                        contents.append(content)
                    else:
                        pass   
            
            #Buscamos las fechas de publicación
            textos = allweb_soup.findAll(text=True)
            for texto in textos:
                date=re.search(r'(\d+/\d+/\d+)',texto)
                if date is not None:
                    dates.append(date.group())
                else:
                    pass
                
    #Sacamos los nombres de las specificaciones de los enlaces
    specslink = [ ele for ele in specs ] 
    for a in urls: 
        if a in specs:
            specslink.remove(a)

    specsclean=[]
    for a in specslink:
        specsclean.append(a.replace(web,""))
    
    #Finalmente extraemos de las "a" que habiamos almacenado en content los releases y las versiones
    rels=[]
    vers=[]

    for rel in contents:
        rels.append(rel[0:2])
        vers.append(rel[3:])

    #Guardamos todo en un dataframe y lo envíamos a un csv
    specsFinal=pd.DataFrame(columns=['Spec','Date','Release','Version'])
    specsFinal['Spec']=specsclean
    specsFinal['Date']=dates
    specsFinal['Release']=rels
    specsFinal['Version']=vers

    #Enviamos a CSV
    specsFinal.to_csv('Specs200_299.csv')
    return 

# Ejecutamos las funciones
web = 'https://www.etsi.org/deliver/etsi_ts/102200_102299/'

primera=primeraextracción(web)
final=extraccion(primera)