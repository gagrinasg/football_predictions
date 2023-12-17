import asyncio
import os

from pyppeteer import launch

async def screenshot_fixture(fixture_id):
    # Replace 'your-api-key' with your actual API key
    api_key = os.getenv('RAPID_API_KEY')

    # Launch a headless browser
    browser=await launch(options={'args': ['--no-sandbox']})

    # Create a new page
    page = await browser.newPage()

    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    widget_file_directory = os.path.join(current_script_directory,'widget_html', 'widget.html')

    # Read the content of the local HTML file
    with open(widget_file_directory, 'r') as file:
        widget_html = file.read()

    await asyncio.sleep(1)
    # Set the content of the page to the widget HTML
    await page.setContent(widget_html)

    # Execute JavaScript to set the API key for a specific element (replace 'your-element-id' with the actual ID)
    await page.evaluate(f'document.getElementById("wg-api-football-game").setAttribute("data-key", "{api_key}")')

    await page.evaluate(f'document.getElementById("wg-api-football-game").setAttribute("data-id", "{fixture_id}")')

    await page.evaluate('document.getElementById("wg-api-football-game").click()')

    # Wait for the script to take effect (you might need to adjust the wait time)
    await asyncio.sleep(2)

    image_path = f'screenshots\\{fixture_id}.png'

    joined_path = os.path.join(current_script_directory, image_path)
    screenshot_options = {'path': joined_path, 'clip': {'x': 0, 'y': 0, 'width': 800, 'height': 400}}  
    # Take a screenshot (optional)
    await page.screenshot(screenshot_options)

    await asyncio.sleep(2)
    # Close the browser
    await browser.close()

    return joined_path

# Run the event loop
# asyncio.get_event_loop().run_until_complete(screenshot_fixture(718243))