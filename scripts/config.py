museum_configs = {
    "BTLS": {
        "urls": [
            {
                "url": "https://www.baotanglichsutphcm.com.vn/",
                "method": "beautifulsoup"  # Crawl bằng BeautifulSoup
            },
            {
                "url": "https://vinwonders.com/vi/wonderpedia/news/bao-tang-lich-su-thanh-pho-ho-chi-minh/",
                "method": "selenium"  # Crawl bằng Selenium vì có JS render
            }
        ],
        "selectors": {
            "gioi_thieu": "div.history-section",
            "kien_truc": "div.architecture",
            "hien_vat": "div.exhibits",
            "dich_vu": "div.visit-info",
            "ket_luan": "div.conclusion"
        }
    },
    "HCMC": {
        "urls": [
            {
                "url": "https://hcmc-museum.edu.vn/",
                "method": "beautifulsoup"
            }
        ],
        "selectors": {
            "gioi_thieu": "section.introduction",
            "kien_truc": "section.architecture",
            "hien_vat": "section.exhibits",
            "dich_vu": "section.services",
            "ket_luan": "section.conclusion"
        }
    }
}
