from bs4 import BeautifulSoup
import requests, os
from tqdm import tqdm
import json
from random import randint
chastota = [0, 0, 0]

debug = False

number_of_pages = 7 # 7 actual value 

global_contens = {}

plants_links = []

categories = {"ampelnye-rasteniya" : "Ампельные растения",
			  "bonsaj" : "Бонсай",
			  "bromelievye" : "Бромелиевые", 
			  "dekorativno-listvennye" : "Декоративно-лиственные", 
			  "derevya-i-kustarniki" : "Деревья и Кустарники",
			  "kaktusy" : "Кактусы",
			  "lukovichnye" : "Луковичные",
			  "orxidei" : "Орхидеи",
			  "palmy" : "Пальмы",
			  "paporotniki" : "Папоротники",
			  "plodovyj-sad-v-kvartire" : "Плодовый сад в квартире",
			  "sukkulenty" : "Суккуленты",
			  "hishhnye" : "Хищные",
			  "cvetushhie": "Цветущие"
}

def download(url):
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(url.split("/")[-1])
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))

total = 0
#for category in categories.keys():
for category in tqdm(categories.keys(), total=len(categories)):
	cnt = 0
	print(categories[category], ':', sep='')
	category_content = {}
	for page in range(1, number_of_pages):
		response = requests.get(f"https://rastenievod.com/category/komnatnye-rasteniya/{category}/page/{page}")
		if response.status_code != 200:
			#print(f"BREAK ON PAGE:{page}")
			break

		site = response.text
		soup = BeautifulSoup(site, "html.parser")

		links = soup.find_all('a', rel="bookmark")

		cur = 0

		if debug:
			datarate = 1
		else:
			datarate = 22

		for a in links[:datarate]:
			cur += 1
			plants_links.append(a["href"])
			#print(cnt, ") ", a["href"], sep='')
		cnt += cur
		#print(f"\t\tcur: {cur}")
	total += cnt
	#print(categories[category], ':', sep='', end='')
	#print(f"\tcnt: {cnt}")

	for link in plants_links:
		response = requests.get(link)
		site = response.text
		soup = BeautifulSoup(site, "html.parser")
		name = soup.find_all(class_="entry-title")[0].text
		image_url = soup.find_all(class_="entry-thumb")[0].img['src']
		description = soup.p.text
		all_content = soup.find('main').find('article').find(class_="entry-content").find_all()

		# print('\t', name)

		count = 0
		eng_name = link.split('/')[-1].split('.')[0]
		plant_content = {"name": eng_name,"Описание": ''}
		cur_key = "Описание"
		for i in all_content:
			if i.name == 'p' and i.text == "Содержание":
				continue
			if i.name != 'p' and i.name != 'h2' and i.name != 'h3' and i.name != 'ul' and i.name != 'ol':
				continue
			if i.name == 'h2':
				if "с фото" in i.text:
					break
				cur_key = i.text
				plant_content[cur_key] = ''
			if i.name == 'p':
				if plant_content[cur_key] != '':
					plant_content[cur_key] += '\n' 
				plant_content[cur_key] += i.text
			if i.name == 'h3':
				if plant_content[cur_key] != '':
					plant_content[cur_key] += '\n' 
				plant_content[cur_key] += "\n<i>" + i.text + "</i>"
			if i.name == 'ul' or i.name == 'ol':
				if len(i.attrs) != 0:
					if 'class' in i.attrs.keys():
						if 'toc_list' in i.attrs['class']:
							continue
				a = i.li.find_all('a')
				if len(a) != 0:
					a = a[0].find_all('span')
					#print(a[0].attrs)
					if len(a) != 0:
						if 'class' in a[0].attrs.keys():
							if 'toc_number' in a[0].attrs['class']:
								continue
					count = 1;
				for j in i.find_all('li'):
					plant_content[cur_key] += f'\n\t{count}) {j.text}'
					count += 1

		#print(plant_content)
		plant_content['Частота полива'] = 6 + randint(-2, 3)
		
		for key in plant_content:
			if 'Уход' in key:
				if 'редко' in plant_content[key] or 'скудным' in plant_content[key] or 'редким' in plant_content[key] or 'редки' in plant_content[key]:
					plant_content['Частота полива'] = 10 + randint(-1, 1)
					chastota[0] += 1
				elif 'умеренный' in plant_content[key] or 'умеренно' in plant_content[key] or 'умере' in plant_content[key]:
					plant_content['Частота полива'] = 5 + randint(-1, 1)
					chastota[1] += 1
				elif 'регулярный' in plant_content[key] or 'регулярно' in plant_content[key] or 'обильно' in plant_content[key]:
					plant_content['Частота полива'] = 3 + randint(-1, 1)
					chastota[2] += 1

		category_content[name] = plant_content
	#print(category_content)
	global_contens[categories[category]] = category_content 
	plants_links.clear()

print(chastota[0], chastota[1], chastota[2], total, sep='\t')

with open(f"content.json", 'w') as json_file:
	#json_object = json.dumps(content, ensure_ascii=False)
	#json_file.write(json_object)
	#json.dump(content, json_file, ensure_ascii=False, indent=4)
	json.dump(global_contens, json_file)
	
		#print(plane_image_url)
	#download(plane_image_url)