from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


# Copying from Watch Later
copyToPlaylist = 'Watch Later - Old'

# Google Log in Credentials
myUserNameOrEmail = 'YourEmail@gmail.com'
myPassword = 'YourPassword'

# We sign-in using Stack-overflow, because google forbids other approaches. 
# Idea from https://medium.com/@hostapandey/google-login-with-selenium-solved-f58873af5de9 

driver = webdriver.Chrome()
driver.get("https://stackoverflow.com/users/login")

findGoogle = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@data-provider, "google")]')))
findGoogle.click()

print("Google sign-in started")

findEmail = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//input[contains(@type, "email")]')))
time.sleep(2)
findEmail.send_keys(myUserNameOrEmail)
time.sleep(1)
findEmail.send_keys(Keys.ENTER)

print("Email Entered")

findPassword = WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, '//input[contains(@type, "password")]')))
time.sleep(2)
findPassword.send_keys(myPassword)
time.sleep(1)
findPassword.send_keys(Keys.ENTER)

print("Password Entered")


time.sleep(8)

driver.get("https://www.youtube.com/playlist?list=WL")

while True:
	searchingWatchLater = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//h1[contains(@id, "title")]')))
	if searchingWatchLater.text == 'Watch later':
		break

print("Found - Watch Later Playlist")
time.sleep(5)

count = 0

while True:
	checks = driver.find_elements_by_xpath('//ytd-playlist-video-renderer')

	# Title of the top video
	possibleTitle = checks[0].text
	print("")
	try:
		if possibleTitle != '[Private video]' and possibleTitle != '[Deleted video]':
			print("Found Video : " + str(possibleTitle.split('\n')[1]))
		else:
			print("This is a " + str(possibleTitle))
	except:
		None

	if len(checks) == 0:
		break

	stats = driver.find_element_by_xpath('//span[contains(@dir, "auto")]')
	print("Currently at " + str(stats.text) + " videos remaining in Watch Later.")
	count = count + 1


	sortThing = WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@id, "sort-filter-menu")]')))
	time.sleep(0.05)
	sortThing.click()
	time.sleep(0.1)
	sortThing.click()

	
	actions = ActionChains(driver)
	actions.send_keys(Keys.TAB)
	actions.perform()
	time.sleep(0.05)
	actions.perform()
	time.sleep(0.05)
	actions.perform()

	if possibleTitle != '[Private video]' and possibleTitle != '[Deleted video]':
		time.sleep(0.05)
		actions.perform()

	actions = ActionChains(driver)
	time.sleep(0.05)
	actions.send_keys(Keys.ENTER)
	actions.perform()

	if possibleTitle != '[Private video]' and possibleTitle != '[Deleted video]':
		actions = ActionChains(driver)
		time.sleep(0.05)
		actions.send_keys(Keys.TAB)
		actions.perform()

	actions = ActionChains(driver)
	time.sleep(0.05)
	actions.send_keys(Keys.ENTER)
	actions.perform()

	if possibleTitle != '[Private video]' and possibleTitle != '[Deleted video]':
		playlistsAppear = WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.XPATH, '//ytd-playlist-add-to-option-renderer')))
		time.sleep(0.1)
		playlists = driver.find_elements_by_xpath('//ytd-playlist-add-to-option-renderer')

		for playlist in playlists:
			if playlist.text == 'Watch later':
				playlist.click()
				time.sleep(0.1)
			if playlist.text == copyToPlaylist:
				playlist.click()
				time.sleep(0.1)

		print(str(count) + " videos transferred so far.")

		actions = ActionChains(driver)
		time.sleep(0.05)
		actions.send_keys(Keys.ESCAPE)
		actions.perform()
		time.sleep(0.05)
		actions.perform()

	time.sleep(0.5)
	driver.refresh()

