PREFIX = '/video/wimp'
WIMP_URL = 'http://www.wimp.com'
WIMP_ARCHIVE = 'http://www.wimp.com/archives/'


####################################################################################################
def Start():

    ObjectContainer.title1 = 'Wimp'
    HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler(PREFIX, "Wimp")
def MainMenu():

    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(DateBrowser, title="Newest Videos", url=WIMP_URL), title="Newest Videos", summary="Most recent videos uploaded on Wimp.com"))
    oc.add(DirectoryObject(key=Callback(Archive, title="Archives"), title="Archives", summary="Videos previously uploaded on Wimp.com"))
    oc.add(VideoClipObject(url=(WIMP_URL+'/random/'), title="Random Video", summary="Play a random Wimp.com video"))
    oc.add(SearchDirectoryObject(identifier="com.plexapp.plugins.wimp", title=L("Search Wimp Videos"), prompt=L("Search for Videos")))

    return oc

####################################################################################################
@route(PREFIX + '/datebrowser')
def DateBrowser(title, url, year=''):

    oc = ObjectContainer(title2=title)
    data = HTML.ElementFromURL(url)
    
    date_list = []
    new_date_list = data.xpath('//span[@class="video_date"]//text()')
    # wanted to use set to take out repeated items, but then they are out of order. This maintains order
    for entry in new_date_list:
        if entry not in date_list:
            date_list.append(entry)

    for names in date_list:
        date_title = names
        # Here we check the main page to make sure it does not have two different years in it
        if url==WIMP_URL:
            year = Datetime.Now().year
            curr_month = Datetime.Now().month
            item_month = Datetime.ParseDate(names.split()[0]).month
            if item_month > curr_month:
                year = year-1
            year = str(year)
        date = '%s, %s' %(names, year)      
        #Log('the value of date is %s' %date)
        oc.add(DirectoryObject(key=Callback(Videos, title=date_title, url=url, date_list=date_list, date=date), title=date_title))

    for element in data.xpath('//a[contains(@href,"/archives/")]'):
        title = element.xpath('.//text()')[0].strip()
        url = element.xpath('.//@href')[0]
        if url==WIMP_ARCHIVE:
            title="Archives"
            oc.add(DirectoryObject(key=Callback(Archive, title="Archives", url=WIMP_URL+url), title="Archives"))
        else:
            oc.add(DirectoryObject(key=Callback(DateBrowser, title=title, url=WIMP_URL+url), title=title))

    return oc  

####################################################################################################
@route(PREFIX + '/archive')
def Archive(title):

    oc = ObjectContainer(title2=title)
    data = HTML.ElementFromURL(WIMP_ARCHIVE)

    for video in data.xpath('//div/p/a[@class="b"]'):
        title = video.xpath('.//text()')[0]
        year = title.split()[1]
        url = WIMP_URL + video.xpath('.//@href')[0]
        oc.add(DirectoryObject(key=Callback(DateBrowser, title=title, url=url, year=year), title=title))

    return oc  

####################################################################################################
@route(PREFIX + '/videos', date_list=list)
def Videos(title, url, date_list, date, title1="Videos"):

    oc = ObjectContainer(title1=title1, title2=title)
    data = HTML.ElementFromURL(url)
  
    vid_date = Datetime.ParseDate(date)
    for video in data.xpath('//span[@class="video_date" and text()="%s"]' % title):
        vid_title = video.xpath('./following-sibling::a//text()')[0].strip()
        vid_title = '%s - %s' %(title, vid_title)
        vid_url = video.xpath('./following-sibling::a//@href')[0]
        oc.add(VideoClipObject(url=WIMP_URL+vid_url, title=vid_title, originally_available_at=vid_date))
        
    return oc  
