from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
# from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1>Hello</h1>")
    category=""
    location=""
    print("showing....")
    try:
        category=request.GET['jobrole']
        location=request.GET['joblocation']
        print(category)
        print(location)
    except:
        pass
    details=scrap_internshala(request, category, location)

    simplyhired_details=scrap_simplyhired(request, category, location)

    return render(request,"index.html",context={'details':details,'simplyhired_details':simplyhired_details})

# def about(request):
#     return render(request,"about.html")

# def contact(request):
#     return render(request,"contact.html")


def scrap_internshala(request,category,location):
    # print(location)
    # loc="internship-in-"
    # loc=loc+location
    # print(loc)
    # if len(loc)>14:
    #     location=loc
    # print(location)
    dynamic_url="https://internshala.com/internships/"+category+location
    url="https://internshala.com/internships/"
    print(dynamic_url)
    print(len(dynamic_url))
    if len(dynamic_url) >40:
        r=requests.get(dynamic_url)
        print("dynamic url")
    else:
        r=requests.get(url)
        print("SimpleUrl")
# https://internshala.com/internships/backend-development-internship-in-bangalore/

    # url="https://internshala.com/jobs/web-development-jobs/"

    # r=requests.get(url)
    soup = bs(r.text,"lxml")
    links = soup.find_all('h3', {'class': 'heading_4_5 profile'})
    names=[]
    apply_links=[]
    stipendd=[]
    work_loc=[]
    starter="https://internshala.com/"
    for link in links:
        for a in link.find_all('a'):
            names.append(a.text)
            apply_links.append(starter + a['href'])

    links_stipend = soup.find_all('span', {'class': 'stipend'})
    for stipend in links_stipend:
        stipendd.append(stipend.text)
    
    work_location = soup.find_all('a', {'class': 'location_link view_detail_button'})
    for loc in work_location:
        work_loc.append(loc.text)

    details = [{'title': title, 'apply': apply,'stipends':stipends} for title, apply,stipends in zip(names, apply_links,stipendd)]
    details=details[:10]
    # print(details)
    return details


def scrap_simplyhired(request,category,location):
    # if len(location)<=1:
    #     location="India"
    url="https://www.simplyhired.co.in/search?q=&l=India"
    print(url)
    r=requests.get(url)
    soup = bs(r.text,"lxml")
    links = soup.find_all('h3', {'class': 'jobposting-title'})
    names=[]
    apply_links=[]
    starter="https://www.simplyhired.co.in/"
    for link in links:
        for a in link.find_all('a'):
            names.append(a.text)
            apply_links.append(starter + a['href'])

    simplyhired_details = [{'title': title, 'apply': apply} for title, apply in zip(names, apply_links)]
    return simplyhired_details