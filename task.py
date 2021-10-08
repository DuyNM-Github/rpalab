# +
from RPA.Browser.Selenium import Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from RPA.FileSystem import FileSystem

browser = Selenium()
fs = FileSystem()
url = "https://itdashboard.gov"


def minimal_task():
    browser.open_available_browser(url)
    browser.click_link("#home-dive-in")
    listOfAgencies = browser.find_elements('//*[@id="agency-tiles-widget"]/div/div/div/div/div/div/div/a/span')
    writeToExcelFile(listOfAgencies)
    print(f'//*[contains(text(), \"{agencyToSelect}\")]')
    agncElements = browser.find_elements(f'//*[contains(text(), \"{agencyToSelect}\" )]')
    browser.click_element_when_visible(agncElements[1])
    test = browser.find_elements("investments-table-object")


def writeToExcelFile(data):
    fs.create_file('output/workbook', content=None, encoding='utf-8', overwrite=True)
    fs.append_to_file('output/workbook', "Agency,Investment\n", encoding='utf-8')

    for i in range(0, len(data), 2):
        agencyName = browser.get_text(data[i])
        agencyInvestment = browser.get_text(data[i+1])
        text = agencyName + "," + agencyInvestment + "\n"
        fs.append_to_file('output/workbook', text, encoding='utf-8')
    print("Workbook handled")


def convertToCSV():
    if fs.does_file_exist('output/workbook.csv'):
        fs.remove_file('output/workbook.csv')
        fs.change_file_extension('output/workbook', '.csv')
    else:
        fs.change_file_extension('output/workbook', '.csv')


def readConfigurationFile():
    file = open('test_config', 'r')
    Lines = file.readlines()

    for line in Lines:
        if 'agency_to_be_selected' in line:
            global agencyToSelect
            agencyToSelect = format(line.split("=")[1]).strip()


if __name__ == "__main__":
    try:
        readConfigurationFile()
        minimal_task()
    except Exception as e:
        print("Error occurred: " + str(e))
    finally:
        print("Task Ended")
# -


