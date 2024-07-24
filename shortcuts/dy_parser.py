from bs4 import BeautifulSoup, Tag
from tenacity import (
    AsyncRetrying, 
    RetryError, 
    stop_after_attempt, 
    retry_if_exception_type, 
    wait_exponential,
    retry
)
import httpx

from shortcuts.exceptions import ParsingError

DL_DOUYIN_URL = 'https://www.dlpanda.com/douyin'

def httpx_retries():
    return (
        retry_if_exception_type(httpx.ReadError) |
        retry_if_exception_type(httpx.ReadTimeout) |
        retry_if_exception_type(httpx.ConnectError) | 
        retry_if_exception_type(httpx.ConnectTimeout)
    )

def get_video_url_from_card_body_row(card: Tag):
    tags = card.find_all('video')
    return ['https:'+t.source['src'] for t in tags]

def get_photo_url_from_card_body_row(card: Tag) -> list[str]:
    tags = card.find_all('img')
    return [t['src'] for t in tags]

@retry(retry=httpx_retries(), wait=wait_exponential(multiplier=0.1), stop=stop_after_attempt(5), reraise=True)
def parse_url(url: str):
    if not len(url):
        raise ParsingError('Empty input', url)
    
    resp = httpx.get(
        'https://www.dlpanda.com/',
        params={
            'url': url,
            'token': 'G7eRpMaa'
        }
    )
    soup = BeautifulSoup(resp.text, 'lxml')
    card_body_row = soup.find(True, class_='card-body row')
    if not card_body_row:
        alert = soup.find(True, class_='alert alert-danger')
        if alert:
            raise ParsingError(alert.text, url)
        else:
            raise ParsingError(soup.title.text, url)

    videos = get_video_url_from_card_body_row(card_body_row)
    photos = get_photo_url_from_card_body_row(card_body_row)
    return videos + photos
    

if __name__ == '__main__':
    # 5.61 11/22 Jip:/ R@k.PK 我要的最简单，我要的也最难  https://v.douyin.com/ij5tWFcD/ 复制此链接，打开Dou音搜索，直接观看视频！
    # 
    r = parse_url('5.61 11/22 Jip:/ R@k.PK 我要的最简单，我要的也最难  https://v.douyin.com/ij5tWFcD/ 复制此链接，打开Dou音搜索，直接观看视频！')
    r = parse_url('7.92 01/12 b@n.dn UYM:/ # 自由的小脚丫 # 图图 # 无处安放的小脚丫  https://v.douyin.com/ij5gK3M9/ 复制此链接，打开Dou音搜索，直接观看视频！')
    print(r)
    print(r)