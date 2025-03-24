import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import museum_configs

def get_html_using_beautifulsoup(url):
    """Crawl nội dung bằng BeautifulSoup."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi lấy dữ liệu từ {url}: {e}")
        return None

def get_html_using_selenium(url):
    """Crawl nội dung bằng Selenium."""
    try:
        service = Service(executable_path="chromedriver.exe")  # Đường dẫn ChromeDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Chạy không hiện trình duyệt
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(url)
        time.sleep(3)  # Đợi JavaScript load xong
        html = driver.page_source
        driver.quit()

        return BeautifulSoup(html, "html.parser")
    except Exception as e:
        print(f"❌ Lỗi khi render trang {url} bằng Selenium: {e}")
        return None

def crawl_museum(museum_name):
    """Crawl dữ liệu bảo tàng theo tên."""
    if museum_name not in museum_configs:
        print(f"❌ Bảo tàng {museum_name} không có trong danh sách!")
        return
    
    config = museum_configs[museum_name]
    data = {"name": museum_name, "sections": {}}

    for section, selector in config["selectors"].items():
        for url_config in config["urls"]:
            url = url_config["url"]
            method = url_config["method"]

            # Chọn phương thức crawl phù hợp
            if method == "beautifulsoup":
                soup = get_html_using_beautifulsoup(url)
            elif method == "selenium":
                soup = get_html_using_selenium(url)
            else:
                print(f"⚠️ Không có phương thức crawl phù hợp cho {url}")
                continue

            if not soup:
                continue

            content = soup.select_one(selector)
            if content:
                data["sections"][section] = content.get_text(strip=True)
                break  # Lấy nội dung từ trang đầu tiên có dữ liệu hợp lệ

    return data

# Crawl và lưu dữ liệu vào file JSON
for museum in ["history", "hcm_city"]:
    museum_data = crawl_museum(museum)
    if museum_data:
        with open(f"database/{museum}.json", "w", encoding="utf-8") as f:
            json.dump(museum_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Crawl thành công: {museum}.json")
