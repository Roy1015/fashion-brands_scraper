def coach_scraper():
    #Coach JP
    #preparation
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import requests
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import time
    url = "https://japan.coach.com/shop/women/bags?page=12"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

    #product list
    productlinks = []
    list = []
    
    #use selenium and scroll down to the bottom, get all content first
    driver = webdriver.Chrome()
    driver.get(url)
    def scroll_to_bottom():
        actions = ActionChains(driver)actions.send_keys(Keys.END).perform()
    for _ in range(30):  # Adjust the number of scrolls as needed
        scroll_to_bottom()
        time.sleep(2) 
    soup = bs(driver.page_source, "html.parser")

    #get the links for each product
    productlist = soup.find_all("div",{"class":"product-thumbnail css-grdrdu"})
    for product in productlist:
        link = product.find('a').get('href')
        link='https://japan.coach.com/'+link
        productlinks.append(link)

    #for each product, get info
    for link in productlinks:
        f = requests.get(link,headers=headers).text
        hun=bs(f,'html.parser')

        try:
            sku=hun.find("h1",{"class":"chakra-heading pdp-product-title css-qpfb1e"}).text.replace('\n',"")
        except:
            sku = None

        try:
            price=hun.find("div",{"class":"pdp-active-price css-10g9bhb"}).text.replace('\n',"")
            price = price.replace('\t', '').replace('￥', '').replace(',', '').strip()
        except:
            price = None
    
        try:
            image = hun.find("img", {"class": "chakra-image css-119q2e7"})['src']
        except:
            image = None

        data={'sku':sku,'price':price,'image':image,'url':link}
        list.append(data)

    print(list)

    df = pd.DataFrame(list)
    df.to_clipboard()
