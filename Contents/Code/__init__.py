NAME = 'Wimp'
ART  = 'art-default.jpg'
ICON = 'icon-default.png'
WIMP_URL = 'http://www.wimp.com'

####################################################################################################
def Start():

	Plugin.AddPrefixHandler("/video/wimp", VideoMainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

	ObjectContainer.title1 = NAME
	ObjectContainer.view_group = "InfoList"
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	VideoClipObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
def VideoMainMenu():

	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(NewestVideos, title="Newest Videos"), title="Newest Videos", summary="Most recent videos uploaded on Wimp.com"))
	oc.add(DirectoryObject(key=Callback(OlderVideos, title="Older Videos"), title="Older Videos", summary="Videos previously uploaded on Wimp.com"))
	oc.add(VideoClipObject(url=(WIMP_URL+'/random/'), title="Random Video", summary="Play a random Wimp.com video"))

	return oc

####################################################################################################
def NewestVideos(title):

	oc = ObjectContainer(title2=title)
	data = HTML.ElementFromURL(WIMP_URL)
	recent = data.xpath('//span[@class="video_date"]')[0].text

	for video in data.xpath('//span[@class="video_date" and text()="%s"]' % recent):
		title = video.xpath('./following-sibling::a')[0].text.strip()
		url = video.xpath('./following-sibling::a')[0].get('href')
		oc.add(VideoClipObject(url=WIMP_URL+url, title=title))

	return oc  

####################################################################################################
def OlderVideos(title):

	oc = ObjectContainer(title2=title)
	data = HTML.ElementFromURL(WIMP_URL)
	recent = data.xpath('//span[@class="video_date"]')[0].text

	for video in data.xpath('//span[@class="video_date" and text()!="%s"]' % recent):
		title = video.xpath('./following-sibling::a')[0].text.strip()
		url = video.xpath('./following-sibling::a')[0].get('href')
		oc.add(VideoClipObject(url=WIMP_URL+url, title=title))

	return oc  
