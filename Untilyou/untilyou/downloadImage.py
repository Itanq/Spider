
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re

# 自定义一个普遍下载器
# 用于下载爬取的公司logo图
# 貌似所有公司logo图都是png和jpg格式两种
# 所以这里只写png格式和jpg格式的logo图
class DownloadImage():
    def __init__(self):
        pass

    def downloadImage(self, URL, number):
        try:
            html = urlopen(URL)
        except(HTTPError,URLError) as e:
            return None
        else:
            bsObject = BeautifulSoup(html.read(),"lxml")
            imageLocation = bsObject.find("div", {"class":"jb_det_right_top"}).find("img")['src']
            imageKind = imageLocation[len(imageLocation)-3]
            #print("ImageKind: %s" % imageKind)
            #pattern = re.compile(r'.*?http://www\.(.*?)\.com/.*?\.(.*?).*?', re.S)
            #List = re.findall(pattern, imageLocation)
            #for data in List:
            #    imageKind = data[0].strip()
            #print("imageKind: %s" % imageKind)
            if imageKind == 'p':
                urlretrieve(imageLocation,'./Image/image%s.png' % number)
            else: 
                urlretrieve(imageLocation,'./Image/image%s.jpg' % number)

    def test(self):
        url = 'http://shixiseng.com/intern/inn_8fqm7lyn7nay'
        number = 0
        self.downloadImage(url, number)


#def main():
#    test = DownloadImage()
#    test.test()
#
#if __name__ == '__main__':
#    print("RUNING....")
#    main()
#    print("END!!!")
#
