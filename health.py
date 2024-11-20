from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_table_data(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    try:
        all_data = []
        
        while True:  
            try:
                
                district_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "s_district"))
                )
                select = Select(district_dropdown)
                districts = [option.get_attribute('value') for option in select.options if option.get_attribute('value')]
                break  
            except Exception as e:
                print(f"Retrying to get district list: {str(e)}")
                time.sleep(2)
        
        
        for district_value in districts:
            print(f"Scraping data for district: {district_value}")
            
            try:
                
                district_dropdown = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "s_district"))
                )
                select = Select(district_dropdown)
                select.select_by_value(district_value)
                
                
                time.sleep(3)
                
                
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[style*='width: 475px;overflow: scroll'] table"))
                )
                
                
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                for row in rows[1:]:  
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) >= 8:
                            row_data = {
                                'District': district_value,
                                'Serial_No': cells[0].text.strip(),
                                'PHC_Name': cells[1].text.strip(),
                                'Location': cells[2].text.strip(),
                                'Area': cells[3].text.strip(),
                                'Block': cells[4].text.strip(),
                                'Phone': cells[5].text.strip(),
                                'Code': cells[6].text.strip(),
                                'Email': cells[7].text.strip()
                            }
                            all_data.append(row_data)
                    except Exception as e:
                        print(f"Error processing row in district {district_value}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error scraping district {district_value}: {str(e)}")
                continue
        
        
        if all_data:
            df = pd.DataFrame(all_data)
            df.to_json('health_centers_data.json', orient='records', lines=True)  # Save as JSON
            print(f"Successfully scraped {len(all_data)} rows of data across all districts")
        else:
            print("No data was collected")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()


url = "https://www.wbhealth.gov.in/pages/search_hospitals"
scrape_table_data(url)
