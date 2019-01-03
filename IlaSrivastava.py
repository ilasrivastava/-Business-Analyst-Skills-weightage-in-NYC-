#Ila Srivastava Homework 7 Project
#importing libraries
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plot
import csv
VAR='C:/Users/ilasr/Dropbox/New folder/PYTHON/GlassdoorJobs.csv'


#creating csv file to store job related information for jobs having rating more tham 3.5
#The following code came from https://realpython.com/python-csv/
with open(VAR,'w',encoding='utf-8') as destinationFile:
    writer =csv.writer(destinationFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Company Name','Position','Rating','Link to Job Posting'])
#End of code from https://realpython.com/python-csv/
    
#list for url of first 4 pages of glassdoor
list_of_urls=['/Job/new-york-business-analyst-jobs-SRCH_IL.0,8_IC1132348_KO9,25.htm','/Job/new-york-business-analyst-jobs-SRCH_IL.0,8_IC1132348_KO9,25_IP2.htm','/Job/new-york-business-analyst-jobs-SRCH_IL.0,8_IC1132348_KO9,25_IP3.htm']
#for loop for url and functioncalled at the end of code

#function 1: to print title and count of job openings
def title(soup):    
    print("\t\t\t\t\t\t",(soup.title).get_text(),"\t\t\t\t\t\t")
    for count in soup.find_all(name="p",attrs={"class":"jobsCount"}):
        print("\t\t\t\t\t\t\tJob count:",count.get_text(),"\t\t\t\t\t\t\t")

    
#function 2: to fetch all job details
def jobDetails(soup):    
    #initializing variables for count of each skill.For ex:if "Excel" appears once in job desc then e=1 etc.
    sql=0
    l=0
    e=0
    r=0
    p=0
    b=0
    w=0
    c=0
    a=0
    #extracting company name
    for d in soup.find_all(name="li",attrs={"class":"jl"}):
        i=d['data-id']
        for loc in d.find_all(name="div" ,attrs={"class":"flexbox empLoc"}):
            loc2=loc.get_text()
	    #data cleaning
            pos=loc2.index(" – ")
            loc3=loc2.replace(loc2[pos:len(loc2)],'')
            print("\n\n\nCompany Name: ",loc2[0:pos])
            #extracting location
            for loc1 in loc.find_all(name="span",attrs={"class":"subtle loc"}):
                print("Location: ",loc1.get_text())
            #extracting days when job was posted
            for days in loc.find_all(name="span",attrs={"class":"hideHH nowrap"}):
                if len(days.get_text())==0:
                    days=0
                    #print(days)
                    for daysagn in d.find_all(name="div",attrs={"class":"flexbox"}):
                        for days1 in daysagn.find_all(name="span",attrs={"class":"hideHH nowrap"}):
                            print("When posted: ",days1.get_text())
                else:
                    print("When posted: ",days.get_text())
	#extracting job title
        for jobtitle in d.find_all(name="div" ,attrs={"class":"flexbox jobTitle"}):            
            for jobname in jobtitle.find_all(name="a"):
                print("Position:",jobname.get_text())
	#extracting rating for each job
        for rating in d.find_all(name="div",attrs={"class":"logoWrap"}):
            for star in rating.find_all(name="span",attrs={"class":"compactStars"}):
                print("Rating: ",star.get_text())
                #extracting link within each job which directs me to job description html code to extract job description
                link=rating.find("a")
                get_link=link.get('href')
                page_link='https://www.glassdoor.com'+get_link
                print("Link: ",page_link)
                k1=r'https'+'://www.glassdoor.com'+get_link
                req1=Request(k1, headers={'User-Agent': 'Mozilla/5.0'})
                url1 = urlopen(req1).read()
                soup1 = BeautifulSoup(url1, 'html.parser')
                for desc in soup1.find_all(name="div",attrs={"id":"JobDesc"+i}):
                    print("Job description: ",desc.get_text())
                    desc1=desc.get_text()
		    #replacing all other characters in job description
                    desc2=desc1.replace('\'','').replace(',','').replace('(','').replace(')','').replace('.','').replace(':','').replace('-','').replace('.','')
                    list=[]
                    list=desc2.split(' ')
		    #removing multiple occurences of skill in job description
		    # The following code came from https://www.geeksforgeeks.org/python-remove-duplicates-list/
                    finallist=[]
                    for k in list:
                        if k not in finallist:
                            finallist.append(k)                            
		     #End of code from  https://www.geeksforgeeks.org/python-remove-duplicates-list
                    for l in finallist:
                        if l.lower()=='sql':
                            sql=sql+1
                        if l.lower() in('bachelors','ba/bs' ,'master','ba','bs','masters','bachelor'):
                            b=b+1
                        if l.lower()=='r':
                            r=r+1
                        if l.lower()=='excel':
                            e=e+1
                        if l.lower()=='powerpoint':
                            p=p+1
                        if l.lower()=='word':
                            w=w+1
                        if l.lower()=='communication':
                            c=c+1
                        if l.lower() in('agile','waterfall','sdlc'):
                            a=a+1                                           
				
	#extracting salary  
        for salary in d.find_all(name="div",attrs={"class":"flexbox"}):
            for sal in salary.find_all(name="span",attrs={"class":"green small"}):
                print("Salary: ",sal.get_text())
                sal1=sal.get_text().replace('$','').replace('k','').replace('(Glassdoor Est.)','')                   
	#extracting listing for example:whether hiring or hot in list
        for listing in d.find_all(name="div",attrs={"class":"hotListing"}):
            print("Listing: ",listing.get_text())
        #extracting additional features whether easy apply or not
        for eapp in loc.find_all(name="div",attrs={"class":"alignRt"}):
            if len(eapp.get_text())!=0:
                print("This job has feature Easy apply")
            else:
                print("Not easy apply")
				
	#if rating more than 3.5 add to excel file       
        if float(star.get_text())>3.5:
            try:
                destinationFile=open(VAR,'a')
                #The following code came from https://realpython.com/python-csv/
                csvdata=[loc2[0:pos],jobname.get_text(),star.get_text(),page_link]
                writer =csv.writer(destinationFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(csvdata)
                #End of code from https://realpython.com/python-csv/
            except PermissionError:
                print('Please close any program using GlassdoorJobs.csv and try again')
            finally:
                destinationFile. close()
    all_total=[sql,b,r,e,p,w,c,a]
    return all_total
				
	   
					
#creating pie chart for top trending skill for Business Analyst.Passing sum of each skills stored in a list as value       
def piechart(value):    
    labels = 'SQL','Bachelor or Master degree','R language','Excel','Power Point','Word','Communication skills','SDLC methologies'
    fracs = [value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7] ]
    explode = [0, 0, 0, 0, 0, 0, 0.1,0]
    plot.axes(aspect=1)    
    plot.title('Skills weightage for Business Analyst jobs in NY')
    plot.pie(x=fracs, labels=labels, explode=explode,autopct='%3.1f %%',shadow=True, labeldistance=1.0, startangle = 90,pctdistance = 0.6)
    plot.legend(loc='upper left', numpoints=1,bbox_to_anchor=(0.9, 1))
    plot.show()
    
#function to view additional details related to job search      
def additional_info(soup):
    for div in soup.find_all(name="div",attrs={"class":"pageContentWrapper"}):
        for topcities in div.find_all(name="div",attrs={"class":"links-group"}):
            print("\n\n",topcities.get_text())               

for u in list_of_urls:    
    urls=r'https'+'://www.glassdoor.com'+u
    #glassdoor has some security feature that blocksus to scrape websiteand throwserror "urllib.error.HTTPError: HTTP Error 403: Forbidden".Therefore I user browser agent to access it.
    #The following idea came from https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
    req=Request(urls, headers={'User-Agent': 'Mozilla/5.0'})    
    url = urlopen(req).read()
    #using BeautifulSoup to parse html page
    soup = BeautifulSoup(url, 'html.parser')
    #Calling all functions
    #title only needs to be printed initially
    if u in ('/Job/new-york-business-analyst-jobs-SRCH_IL.0,8_IC1132348_KO9,25.htm'):
        title(soup)
    value=jobDetails(soup)        
    additional_info(soup)
    piechart(value)
    




    


           











