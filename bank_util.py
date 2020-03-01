import os
import time
import datetime
import calendar
import shutil
import pandas as pd
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# find current and parent path
def parent_path(path=__file__, f=0):
    return str('/'.join(os.path.abspath(path).split('/')[0:-1-f]))

current_path = os.path.dirname(os.path.abspath(__file__))
parent1_path = parent_path(current_path, f=0)
parent2_path = parent_path(current_path, f=1)

# global varialbe
WAIT_TIME_LONG = 5
WAIT_TIME_SHORT = 2
DATA_ROOT_DIR_PATH = parent2_path + '/cashflow_mng_root_dir/'
BANK_NAME_SMBC = 'smbc'


# =============================================================================
# common functions
# =============================================================================

def download_all_bank_statement(period):
    """
    download all bank statement (of all user and all bank) in specified period

    :param  period: int, period that we want to get bank statement data (past ~ now)
    :return None
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

                # make directories to save bank statement
                make_dir_to_save_bank_statement(user, bank, period)

                # download csv data
                download_user_bank_statement(user, bank, period)


def exists_bank_account(user, bank):
    """
    check if a user has bank account

    :param  user: str, user name 
    :param  bank: str, bank name
    :return     : bool, existence of bank account
    """
    path = DATA_ROOT_DIR_PATH + 'bank_user_data/' + bank + '/user_' + user + '/user_data.csv'
    return os.path.exists(path)


def make_dir_to_save_bank_statement(user, bank, period):
    """
    make directories to save bank statement
    if a directory has already existed, making directory is passed

    :param  user  : str, user name
    :param  bank  : str, user name
    :param  period: int, period that we want to get bank statement data (past ~ now)
    :return None
    """
    # get last month date
    target_date = datetime.datetime.today() - relativedelta(months=1)

    # make directories for specified period
    for i in range(period):
        # get year and month
        target_year = target_date.year
        target_month = target_date.month

        # make directory
        year_dir_path = (DATA_ROOT_DIR_PATH
                         + 'bank_statement/' + bank + '/user_' + user
                         + '/' + str(target_year))
        month_dir_path = (DATA_ROOT_DIR_PATH
                          + 'bank_statement/' + bank + '/user_' + user 
                          + '/' + str(target_year)
                          + '/' + str(target_month))
        if (not os.path.isdir(year_dir_path)):
            os.makedirs(year_dir_path)
            print('make   directory: ' + year_dir_path)
        else:
            print('exists directory: ' + year_dir_path)

        if (not os.path.isdir(month_dir_path)):
            os.makedirs(month_dir_path)
            print('make directory:   ' + month_dir_path)
        else:
            print('exists directory: ' + month_dir_path)

        # move to last month
        target_date -= relativedelta(months=1)


# TODO: implement
def delete_dir_to_save_bank_statement():
    pass

# NOTE: If you want to handle with new bank or revise each bank functions,
#       You shoule revise this function.
def download_user_bank_statement(user, bank, period):
    """
    download user's bank statement for bank
    API or HP are different depending on a bank,
    so download functions is prepared for each bank

    :param  user  : str, user name
    :param  bank  : str, bank name
    :param  period: int, period that we want to get bank statement data (past ~ now)
    :return None
    """
    # smbc: download user bank statement
    if (bank == BANK_NAME_SMBC):
        download_user_bank_statement_smbc(user, bank, period)

# NOTE: If you want to handle with new bank or revise each bank functions,
#       You shoule revise this function.
def exists_bank_statement(user, bank):
    """
    chech if bank statement exists or not
    
    :param  user: str, user name
    :param  bank: str, bank name
    :return     : bool, existence of bank statement
    """
    pass

def get_last_date(year, month):
    """
    get last date of specified year and month

    :param  year : year that you want to get last date
    :param  month: month that you want to get last date
    :return None :
    """
    return calendar.monthrange(year, month)[1]

# TODO: implement
def make_master_data(period):
    """
    make master data from each bank statement

    :param  period: int, period that we want to make master data (past ~ now)
    :return None
    """
    # TODO:
    # make directories to save master data
    make_dir_to_save_master_data(period)

    # get all user data
    user_filepath = DATA_ROOT_DIR_PATH + 'registration/user_list.csv'
    user_list = list(pd.read_csv(user_filepath, header=None).values)[0]

    # get all bank data
    bank_filepath = DATA_ROOT_DIR_PATH + 'registration/bank_list.csv'
    bank_list = list(pd.read_csv(bank_filepath, header=None).values)[0]

    # TODO:
    # loop for user and bank
    for user in user_list:
        for bank in bank_list:
            pass


def make_dir_to_save_master_data(period):
    """
    make directories to save master data
    master data is created every other years

    :param  period: int, period that we want to make master data (past ~ now)
    :return None
    """
    # get last month date
    period_past_date = datetime.datetime.today() - relativedelta(months=period)
    from_year = period_past_date.year
    last_month_date = datetime.datetime.today() - relativedelta(months=1)
    to_year = last_month_date.year

    for year in range(from_year, to_year+1):
        year_dir_path = (DATA_ROOT_DIR_PATH
                        + 'master_data/' + str(year) + '/')
        if (not os.path.isdir(year_dir_path)):
            os.makedirs(year_dir_path)
            print('make   directory: ' + year_dir_path)
        else:
            print('exists directory: ' + year_dir_path)


# =============================================================================
# smbc functions
# =============================================================================

def download_user_bank_statement_smbc(user, bank, period):
    """
    download smbc csv in specified priod
    1. login to bank HP and move to the page to download csv
    2. specify period to download csv
    3. download csv

    :param  user  : str, user name
    :param  bank  : str, bank name
    :param  period: int, target period for downloading
    :return None
    """
    # login to HP and move to a page to dowonload csv
    driver = move_to_page_to_download_csv_smbc(user, bank, period)

    # download csv for period
    target_date = datetime.datetime.today() - relativedelta(months=1)
    for i in range(period):
        # set year and month
        year = target_date.year
        month = target_date.month
        set_period_to_download_csv(driver, year, month)

        # download csv file of bank statement
        filename = 'bank_statement_raw.csv'
        filepath_to_save_csv = (DATA_ROOT_DIR_PATH
                                + 'bank_statement/' + bank + '/user_' + user + '/'
                                + str(year) + '/' 
                                + str(month) + '/'
                                + filename)
        if (not os.path.isfile(filepath_to_save_csv)):
            download_csv_simple_smbc(driver, filepath_to_save_csv)
            print('download: ' + filepath_to_save_csv)
        else:
            print('exist   : ' + filepath_to_save_csv)

        # move to last month
        target_date -= relativedelta(months=1)


def move_to_page_to_download_csv_smbc(user, bank, period):
    """
    move to a page to download csv of bank statement

    :param  user  : str, user name
    :param  bank  : str, bank name
    :param  period: int, target period for downloading
    :return webdriver
    """
    # get account information
    bank_account_filepath = DATA_ROOT_DIR_PATH + 'bank_user_data/' + bank + '/user_' + user + '/user_data.csv'
    bank_account_df = pd.read_csv(bank_account_filepath)
    branch_num = bank_account_df['branch_num'][0]
    account_num = bank_account_df['account_num'][0]
    password = bank_account_df['password'][0]

    # set bank url
    bank_url = 'https://direct.smbc.co.jp/aib/aibgsjsw5001.jsp'
    
    # open chrome with secret mode
    option = Options()
    option.add_argument('--incognito')
    driver = webdriver.Chrome(options=option)
    driver.get(bank_url)
    time.sleep(WAIT_TIME_LONG)

    # enter account information and login
    branch_box = driver.find_element_by_id('S_BRANCH_CD')
    branch_box.send_keys(str(branch_num))

    account_box = driver.find_element_by_id('S_ACCNT_NO')
    account_box.send_keys(str(account_num))

    password_box = driver.find_element_by_xpath('//*[@id="PASSWORD"]')
    password_box.send_keys(str(password).zfill(4))

    login_button = driver.find_element_by_xpath('//*[@id="login"]/input[7]')
    login_button.click()
    time.sleep(WAIT_TIME_LONG)

    # push next button
    next_button = driver.find_element_by_xpath('//*[@id="mainCont"]/div/div[3]/ul/li/input')
    next_button.click()
    time.sleep(WAIT_TIME_LONG)

    # go to page of account activity statement
    account_activity_statement_button = driver.find_element_by_xpath('//*[@id="cmn02main"]/div[2]/form/div/div/div[2]/div[2]/table/tbody/tr/td[2]/p[1]/a')
    account_activity_statement_button.click()
    time.sleep(WAIT_TIME_LONG)

    return driver


def set_period_to_download_csv(driver, year, month):
    """
    set period to download csv

    :param  driver: webdriver, webdriver of a smbc site
    :param  year  : int, year you want to set
    :param  month : int, month you want to set
    :return None
    """
    # set period of downloding target
    from_year_num = year
    from_month_num = month
    from_date_num = 1

    to_year_num = year
    to_month_num = month
    to_date_num = get_last_date(year, month)

    # set "from"
    from_year = driver.find_element_by_name('FromYear')
    from_year_select = Select(from_year)
    from_year_select.select_by_value(str(from_year_num))

    from_month = driver.find_element_by_name('FromMonth')
    from_month_select = Select(from_month)
    from_month_select.select_by_value('{0:02d}'.format(from_month_num))

    from_date = driver.find_element_by_name('FromDate')
    from_date_select = Select(from_date)
    from_date_select.select_by_value('{0:02d}'.format(from_date_num))

    # set "to"
    to_year = driver.find_element_by_name('ToYear')
    to_year_select = Select(to_year)
    to_year_select.select_by_value(str(to_year_num))

    to_month = driver.find_element_by_name('ToMonth')
    to_month_select = Select(to_month)
    to_month_select.select_by_value('{0:02d}'.format(to_month_num))

    to_date = driver.find_element_by_name('ToDate')
    to_date_select = Select(to_date)
    to_date_select.select_by_value('{0:02d}'.format(to_date_num))

    # click inquiry button
    inquiry_button = driver.find_element_by_name('web_kikan')
    inquiry_button.click()


def download_csv_simple_smbc(driver, filepath_to_save_csv):
    """
    download csv simply in the downloding page

    :param  driver              : webdriver, 
    :param  filepath_to_save_csv: str, destination to save csv
    :return None
    """
    # HACK: want to save csv file directory
    # download csv simply in csv downloading page
    csv_donwload_button = driver.find_element_by_id('DownloadCSV')
    csv_donwload_button.click()
    time.sleep(WAIT_TIME_LONG)

    # move csv file
    filepath_download_file = os.environ['HOME'] + '/Downloads/meisai.csv'
    dest_path = shutil.move(filepath_download_file, filepath_to_save_csv)


if __name__ == '__main__':
    # [unit: download bank statement]
    # (1) make directories to save bank statement
    # make_dir_to_save_bank_statement('user_name', 'bank_name', period)
    # (2) download csv data
    # download_user_bank_statement('user_name', 'bank_name', period)

    # [integration]
    # (1) download bank statement
    # download_all_bank_statement(24)
    
    # TODO:
    # (2) create master data
    make_master_data(24)