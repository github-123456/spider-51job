from tutorial.spiders.SpiderPost import  SpiderPost
from scrapy.crawler import CrawlerProcess
from scrapy import *

process = CrawlerProcess({
    'USER_AGENT': 'bigyasuo/qq-1801041646'
})
csharp="https://search.51job.com/list/040000,000000,0000,00,9,99,c%2523,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
dotnet="https://search.51job.com/list/040000,000000,0000,00,9,99,.net,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
shanghai_csharp="https://search.51job.com/list/020000,000000,0000,00,9,99,c%2523,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
shanghai_dotnet="https://search.51job.com/list/020000,000000,0000,00,9,99,.net,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
# urls=[csharp,dotnet]
urls=[shanghai_csharp,shanghai_dotnet]
keys=['c#','.net']
process.crawl(SpiderPost,urls,10000,keys)
process.start() # the script will block here until the crawling is finished

