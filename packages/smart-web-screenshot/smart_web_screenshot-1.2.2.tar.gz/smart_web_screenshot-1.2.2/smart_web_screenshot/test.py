from smart_screenshot import SmartWebScreenShot


screenshotter = SmartWebScreenShot()
screenshotter.setup_driver(headless=True)
screenshotter.take_screenshot("https://google.com")
screenshotter.close_driver()