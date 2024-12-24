from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps")

searchbox = driver.find_element_by_id("searchboxinput")
searchbox.send_keys("Clothes shops manchester")
searchbox_searchbutton = driver.find_element_by_id("searchbox-searchbutton")
searchbox_searchbutton.click()
