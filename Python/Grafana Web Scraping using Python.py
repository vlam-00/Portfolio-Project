from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import tkinter as tk
from tkinter import ttk,messagebox
import math
import os
import time
import glob
import sys

def region_checkbox(field_values):
    selected = {}

    def on_ok():
        for region, vars_dict in check_vars.items():
            checked = [val for val, var in vars_dict.items() if var.get()]
            if checked:
                selected[region] = checked
        root.destroy()

    def on_cancel():
        
        root.destroy()
        sys.exit(0)
    root = tk.Tk()
    root.title("Select the desired zones")
    root.geometry("800x600")
    main_frame = ttk.Frame(root)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    regions = list(field_values.keys())
    half = math.ceil(len(regions)/2)
    columns = [regions[:half], regions[half:]]
   
    col_frames = []
    for col_idx in range(2):
        col = ttk.Frame(main_frame)
        col.grid(row=0, column=col_idx, padx=20, sticky="n")
        col_frames.append(col)

    

    check_vars = {}
    for col_idx, col_regions in enumerate(columns):
        for region in col_regions:
            frame = col_frames[col_idx]
            label = ttk.Label(frame, text=region, font=("Arial", 10, "bold"))
            label.pack(pady=(10, 0))
            check_vars[region] = {}
            for val in field_values[region]:
                var = tk.BooleanVar(value=True)
                chk = ttk.Checkbutton(frame, text=val, variable=var)
                chk.pack(anchor="w", padx=10)
                check_vars[region][val] = var
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(3, weight=1)
    
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)

    ok_btn = ttk.Button(btn_frame, text="OK", command=on_ok)
    ok_btn.pack(side="left", padx=10)
    cancel_btn = ttk.Button(btn_frame, text="Cancel", command=on_cancel)
    cancel_btn.pack(side="left", padx=10)

    root.mainloop()
    return selected

user = os.environ.get("USERNAME")

print(f"User: {user}")

download_dir = fr"C:\Users\{user}\Box\IBM Cloud Capacity\Reports\- Weekly Reports\Grafana - VPC Power Reports\Grafana - Power Files"


print(f'caminho: {download_dir}')

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.dir", download_dir)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/csv")
fp.set_preference("pdfjs.disabled", True)

options = Options()
options.profile = fp

field_values = {
    "obs-metrics-ca-tor": ["mzone2q7", "mzone2r7", "mzone2s7"],
    "obs-metrics-au-syd":["mzone2h7","mzone2i7","mzone2j7"],
    "obs-metrics-br-sao" : ["mzone2t7","mzone2u7","mzone2v7"],
    "obs-metrics-eu-de" : ["mzone2b7","mzone2c7","mzone2d7"],
    "obs-metrics-eu-es": ["mzone2w7","mzone2x7","mzone2y7"],
    "obs-metrics-eu-gb": ["mzone787","mzone797","mzone7a7"],
    "obs-metrics-jp-osa": ["mzone2n7","mzone2o7","mzone2p7"],
    "obs-metrics-jp-tok": ["mzone2e7","mzone2f7","mzone2g7"],
    "obs-metrics-us-east": ["mzone757","mzone767","mzone777"],
    "obs-metrics-us-south" : ["mzone717","mzone727","mzone737","mzone747"]

    }

field_values = region_checkbox(field_values)

driver = webdriver.Firefox(options=options)




actions = ActionChains(driver)

# Page
driver.get("https://opsdashboard.w3.cloud.ibm.com/graphs/d/fleetman-power-capacity/power-capacity?orgId=1&from=now-5m&to=now&timezone=browser&var-Region=obs-metrics-br-sao&var-mzone=mzone2t7&var-Metric_Owner=sao1-qz1-sr2-rk045&var-Metric_Model=Lenovo%20SR650-V3::GPU%20count%3D2,%20GPU%20type%3DNVIDIA%20L40S-PCIe-48GB%2048::CPU%20count%3D2,%20CPU%20type%3DXeon-Sapphire-Rapids%208474C-PLATINUM-48Cores%2F96T%202.1G&refresh=2h") 

# wait for login
wait = WebDriverWait(driver, 60)

# Fill the first combobox (react-select-2-input)
time.sleep(45)




for field1_val, field2_list in field_values.items():
    for field2_val in field2_list:
        driver.refresh()
        time.sleep(2)
        field1 = wait.until(EC.visibility_of_element_located((By.ID, "react-select-2-input")))
        field1.send_keys(field1_val)
        field1.send_keys(Keys.ENTER)

