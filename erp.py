from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import os
from datetime import datetime
import webdriver_manager
import selenium
import sys
import argparse

print("#####################This Program is Tested With######################")
print(f"python version of this device : {sys.version}")
print(f"selenium version of this device: {selenium.__version__}")
print(f"webdriver_manager version of this device :  {webdriver_manager.__version__}")
print("The program is tested with python  3.9.6, selenium 4.25.0 &\nwebdriver_manager  4.0.2")
print("#####################################################################")


parser = argparse.ArgumentParser(description="A simple argument parser example.")
    
# Add arguments
parser.add_argument('-u', '--username', type=str, help='Your ERP username', required=True)
parser.add_argument('-p', '--password', type=str, help='Your ERP Password', required=True)
parser.add_argument('-sm', '--semester', type=str, help='Enter Semester ', required=True)
parser.add_argument('-sb', '--subject', type=str, help='Enter Subject ', required=True)
parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')

# Parse the arguments
args = parser.parse_args()

# Access the arguments
#print(f"Hello, {args.username}!")
#print(f"You are {args.password} years old.")
 
username=args.username
password= args.password  
semester=args.semester
subject=args.subject
print(f"Hi {username}, you have chosen Semester: {semester} \nSubjects : {subject} for ERP Attendance Script")
print("#####################################################################")   
if args.verbose:
 print("Verbose mode is enabled.")
##############################################################

def read_nth_column(file_path, n, separator): 
    column_data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace and split the line into columns
            columns = line.strip().split(separator)
            if len(columns) > n:  # Check if the nth column exists
                column_data.append(columns[n])
    return column_data

file_name = "date_loader.txt"
dates = read_nth_column(file_name, 0, ";")
modes = read_nth_column(file_name, 1, ";")
sl = read_nth_column(file_name, 2, ";")


min_date = min(dates)
max_date = max(dates)

f=min_date 
t=max_date 
print(f"You have entered Starting Date: {f} & Last Date : {t} in date_loader.txt")
#print(sl)

# Optionally, you can use ChromeDriverManager for automatic management of the driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# If using a downloaded chromedriver
# driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

driver.get('http://10.0.2.45:8082/CLXOAuthServer/')
driver.maximize_window()
# Perform actions...
username_input = driver.find_element(By.ID, "j_username")
username_input.send_keys(username)
password_field = driver.find_element(By.NAME, 'j_password')
password_field.send_keys(password)

try:
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'buttonui') and normalize-space(text())='Login']"))
    )
    button.click()
except Exception as e:
    print(f"Error: {e}")
print(f"successfully logged in with {username} credentials")
# Keep the browser open for a while to see the result (for demonstration)
# Locate the element by its id and click it
webkiosk_li = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "Webkiosk (Staff)"))
)
webkiosk_li.click()


# Wait until the link is clickable
link = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='widgetgroup']/div/a/div/div[2]"))
)
link.click()
print("Web Kiosk Opened")
# Wait until the dropdown is visible and click to open the options
dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'institute_chosen'))
)
dropdown.click()

# Wait until the specific option with data-option-array-index="1" is visible and click on it
option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-option-array-index='1']"))
)
option.click()

# Locate the "SUBMIT" link and click it
submit_button = driver.find_element(By.XPATH, "//a[contains(@class, 'btn') and text()='SUBMIT']")
submit_button.click()

academic_info = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Academic Info']"))
)
academic_info.click()

# Wait until the anchor element containing "Student Attendance Entry" is clickable, then click it
attendance_entry_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Student Attendance Entry')]"))
)
attendance_entry_link.click()

# Wait until the <span> element containing "Select Semester" is clickable, then click it
select_semester_span = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Select Semester']"))
)
select_semester_span.click()


# Wait until the list item containing "ODD SEM 2024 - ITER" is clickable, then click it
semester_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, f"//li[@data-option-array-index='1' and text()='{semester}']"))
    
    #EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-option-array-index='1']"))
)
semester_option.click()

# Wait until the <span> element containing "Select" is clickable, then click it
select_span = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Select']"))
)
select_span.click()


# Wait until the list item containing "ODD SEM 2024 - ITER" is clickable, then click it
subject_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, f"//li[@data-option-array-index='1' and text()='{subject}']"))
)
subject_option.click()



###################################################

date_from = driver.find_element(By.NAME, "datefrom")  # Adjust the selector as needed
date_from.clear()  # Clear any existing text
date_from.send_keys(f)  # Insert your desired text

date_to = driver.find_element(By.NAME, "dateto")  # Adjust the selector as needed
date_to.clear()  # Clear any existing text
date_to.send_keys(t)  # Insert your desired textprint(f"{absent_radio_button_id} is clicked")


load_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-success.btn-md")
load_button.click()  # Click the Load button

print(f"Date range: {f} to {t} is loaded in ERP")




###################################################

for i in range(0, len(dates)):
    target_date = dates[i]
    mode = modes[i]
    #######################################################
    date_link = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{target_date}')]"))
    )
    date_link.click() 
    print(f"target date: {target_date} link clicked")
    #######################################################
    #print(f"full sl: {sl[i]}")    
    if(mode=="P"):
     s="absent"
     s_inv="present"
    else:
     s="present"
     s_inv="absent"
    status_radio_button = WebDriverWait(driver, 10).until(
         EC.element_to_be_clickable((By.ID, f"all{s}"))
    )
    status_radio_button.click()
    print(f"All {s} of target date: {target_date} link is clicked")
    ###################################################################
    sl_list = sl[i].split(", ") ##split by comma
    for j in range(len(sl_list)):
     print(f"sl list {sl_list[j]}")
     #students=sl_list[j]
     students= sl_list[j].replace(" ", "")
     student=int(students)-1 # Callibration of given Serial Number with ERP Serial Number
     ###################################################################
     absent_radio_button_id = f"status{s_inv}{student}"  
     print(absent_radio_button_id)
     absent_radio_button = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.ID, absent_radio_button_id))
     )
     absent_radio_button.click()
     print(f"{absent_radio_button_id} is clicked")   
  
    save_attendance_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Save Attendance')]"))
    )
    save_attendance_button.click()
    print(f"Attendance of {target_date} of \nSerial number: {sl_list} is uploaded in ERP ")
######################################################


print(f"\033[31m{username} all your attendance successfully uploaded in ERP\033[0m")
#driver.quit()
