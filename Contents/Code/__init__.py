NAME = 'Wimp'
ART  = 'art-default.jpg'
ICON = 'icon-default.png'
WIMP_URL = 'http://wimp.com'

####################################################################################################
def Start():

    Plugin.AddPrefixHandler("/video/wimp", VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ObjectContainer.title1 = NAME
    ObjectContainer.view_group = "List"
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ICON)
    VideoClipObject.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
def VideoMainMenu():

    oc = ObjectContainer(view_group="InfoList")
    oc.add(DirectoryObject(key=Callback(NewestVideos, title="Newest Videos"), title="Newest Videos", summary="Most Recent Videos uploaded on Wimp.com"))
    oc.add(DirectoryObject(key=Callback(OlderVideos, title="Older Videos"), title="Older Videos", summary="Videos previously uploaded on Wimp.com"))
    oc.add(VideoClipObject(url=(WIMP_URL+'/random/'), title="Random Video", summary="Play a random Wimp.com video"))

    return oc

####################################################################################################
def NewestVideos(title):

    oc = ObjectContainer(title1=title, view_group="InfoList")
    data = HTML.ElementFromURL(WIMP_URL)

    for video in data.xpath('//span[@class="video_date"]'):
        theDate = Datetime.ParseDate(video.text)
        delta = Datetime.Now() - theDate
        if delta.days <= 1:
            title = video.xpath('./following-sibling::a')[0].text
            url = video.xpath('./following-sibling::a')[0].get('href')
            oc.add(VideoClipObject(url=(WIMP_URL + url), title=title, thumb=R(ICON)))
        else:
            pass

    return oc  

####################################################################################################
def OlderVideos(title):

    oc = ObjectContainer(title1=title, view_group="InfoList")
    data = HTML.ElementFromURL(WIMP_URL)

    for video in data.xpath('//span[@class="video_date"]'):
        theDate = Datetime.ParseDate(video.text)
        delta = Datetime.Now() - theDate
        if delta.days > 1:
            title = video.xpath('./following-sibling::a')[0].text
            url = video.xpath('./following-sibling::a')[0].get('href')
            oc.add(VideoClipObject(url=(WIMP_URL + url), title=title, thumb=R(ICON)))
        else:
            pass

    return oc
