#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Need to Import Selenium Webdriver and several of its components for the Web Interaction Package 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


#Opens the file to be analyzed, so paste the text path into this portion of the open statement for the file containing your protein sequence 
file = open('Protein.txt','r')

#Reads the desired file
data = file.read()

#Creates an empty list to populate with the file contents 
AA = []

#Separates the Peptide String into Nonomer or 9 AA lengths for easier processing with the tool
AA = [data[i:i+9] for i in range(0, len(data), 9)]

#Adds spaces before and after each item in the list with the Nonomers to separate each item when populating the tool
AA2 = [' {} '.format(i) for i in AA]

#Starts up Chrome (can substitute any browser that has the right driver, for example Chrome has Chrome Driver for web-based applications)
br = webdriver.Chrome()

#Waits for the page to get done loading before it does anything with it
br.implicitly_wait(15)

#Command to pull up the specific webpage and in this case, the tool from IEDB
br.get('http://tools.iedb.org/immunogenicity/')

#To fill out the page with the desired info:
#First, Need to use this to find the text box to be populated with the desired protein sequence and Nonomers
search = br.find_element_by_id('id_sequence_text')

#Waits for the page to get done loading before it does anything with it
br.implicitly_wait(15)

#This If Statement Asks the User for input as to whether the Default or a Custom Masking Option is going to be used for analysis
#Enter either Default or default for the base case for analysis
default = input(r'Do you want the Default or Customized Masking Option?')
if '%s' % default == 'Default':
    
    #Second, Need to send the information of the sequences over to the specific textbox
    #This will find the input box 
    search = br.find_element_by_id('id_sequence_text')
    
    #This will send the information on the separate Nonomers to the input box
    search.send_keys(AA2)
    
    #This will the full length peptide as well
    search.send_keys(AA)
    
    br.implicitly_wait(15)
    
    #Third, Need to find the Submit button on the page in order to get the sequences through the program
    search2 = br.find_element_by_name('submit')

    #Now this command will 'click' on the button and initiate the processing
    search2.click()

    #Waits for the page to get done loading before it does anything with it
    br.implicitly_wait(15)

    #This will now find the Download link for the results and will 'Click' it to start downloading to an excel format for further visualization
    search3 = br.find_element_by_link_text("Download result").click()
    
#This portion will ask the user to input the specific allele to be used for the Custom Masking Option 
else:
    while True:
        desiredoption = input(r"What HLA type would you like to use for Masking? (Example is HLA-A0201)")
        
        #Tries to match the input to the drop down menu options available
        try:
            maskoptions = Select(br.find_element_by_id('id_allele'))
            maskoptions.select_by_visible_text('%s' % desiredoption)
            
        #Checks whether this error comes up from the program due to an incorrect input that 
        #does not match up with one of the available alleles
        except NoSuchElementException:
            
            #Tells the user that the entered input is not in the available selection of alleles and 
            #to retype a new allele for analysis
            print("{input} is not an available allele, please retype your desired allele".format(input = desiredoption))
            continue
            
        else:
            #Breaks the while loop to continue with the program
            break
            
    #Finds the textbox for the sequence input
    search = br.find_element_by_id('id_sequence_text')
    
    #Removes any sequences less than 9 AA's long because the IEDB tool will not take any sequences shorther than that for the custom option case
    #and will return an error when prompted
    #Does this by appending the list with only segments that contain more than 10 characters that include spaces surrounding them
    AA2 = [i for i in AA2 if len(i) > 10]
    
    #Sends the Full Length Sequence and the Broken up sequences to the tool for analysis 
    search.send_keys(AA)
    search.send_keys(AA2)
        
    #Now this command will 'click' on the button and initiate the processing
    br.implicitly_wait(15)
    
    #Third, Need to find the Submit button on the page in order to get the sequences through the program
    search2 = br.find_element_by_name('submit')
    search2.click()

    #Waits for the page to get done loading before it does anything with it
    br.implicitly_wait(15)

    #This will now find the Download link for the results and will 'Click' it to start to download to an excel format for further visualization
    search3 = br.find_element_by_link_text("Download result").click()


# In[ ]:




