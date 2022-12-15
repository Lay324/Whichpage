from selenium import webdriver
import time
import pymysql


# 模拟点击
def pointer(num):
    pointer_url = "https://link.springer.com/chapter/10.1007/978-3-030-01267-0_" + str(
        num)
    br.get(pointer_url)
    time.sleep(2)
    get_message(num)
    # ul = br.find_elements_by_class_name("publ-list")[1]
    # lis = ul.find_elements_by_xpath('li')
    # for i in range(len(lis)):


# 获取数据
def get_message(num):
    abstract = br.find_element_by_id('Par1').text
    if len(br.find_elements_by_xpath('//p[@class="Para"]')):
        abstract = br.find_elements_by_xpath('//p[@class="Para"]')[0].text
    else:
        return

    if len(
            br.find_elements_by_xpath(
                '//span[@class="article-dates__first-online"]/time')):
        date = br.find_elements_by_xpath(
            '//span[@class="article-dates__first-online"]/time')[0].text
        # date = date.split(r': ')[1]
    else:
        return
    # date = "11 September 2010"

    if len(
            br.find_elements_by_xpath(
                '//span[@class="RefSource"]'
            )):
        link = br.find_elements_by_xpath(
            '//span[@class="RefSource"]'
        )[0].text
        length = len(link.split(r'/'))
        isbn = link.split(r'/')[length - 1]
        if not len(isbn):
            return
    else:
        return

    if len(br.find_elements_by_xpath('//h1[@class="ChapterTitle"]')):
        title = br.find_elements_by_xpath(
            '//h1[@class="ChapterTitle"]')[0].text
    else:
        return

    key_list = br.find_elements_by_xpath('//div[@class="KeywordGroup"]/span')

    key_word = ""
    for k in key_list:
        key_word += k.text

    key_list = key_word.split(" ")

    if ('doi.org' in link) is False:
        return

    # print("\nabstract: " + abstract)
    # print("\ndate: " + date)
    # print("\nlink: " + link)
    # print("\ntitle: " + title)
    # print("\nisbn: " + isbn)
    # print("\nkey_word: " + key_word)
    save_data(isbn, key_word, title, link, date, abstract)
    save_tag(key_list)


def save_data(isbn, key_word, title, link, date, abstract):
    db = pymysql.connect(host='106.52.194.66',
                         user='root',
                         password='123456',
                         port=3306,
                         db='whichpage')
    con = db.cursor()

    # 将数据写入MySQL
    d = (isbn, title, key_word, date, link, abstract)
    sql = 'INSERT INTO page_list(isbn, title, tag, year, link, abstract) values(%s, %s, %s, %s, %s, %s)'
    try:
        con.execute(sql, d)
        db.commit()
        print("succeed to save page!")
    except Exception as ex:
        db.rollback()
        print("have something wrong, and %s" % ex)

    con.close()
    db.close()


# 将tag导入数据库
def save_tag(key_list):
    db = pymysql.connect(host='106.52.194.66',
                         user='root',
                         password='123456',
                         port=3306,
                         db='whichpage')
    con = db.cursor()

    belong = "ECCV"
    year = "2017"

    for k in key_list:
        key = (k, belong, year)
        sql = 'select * from tag_list where name = %s and belong = %s and year = %s'
        try:
            con.execute(sql, key)
            if con.fetchone() is not None:
                sql = 'update tag_list set num = num + 1 where name = %s and belong = %s and year = %s'
                con.execute(sql, key)
                db.commit()
                print("succeed to +1!")
            else:
                # 将数据写入MySQL
                d = (k, belong, year)
                sql = 'INSERT INTO tag_list(name, belong, year) values(%s, %s, %s)'
                try:
                    con.execute(sql, d)
                    db.commit()
                    print("succeed to save!")
                except Exception as ex:
                    db.rollback()
                    print("have something wrong, and %s" % ex)
        except Exception as ex:
            db.rollback()
            print("have something wrong, and %s" % ex)

    con.close()
    db.close()


# 主程序
if __name__ == '__main__':
    br = webdriver.Chrome()
    for i in range(1, 47):
        pointer(i)
