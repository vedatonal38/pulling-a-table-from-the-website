import requests as req
import argparse 
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

# English : Convert and save HTML tables to CSV or EXCEL Files in Python
# Türkçe : Python'da HTML tablolarını CSV veya EXCEL Dosyalarına Dönüştürüp kaydetme
# kurulum : pip install requests
#           pip install bs4
#           pip install pandas

class HTML_Tables:
    def __init__(self,url):
        self.USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        # US english
        self.LANGUAGE = "en-US,en;q=0.5"
        self.url = url


    def is_valid(self):
        """
        English:
            Checks whether `url` is a valid URL.
        Türkçe:
            "Url" nin geçerli bir URL olup olmadığını kontrol eder.
        """
        temp = urlparse(self.url)
        # temp.netloc -> example.com
        # temp.scheme -> https
        return bool(temp.netloc) and bool(temp.scheme)
        
    def get_soup(self):
        """
        English:
            Constructs and returns a soup using the HTML content of `url` passed
        Türkçe:
            Geçilen" url "nin HTML içeriğini kullanarak bir soup oluşturur ve döndürür
        """
        # initialize a session / bir oturumu başlat 
        session = req.Session()
        session.headers["User-Agent"] = self.USER_AGENT
        session.headers['Accept-Language'] = self.LANGUAGE
        session.headers['Content-Language'] = self.LANGUAGE
        # request / istek
        html = session.get(self.url)
        return bs(html.content, "html.parser")
    
    def get_all_tables(self, soup):
        """
        English:
            Extracts and returns all tables in a soup object
        Türkçe:
            Bir soup nesnesindeki tüm tablolari cikarir ve dondurur
        """
        return soup.find_all("table")
    
    def get_table_headers(self, table):
        """
        English:
            Given a table soup, returns all the headers.
            If the number of header cells and the number of 
            data cells are not equal, the number of header 
            cells increases.
        Türkçe:
            Tablo soup verildiğinde tüm başlıkları döndürür.
            Eğer başlık hücrelerin sayısı ile veri hücrelerin 
            sayısı birbirine eşit değilse başlık hücrelerin 
            sayısını artırıyor.
        """
        len_headers = len(table.find_all("tr")[0].find_all("th"))
        len_datas = len(table.find_all("tr")[1].find_all("th")) + len(table.find_all("tr")[1].find_all("td"))
        headers  = []
        if len_headers == len_datas:
            for th_tag in table.find("tr").find_all("th"): # <tr> tag satir <th> tag sutun
                headers.append(th_tag.text.strip())
        else:
            for th_tag in table.find("tr").find_all("th"): # <tr> tag satir <th> tag sutun
                headers.append(th_tag.text.strip())
            length = abs(len_datas - len_headers)
            for i in range(length):
                headers.append(" ")
        return headers
    
    def get_table_rows(self,table):
        """
        English:
            Given a table, returns all its rows.
        Türkçe:
            Bir tablo verildiğinde, tüm satırlarını döndürürür.
        """
        rows = []
        for tr_tag in table.find_all("tr")[1:]:
            cells = []
            td_tags = tr_tag.find_all("td")
            if len(td_tags) == 0:
                th_tags = tr_tag.find_all("th")
                for th_tag in th_tags:
                    cells.append(th_tag.text.strip())
            else:
                th_tags = tr_tag.find_all("th")
                if len(th_tags) != 0:
                    for th_tag in th_tags:
                        cells.append(th_tag.text.strip())
                for td_tag in td_tags:
                    cells.append(td_tag.text.strip())
            rows.append(cells)
        return rows

    def print_(self, table_name, headers, rows):
        """
        English:
            Print the table to the screen
        Türkçe:
            Tabloyu ekrana yazdırma
        """
        dataframe = pd.DataFrame(rows, columns=headers)
        dataframe.index +=1
        print(dataframe)
    
    def save_as_csv(self, table_name, headers, rows):
        """
        English:
            Saving the table in csv format
        Türkçe:
            Tabloyu csv formatta ile kaydetme
        """
        pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")
    
    def save_as_excel(self,table_name, headers, rows):
        """
        English:
            Saving the table in excel format
        Türkçe:
            Tabloyu excel formatta ile kaydetme
        """
        pd.DataFrame(rows, columns=headers).to_excel(f"{table_name}.xlsx")
    
    def main(self, _format):
        print(f"Web site: {self.url}")
        # get the soup / soup nesnesi al
        soup = self.get_soup()
        # extract all the tables from the web page / web sayfasından tüm tabloları çıkar
        tables = self.get_all_tables(soup)
        print(f"[+] Found a total of {len(tables)} tables.")
        # iterate over all tables / tüm tabloları yineleyin
        for i, table in enumerate(tables, start=1):
            # get the table headers / tablo başlıklarını al
            headers = self.get_table_headers(table)
            # get all the rows of the table / tablonun tüm satırlarını al
            rows = self.get_table_rows(table)
            table_name = f"table-{i}"
            print(f"[+] Saving {table_name}")
            # save table as csv or excel file / tabloyu csv veya excel dosyası olarak kaydet
            if _format.lower() == "csv" or _format.lower() == "c":
                self.save_as_csv(table_name, headers, rows)
            if _format.lower() == "excel" or _format.lower() == "e":
                self.save_as_excel(table_name, headers, rows)
            if _format.lower() == "print" or _format.lower() == "p":    
                self.print_(table_name, headers, rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url","-u",help="To enter a URL")
    parser.add_argument("--file","-f",help="Save from what file type (csv or excel)")
    parser.add_argument("-p", help="Print on screen")
    data = parser.parse_args()
    
    
    if data.url:
        table = HTML_Tables(data.url)
        if table.is_valid():
            if data.file:
                table.main(data.file)
            elif data.p:
                table.main(data.p)
        else:
            print("[!]Please enter a valid URL") # Lütfen geçerli bir adres girin
            print("[!]Example: https://example.com") # Örnek: https://example.com
    else:
        print("[!] You need to enter a URL.")