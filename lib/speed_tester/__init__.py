import speedtest


def __result_format(result):
	return round(int(result) / 10 ** 6, 2)


def get_result():
	ins = speedtest.Speedtest()
	ins.download()
	ins.upload()

	client = ins.results.client
	server = ins.results.server

	return {
		'download': __result_format(ins.results.download),
		'upload': __result_format(ins.results.upload),
		'ping': int(ins.results.ping),
		'client': {
			'ip': client['ip'],
			'isp': client['isp'],
			'country': client['country']
		},
		'server': {
			'host': server['host'],
			'name': server['name'],
			'country': server['country'],
			'sponsor': server['sponsor']
		}
	}
