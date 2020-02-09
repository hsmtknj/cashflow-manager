import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# find curretn and parent path
def parent_path(path=__file__, f=0):
    return str('/'.join(os.path.abspath(path).split('/')[0:-1-f]))

current_path = os.path.dirname(os.path.abspath(__file__))
parent1_path = parent_path(current_path, f=0)
parent2_path = parent_path(current_path, f=1)

# global varialbe
WAIT_TIME_LONG = 5
WAIT_TIME_SHORT = 2
DATA_ROOT_DIR_PATH = parent2_path + '/cashflow_mng_root_dir/'


# =============================================================================
# common
# =============================================================================

def download_all_bank_statement(period):
    """
    download all bank statement (of all user and all bank) in specified period

    :param  period: int, period that we want to get bank statement data from now
    :return none
    """
    # get all user data
    user_filepath = DATA_ROOT_DIR_PATH + 'registration/user_list.csv'
    user_list = list(pd.read_csv(user_filepath, header=None).values)[0]

    # get all bank data
    bank_filepath = DATA_ROOT_DIR_PATH + 'registration/bank_list.csv'
    bank_list = list(pd.read_csv(bank_filepath, header=None).values)[0]

    # loop for user and bank
    for user in user_list:
        for bank in bank_list:
            # check if user data exists in the bank
            if (exists_bank_account(user, bank)):
                # download csv data


def exists_bank_account(user, bank):
    """
    check if a user has bank account

    :param  user: str, user name 
    :param  bank: str, bank name
    :return none: bool, existence of bank account
    """
    path = DATA_ROOT_DIR_PATH + 'bank_user_data/' + bank + '/user_' + user + '/user_data.csv'
    return os.path.exists(path)


# =============================================================================
# smbc
# =============================================================================

def donwload_user_bank_statement_smbc(user, period):
    """
    download smbc csv in specified priod
    1. login to bank HP and move to the page to download csv
    2. specify period to download csv
    3. download csv

    :param  user  : str, user name
    :param  period: int, target period for downloading
    """
    pass

def download_csv_simple_smbc():
    pass

def csv_download_smbc():
    # =========================================================================
    # load account infromation
    # =========================================================================

    # load csv file and get information
    file_path = parent2_path + '/data/bank_account/smbc.csv'
    account_df = pd.read_csv(file_path)

    branch_num = account_df['branch_num'][0]
    account_num = account_df['account_num'][0]
    password = account_df['password'][0]


    # =========================================================================
    # download csv file
    # =========================================================================

    # -------------------------------------------------------------------------
    # login
    # -------------------------------------------------------------------------

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
    time.sleep(WAIT_TIME_LONG)


    # -------------------------------------------------------------------------
    # after login
    # -------------------------------------------------------------------------

    # push next button
    next_button = driver.find_element_by_xpath('//*[@id="mainCont"]/div/div[3]/ul/li/input')
    next_button.click()
    time.sleep(WAIT_TIME_LONG)

    # go to page of account activity statement
    account_activity_statement_button = driver.find_element_by_xpath('//*[@id="cmn02main"]/div[2]/form/div/div/div[2]/div[2]/table/tbody/tr/td[2]/p[1]/a')
    account_activity_statement_button.click()
    time.sleep(WAIT_TIME_LONG)

    # download csv file
    csv_donwload_button = driver.find_element_by_id('DownloadCSV')
    csv_donwload_button.click()
    time.sleep(WAIT_TIME_LONG)


if __name__ == '__main__':
    download_all_bank_statement(1)