# Second combobox
        field2 = wait.until(EC.visibility_of_element_located((By.ID, "react-select-3-input")))
        field2.send_keys(field2_val)
        field2.send_keys(Keys.ENTER)
        time.sleep(2)
# Third combobox
        

        field3 = wait.until(EC.visibility_of_element_located((By.ID, "react-select-4-input")))
        field3.send_keys(".*")
        field3.send_keys(Keys.ENTER)
        time.sleep(0.5)
# Fourth combobox
        field4 = wait.until(EC.visibility_of_element_located((By.ID, "react-select-5-input")))
        field4 = driver.find_element(By.ID, "react-select-5-input")
        field4.send_keys(".*")  
        field4.send_keys(Keys.ENTER)
# wait
        time.sleep(0.5)


        field5 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'button[data-testid="data-testid dashboard-row-title-Power: PDU (filtered by Metric Owner)"]')))

        collapse_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="data-testid dashboard-row-title-Power: PDU (filtered by Metric Owner)"]')))
        collapse_button.click()
# act on hover for panel
        time.sleep(2)
        header_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="header-container"]')))
        ActionChains(driver).move_to_element(header_div).perform()
        time.sleep(1)
        menu_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="data-testid Panel menu PDU Phases"]')))
        menu_button.click()
        time.sleep(1)
        inspect_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="data-testid Panel menu item Inspect"]')))
        inspect_option.click()
        time.sleep(1)
# click on data

        data_option = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Data']")))
        ActionChains(driver).move_to_element(data_option).click().perform()

        time.sleep(1)

        # wait the collapse of button
        expand_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-controls="Data options"]')))
        expand_button.click()

        time.sleep(0.8)
# wait the ID and fill
        input_transform = wait.until(EC.visibility_of_element_located(
            (By.ID, "react-select-6-input")
        ))
        input_transform.send_keys("Series Joined by Time")
        time.sleep(1)
        input_transform.send_keys(Keys.ENTER)



        time.sleep(0.4)
# wait  "Download CSV" and click
        download_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[text()='Download CSV'] and @aria-disabled='false']")
            )
        )
        download_button.click()


        time.sleep(0.4)

        
# rename csv
        timeout = 30
        filename_pattern = os.path.join(download_dir, "*.csv")
        start_time = time.time()
        csv_file = None

        while time.time() - start_time < timeout:
            files = glob.glob(filename_pattern)
            if files:
                csv_file = max(files, key=os.path.getctime)
                if not csv_file.endswith(".part"):
                    break
            time.sleep(1)

        prefix_dict = {
            "mzone2q7": "TOR01",
            "mzone2r7": "TOR04",
            "mzone2s7": "TOR05",
            "mzone2h7": "SYD01",
            "mzone2i7": "SYD04",
            "mzone2j7": "SYD05",
            "mzone2t7": "SAO01",
            "mzone2u7": "SAO04",
            "mzone2v7": "SAO05",
            "mzone2b7": "FRA02",
            "mzone2c7": "FRA04",
            "mzone2d7": "FRA05",
            "mzone2w7": "MAD02",
            "mzone2x7": "MAD04",
            "mzone2y7": "MAD05",
            "mzone787": "LON04",
            "mzone797": "LON05",
            "mzone7a7": "LON06",
            "mzone2n7": "OSA21",
            "mzone2o7": "OSA22",
            "mzone2p7": "OSA23",
            "mzone2e7": "TOK02",
            "mzone2f7": "TOK04",
            "mzone2g7": "TOK05",
            "mzone757": "WDC04",
            "mzone767": "WDC06",
            "mzone777": "WDC07",
            "mzone717": "DAL10",
            "mzone727": "DAL12",
            "mzone737": "DAL13",
            "mzone747": "DAL14"
            }

        if csv_file:
            original_name = os.path.basename(csv_file)
            prefix = prefix_dict.get(field2_val)
            new_name = f"{prefix} - {field2_val} - {original_name}"
            new_filename = os.path.join(download_dir, new_name)

            os.rename(csv_file, new_filename)
            print(f"CSV renamed to: {new_filename}")
        else:
            print("CSV not found!")

        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="data-testid Drawer close"]')))
        close_button.click()

        # quit 
driver.quit()







