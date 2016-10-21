############################################################
# Name : userDetailsQuora.py
# Date : Oct 19, 2016
# Author : Snigdha Praksh
# Description : This script is used to find all the possible users of Quora by entering their name 
#               and get their basic stats. It also points out if there are more number of users with the same name
############################################################

#Importing beutiful Soup
from bs4 import BeautifulSoup

#Importing urllib to read the read and access the url
import urllib.request

#Importing re package to use regex for data parsing
import re

#Defining functions to validate data for each options

#When the user chooses option 1
def validateInput1(inputName):
    print('\nProcessing in progress. Please wait...')
    inputUrl = "https://www.quora.com/profile/" + inputName
    try:
        resp = urllib.request.urlopen(inputUrl)
        return inputUrl		
    except:
        print(inputUrl + ' not found. Please validate the user name and run the script again')
        exit(1)

#When the user chooses option 2
def chooseURL(arrayURL):
    
    lenList = len(arrayURL)
    print('\nChoose one of the profile:\n')
    for count in range(lenList):
        print(str(count+1) + "." + arrayURL[count])

    option = input()
	
    if int(option) < lenList:
        for count in range(lenList):
            if option == str(count+1):
                return arrayURL[count]
    else:
        print('Invalid option. Exiting the script\n')
        exit(1)


def validateURL(inputName):
    print('\nProcessing in progress. Please wait...')
    #Initializing the list to store the result
    arrayURL = []
    baseURL = "https://www.quora.com/profile/" + inputName
    try:
        resp = urllib.request.urlopen(baseURL)
        arrayURL.append(format(baseURL))

    except:
        print('Unable to find ' + baseURL + '.Exiting the script\n')  
        exit(1)
    for n in range(1,50):
        fullURL = baseURL + "-" + str(n)
        try:
            resp = urllib.request.urlopen(fullURL)
            arrayURL.append(format(fullURL))

        except:
            break
    #Calling the function that asks users to choose the URL from the option		
    inputUrl = chooseURL(arrayURL)
    return inputUrl


def getUserName(inputName):
    if (' ' in inputName) == True:
        firstName = inputName.split()[0]
        lastName = inputName.split()[1]
        inputName = firstName + "-" + lastName
        inputUrl = validateURL(inputName)
        return inputUrl
    else:
        inputUrl = validateURL(inputName)
        return inputUrl

#Defining a function to take the input from the user
def takeInput():
    inputOption = input('\nChoose one of the option\n1. I know the exact profile name of the quora user\n2. I know the full name of the quora user\n')
    if inputOption == "1":
        inputName = input('Enter the profile name of the quora user (Note that name should be seperated with \'-\' and preceeded with number if any) : ')
		
		#Trimming unwanted spaces
        inputName = re.sub(' +','',inputName)
		
		#Calling validateInput1 function
        inputUrl = validateInput1(inputName)
        return inputUrl
    elif inputOption == "2":
        inputName = input('Enter the full name of the quora user(Format - FirstName LastName) : ')
		
		#Calling getUserName function
        inputUrl = getUserName(inputName)
        return inputUrl
    else:
        print('\nInvalid Input. Please try again with the correct input')
        inputName = takeInput()
        return inputName
    #return inputName
		
'''This is the starting point of execution.

Hierarchy is as follows - 
Main Function : takeInput()
SubFunctions:
	1. validateInput1 - Takes string as an argument
	2. getUserName - Takes string a input
		A.validateURL - Takes string as input
			i. chooseURL - Takes array as input
'''

#Calling the main function to take the input and get the final URL
finalURL = takeInput()

#Getting the basic details of profile choosen by the user
html = urllib.request.urlopen(finalURL).read()

#Parsing html tags using beautifulSoup
soup = BeautifulSoup(html,"html.parser")

#Extract only the profile name from the finalURL
profileName = finalURL.rsplit('/',1)[1]

userName = soup.find_all('span', attrs={'class':'user'})
noOfAnswers = soup.find_all('a', attrs={'href':'/profile/'+ profileName})
noOfQuestions = soup.find_all('a', attrs={'href':'/profile/' + profileName + '/questions'})
noOfPosts = soup.find_all('a',attrs={'href':'/profile/' + profileName + '/all_posts'})
noOfFollowers = soup.find_all('a', attrs={'href':'/profile/' + profileName + '/followers'})
noOfFollowings = soup.find_all('a', attrs={'href':'/profile/' + profileName + '/following'})
noOfEdits = soup.find_all('a', attrs={'href':'/profile/' + profileName + '/log'})

print("\n-------------------------------------------------------------------------------\n")
print('The profile can be viewed in details at - ' + finalURL)
print("\n--------------------BASIC DETAILS----------------------------------------------")

#Ensuring to pick the single user name
#print(userName[0])
for value in userName:
    print('Name : ', value.text)
    break
for value in noOfAnswers:
    if 'Answers' in value.text:
        #print(value.text + ":")
        print('No. of Answers : ', value.find('span').contents[0])
        
for value in noOfQuestions:
    print('No. of Questions : ', value.find('span').contents[0])
for value in noOfPosts:
    print('No. of Posts : ', value.find('span').contents[0])
for value in noOfFollowers:
    print('No. of Followers : ', value.find('span').contents[0])
for value in noOfFollowings:
    print('No. of Followings : ', value.find('span').contents[0])
for value in noOfEdits:
    print('No. of Edits : ', value.find('span').contents[0])


	
