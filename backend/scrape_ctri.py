import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome driver
driver = webdriver.Chrome()
driver.get("https://ctri.nic.in/Clinicaltrials/pubview.php")
time.sleep(3)

# 1. Enter "cancer" in search box
search_box = driver.find_element(By.NAME, "searchword")
search_box.clear()
search_box.send_keys("cancer")

# 2. Select "Health Condition/Problem Studied" from dropdown
dropdown = Select(driver.find_element(By.NAME, "searchtype"))
dropdown.select_by_visible_text("Health Condition/ Problem Studied")

# 3. Enter CAPTCHA manually
input("Enter the CAPTCHA manually in the browser, then press Enter here...")

# 4. IMPROVED BUTTON SELECTOR - Try multiple strategies
search_button = None
button_selectors = [
    (By.CSS_SELECTOR, "input[type='image']"),
    (By.CSS_SELECTOR, "input[src*='go']"),
    (By.XPATH, "//input[@type='image']"),
    (By.XPATH, "//input[contains(@src, 'go')]"),
    (By.XPATH, "//input[@onclick='return searchForm()']")
]

for by, selector in button_selectors:
    try:
        search_button = driver.find_element(by, selector)
        print(f"Found button using {by}: {selector}")
        break
    except Exception:
        continue

if search_button:
    search_button.click()
else:
    print("ERROR: Could not find the search button.")
    print("Current page URL:", driver.current_url)
    print("First 500 chars of page source:", driver.page_source[:500])
    driver.quit()
    exit()

time.sleep(5)

# 5. Scrape trial data from the sortable table
trial_data = []

try:
    # Try to find the results table
    table_selectors = [
        "//table[contains(@class, 'sortable')]",
        "//table[@class='sortable']",
        "//table[contains(@id, 'results')]",
        "//table[@border='1']"
    ]
    
    trial_rows = []
    for selector in table_selectors:
        try:
            trial_rows = driver.find_elements(By.XPATH, f"{selector}//tr[position()>1]")
            if len(trial_rows) > 0:
                print(f"Found table with selector: {selector}")
                break
        except Exception:
            continue
    
    if len(trial_rows) == 0:
        trial_rows = driver.find_elements(By.XPATH, "//table//tr[position()>1]")
    
    for row in trial_rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 7:  # Minimum expected columns
            trial_info = {
                "CTRI_No": cols[0].text.strip() if len(cols) > 0 else "",
                "Public_Title": cols[1].text.strip() if len(cols) > 1 else "",
                "Type_of_Trial": cols[2].text.strip() if len(cols) > 2 else "",
                "Recruitment_Status": cols[3].text.strip() if len(cols) > 3 else "",
                "Health_Condition": cols[4].text.strip() if len(cols) > 4 else "",
                "Intervention_Name": cols[5].text.strip() if len(cols) > 5 else "",
                "Location": cols[6].text.strip() if len(cols) > 6 else "",
            }
            trial_data.append(trial_info)
            
except Exception as e:
    print(f"Error scraping table: {e}")
    # Try alternative approach - print all tables for debugging
    tables = driver.find_elements(By.TAG_NAME, "table")
    print(f"Found {len(tables)} tables on page")
    for i, table in enumerate(tables):
        print(f"Table {i} HTML snippet: {table.get_attribute('outerHTML')[:200]}...")

# 6. Save to CSV
if trial_data:
    filename = 'cancer_trials.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=trial_data[0].keys())
        writer.writeheader()
        writer.writerows(trial_data)
    print(f"Successfully scraped {len(trial_data)} trials. Saved to '{filename}'")
    
    # Print first few records as verification
    print("\nFirst 3 records:")
    for i, record in enumerate(trial_data[:3]):
        print(f"{i+1}. {record}")
else:
    print("No trials found. The table structure might be different than expected.")
    
    # Debug: save page source for inspection
    debug_filename = 'page_debug.html'
    with open(debug_filename, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print(f"Saved page source to '{debug_filename}' for manual inspection.")

# 7. Close browser
driver.quit()