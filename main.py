import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

WAIT_TIME_LONG = 5
WAIT_TIME_SHORT = 2


# =============================================================================
# find current and parent path and load account infromation
# =============================================================================

# find path
def parent_path(path=__file__, f=0):
    return str('/'.join(os.path.abspath(path).split('/')[0:-1-f]))

current_path = os.path.dirname(os.path.abspath(__file__))
parent1_path = parent_path(current_path, f=0)
parent2_path = parent_path(current_path, f=1)

# load csv file and get information
file_path = parent2_path + '/data/bank_account/smbc.csv'
account_df = pd.read_csv(file_path)

branch_num = account_df['branch_num'][0]
account_num = account_df['account_num'][0]
password = account_df['password'][0]


# =============================================================================
# download csv file
# =============================================================================

# set smbc url
bank_url = 'https://direct.smbc.co.jp/aib/aibgsjsw5001.jsp'
save_file_path = './meisai.csv'

# open chrome with secret mode
option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(options=option)
driver.get(bank_url)
time.sleep(WAIT_TIME_LONG)

# enter account information
branch_box = driver.find_element_by_id('S_BRANCH_CD')
branch_box.send_keys(str(branch_num))

account_box = driver.find_element_by_id('S_ACCNT_NO')
account_box.send_keys(str(account_num))

password_box = driver.find_element_by_xpath('//*[@id="PASSWORD"]')
password_box.send_keys(str(password).zfill(4))

login_button = driver.find_element_by_xpath('//*[@id="login"]/input[7]')
login_button.click()
