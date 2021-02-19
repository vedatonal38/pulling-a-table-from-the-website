# Python'da HTML tablolarını CSV veya EXCEL Dosyalarına Dönüştürüp kaydetme

Bir URL'den mevcut HTML tabloları çekip csv veya excel dosyaları olarak cihazımıza kaydetmek. İsterseniz consolla yazdıra birisiniz.

## Gereksinimler: 
`$ pip install requests`<br>
`$ pip install bs4`<br>
`$ pip install pandas`<br>
<br>
## Kullanıyım:
- csv olarak kaydetmek
`$ attract_html_table.py -u https://example.com -f csv`<br><br>
- excel olarak kaydetmek
`$ attract_html_table.py -u https://example.com -f excel`<br><br>
- Ekrana yazdırma
`$ attract_html_table.py -u https://example.com -p print`<br><br>
