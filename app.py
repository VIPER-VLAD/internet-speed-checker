import lib.speed_tester as speed_tester
from lib.router import Router
from lib.google_sheet import GoogleSheet
import datetime
import os.path
import json

config_file = 'config.json'

if not os.path.isfile(config_file):
	raise Exception('Config file is not exists')

try:
	config = json.load(open('config.json'))
except Exception as e:
	print(e)
	exit(0)

if not config or not config['google_sheet'] or not config['router']:
	raise Exception('Config file is invalid')

now = datetime.datetime.now()
router = Router(config['router']['url'], config['router']['login'], config['router']['password'])
hosts_count = router.get_lan_hosts_count()

speed_test_result = speed_tester.get_result()

client = (f"{speed_test_result['client']['isp']} \n"
          f"{speed_test_result['client']['ip']} \n{speed_test_result['client']['country']}"
          )

server = (f"{speed_test_result['server']['sponsor']} \n{speed_test_result['server']['host']}\n"
          f"{speed_test_result['server']['name']} \n{speed_test_result['server']['country']}"
          )

google_sheet = GoogleSheet(
	config['google_sheet']['sheet_id'],
	config['google_sheet']['page']
)
google_sheet.append([[
	now.strftime("%d.%m.%Y"),
	now.strftime("%H:%M"),
	hosts_count,
	speed_test_result['download'],
	speed_test_result['upload'],
	speed_test_result['ping'],
	client,
	server
]])
