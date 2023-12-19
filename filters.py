import aiohttp
import json


async def fortiguard(domain):
  url = "https://www.fortiguard.com/learnmore/dns"
  headers = {
      'accept':
      '*/*',
      'accept-language':
      'en-US,en;q=0.9',
      'authority':
      'www.fortiguard.com',
      'content-type':
      'application/json;charset=UTF-8',
      'cookie':
      'cookiesession1=678A3E0F33B3CB9D7BEECD2B8A5DD036; privacy_agreement=true',
      'origin':
      'https://www.fortiguard.com',
      'referer':
      'https://www.fortiguard.com/services/sdns',
      'user-agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  }
  data = f'{{"value": "{domain}", "version": 9}}'

  async with aiohttp.ClientSession() as session:
    async with session.post(url, headers=headers, data=data) as response:
      result = await response.json()
      return result.get('dns', {}).get('categoryname', None)


async def lightspeed(hostname):
  url = "https://production-archive-proxy-api.lightspeedsystems.com/archiveproxy"
  headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-US,en;q=0.9',
      'authority': 'production-archive-proxy-api.lightspeedsystems.com',
      'content-type': 'application/json',
      'origin': 'https://archive.lightspeedsystems.com',
      'user-agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'x-api-key': 'onEkoztnFpTi3VG7XQEq6skQWN3aFm3h'
  }
  data = f'{{"query":"\\nquery getDeviceCategorization($itemA: CustomHostLookupInput!, $itemB: CustomHostLookupInput!){{\\n  a: custom_HostLookup(item: $itemA) {{ cat}}\\n  b: custom_HostLookup(item: $itemB) {{ cat   \\n  }}\\n}}","variables":{{"itemA":{{"hostname":"{hostname}"}}, "itemB":{{"hostname":"{hostname}"}}}}}}'

  async with aiohttp.ClientSession() as session:
    async with session.post(url, headers=headers, data=data) as response:
      result = await response.json()
      cat_a = result.get('data', {}).get('a', {}).get('cat', None)
      cat_b = result.get('data', {}).get('b', {}).get('cat', None)
      return [lscat(cat_a), lscat(cat_b)]


def lscat(num):
  with open("ls_cat.json", "r") as file:
    j = json.load(file)
    for entry in j:
      if entry["CategoryNumber"] == num:
        return entry["CategoryName"]
    return num


from bs4 import BeautifulSoup


async def pan(domain):
  url = f"https://urlfiltering.paloaltonetworks.com/single_cr/?url={domain}"
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      html = await response.text()

  soup = BeautifulSoup(html, 'html.parser')
  form_texts = soup.select('.form-text')

  if len(form_texts) > 2:
    return form_texts[2].get_text(strip=True)
  else:
    return None


async def safe_browsing(url):
  api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=API_KEY"
  payload = {
      'client': {
          'clientId': "your-client-id",
          'clientVersion': "1.0.0"
      },
      'threatInfo': {
          'threatTypes': [
              "MALWARE", "SOCIAL_ENGINEERING", "THREAT_TYPE_UNSPECIFIED",
              "UNWANTED_SOFTWARE"
          ],
          'platformTypes': ["ANY_PLATFORM"],
          'threatEntryTypes': ["URL"],
          'threatEntries': [{
              'url': url
          }]
      }
  }

  async with aiohttp.ClientSession() as session:
    async with session.post(api_url, json=payload) as response:
      if response.status == 200:
        threat_matches = (await response.json()).get('matches', [])
        return not bool(
            threat_matches
        )
      else:
        return True
