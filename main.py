import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import bank_util

if __name__ == '__main__':
    bank_util.csv_download_smbc()
