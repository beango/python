# encoding: UTF-8
import re
import urllib,re,sys,os,urllib2,cookielib
import Cookie
reload(sys)
sys.setdefaultencoding('utf-8')


def downgpx(gpxid):
	url = 'https://www.runtastic.com/zh/users/ding-huang-1/sport-sessions/'+gpxid+'.gpx'
	print url
	# second time do url request, the cookiejar will auto handle the cookie
	req = urllib2.Request(url); # urllib2.Request: the HTTP request will be a POST instead of a GET when the data parameter is provided.
	req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36");
	req.add_header('Content-Type', 'application/x-www-form-urlencoded');
	req.add_header('Cache-Control', 'no-cache');
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8');
	req.add_header('Connection', 'Keep-Alive');
	req.add_header('Cookie', 'split=%7B%22navigation_100%22%3A%22new%22%7D; remember_user_token=BAhbB1sGaQRuv9YBSSIZT1J4Z05HV0w4Z0ZVOXlQZ0dZeVUGOgZFRg%3D%3D--fdec972d6c3d2b92fd5361933f57491a883c00eb; _gat=1; __utmt=1; _runtastic_session=BAh7C0kiD3Nlc3Npb25faWQGOgZFVEkiJTU4MmY1NjU5OTY1MGFhNjhkYjZjMDcyZDczOWQ0MGI1BjsAVEkiE3VzZXJfcmV0dXJuX3RvBjsAVCIrL3poL3VzZXJzL2RpbmctaHVhbmctMS9zcG9ydC1zZXNzaW9ucz9JIhBfY3NyZl90b2tlbgY7AEZJIjFPT1ZkTTg5b0lRUWlzakJmYzVFUTZJV1FCM1plc3FvVVpIOGgrTEhBN1pJPQY7AEZJIhl3YXJkZW4udXNlci51c2VyLmtleQY7AFRbCEkiCVVzZXIGOwBGWwZpBG6%2F1gFJIhlNd0VTTzhUQjY5dXZTREVPeXNIcgY7AFRJIhB0YWJsZXRfdmlldwY7AEZGSSIQbW9iaWxlX3ZpZXcGOwBGRg%3D%3D--f0e81f3aa807be6d2c19272bc6b04cf4aca68440; _ga=GA1.2.86753239.1433744580; __utma=1.86753239.1433744580.1433744590.1433744590.1; __utmb=1.30.9.1433746936635; __utmc=1; __utmz=1.1433744590.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _mkra_ctxt=beb0f0d9c46ad6196661d84a747af410--200; locale=zh');
	resp = urllib2.urlopen(req);
	nam = resp.info()["Content-Disposition"].split('"')[1].encode("gb2312");
	
	savepath = "gpxs/"+gpxid+'.gpx';
	print resp.info()["Content-Disposition"].split('"')[1];
	with open(savepath, "wb") as code:
	    code.write(resp.read())
	    resp.close()
	    code.close()

if __name__ == "__main__":
	if (os.path.exists('gpxs')== False):
	    os.mkdir('gpxs')

	file_object = open('gpx.txt')

	list_of_all_the_lines = file_object.readlines()
	for line in list_of_all_the_lines:
		for item in line.split('['):
			gpxid = item.split(',')[0]
			if len(gpxid)==9:
				downgpx(gpxid)
	