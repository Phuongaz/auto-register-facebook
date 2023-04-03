import json
import logging
import random
import re
import string
import time
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import colorama

service_obj = Service(r"C:\Users\BRAVO\py\auto\chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)

date = "15"
Month = "May"
year = "1997"

format = "[" + colorama.Fore.LIGHTBLUE_EX +  "%(asctime)s" + colorama.Fore.RESET + "] " + colorama.Fore.LIGHTGREEN_EX + "%(message)s" + colorama.Fore.RESET
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

def writen_to_file(username, password):
    with open(r"C:\Users\BRAVO\py\auto\data.txt", "a") as f:
        f.write("\n" + username + ":" + password)

def generate_random_email():
    domain = "snapmail.cc"
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@{domain}"

def start():
    driver.get(r"https://www.facebook.com/")
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.find_element(By.LINK_TEXT,"Create new account").click()
    logging.info("-----------------Create new account-----------------")
    first_names = {
        "Xuân", "Hạ", "Thu", "Đông", "Tuyết", "Tuấn", "Hải", "Hà", "Hương", "Hoa", "Hằng", "Hạnh", "Hồng", "Hà", "Phương", "Phượng", "Phúc", "Phú",
        "Anh", "Ánh", "An", "Ân", "Bình", "Bảo", "Bạch"
    }
    last_names = { "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương" }
    
    email = generate_random_email()
    first_name = random.choice(list(first_names))
    last_name = random.choice(list(last_names))
    logging.info("Email: " + colorama.Fore.BLUE + f" {email}")
    logging.info("First Name: " + colorama.Fore.BLUE + f" {first_name}")
    logging.info("Last Name: " + colorama.Fore.BLUE + f" {last_name}")
    
    driver.find_element(By.XPATH,"//input[@name='firstname']").send_keys(first_name)
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='lastname']").send_keys(last_name)
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='reg_email__']").send_keys(email)
    time.sleep(3)
    driver.find_element(By.XPATH,"//input[@name='firstname']").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//input[@name='reg_email_confirmation__']").send_keys(email)
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='reg_passwd__']").send_keys("123456789@123")
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@value='2']").click()

    Dates = driver.find_elements(By.XPATH,"//select[@id='day']/option")
    logging.info("Number of Dates: " + colorama.Fore.BLUE + f" {len(Dates)}")

    driver.find_element(By.XPATH,"//select[@id='day']/option").click()

    for D in Dates:
        if D.text == date:
            D.click()

    Months = driver.find_elements(By.XPATH,"//select[@id='month']/option")
    logging.info("Number of Months: " + colorama.Fore.BLUE + f" {len(Months)}")

    driver.find_element(By.XPATH,"//select[@id='month']/option").click()

    for M in Months:
        if M.text == Month:
            M.click()

    Years = driver.find_elements(By.XPATH,"//select[@id='year']/option")
    logging.info("Number of Years: " + colorama.Fore.BLUE + f" {len(Years)}")

    driver.find_element(By.XPATH,"//select[@id='year']/option").click()

    for Y in Years:
        if Y.text == year:
            Y.click()
    time.sleep(3)
    driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[2]/div/div/div[1]/form/div[1]/div[11]/button").click()
    logging.info("-----------------Verification-----------------")
    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h2"), "Enter the code from your email"))
    logging.info(colorama.Fore.BLUE + "Waiting for verification code...")
    verification = get_verification_code(email).split("-")[1].strip()
    if verification:
        logging.info("Verification code: " + colorama.Fore.BLUE + f" {verification}")
        driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div[2]/form/div[1]/div[1]/label/div/input").send_keys(verification)
        time.sleep(1)
        driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div[2]/form/div[2]/div/button").click()
        time.sleep(50)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div/div/div[3]/div/a')))
        driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/div/div/div[3]/div/a").click()
        time.sleep(15)
        logging.info(colorama.Fore.GREEN + "-------------------------Account created-------------------------")

    writen_to_file(email, "123456789@123")

def finish():
    driver.quit()
    time.sleep(5)
    start()
    
def get_verification_code(email):
    logging.info("Getting verification code...")
    for i in range(50):
        req = requests.get('https://snapmail.cc/emailList/' + email)
        if req.status_code == 200:
            email_text = json.loads(req.text)[0]['html']
            soup = bs4.BeautifulSoup(email_text, 'html.parser')
            match = re.findall(r'FB-\d+', soup.text)
            if match:
                code = match[0]
                logging.info("Verification code: " + colorama.Fore.BLUE + f" {code}")
                return code
        time.sleep(6)

if __name__ == "__main__":
    logging.info(colorama.Fore.GREEN + "Starting the script....")
    start()