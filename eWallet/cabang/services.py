import requests
import json
import math
from . import utils

def check_active_cabang():
	with open(utils.quorum_path_file) as f:
		data = json.load(f)
	success_count = 1
	fail_count = 0
	total_quorum = len(data) + 1
	for item in data:
		try:
			r = requests.post(item['ip'] + "ewallet/ping/", timeout=0.1) 
			response = r.json()['pingReturn']
		except:
			fail_count = fail_count + 1
			continue
		
		if int(response) == 1:
			success_count = success_count + 1

	if success_count < math.ceil(total_quorum/2):
		return -2
	elif success_count < total_quorum:
		return 1
	else:
		return 2

def request_saldo_to_all_cabang(user_id):
	with open(utils.quorum_path_file) as f:
		data = json.load(f)
			
	saldo = 0
	for item in data:
		r = requests.post(item['ip'] + "ewallet/getSaldo/", data = {'user_id': user_id})
		tempSaldo = r.json()['saldo']
		if tempSaldo > 0:
			saldo = saldo + tempSaldo
		elif tempSaldo < -1:
			return -3
		

	return saldo   

def request_get_total_saldo(user_id):
	with open(utils.quorum_path_file) as f:
		data = json.load(f)
	
	for item in data:
		if item['npm'] == user_id:
			try:
				r = requests.post(item['ip'] + "ewallet/getTotalSaldo/", data = {'user_id': user_id}, timeout=0.5)
				response = r.json()['saldo']
				return int(response)
			except:
				return -3
		# user id tidak ada dalam quorum.json
		return -99 

def transfer_saldo(user_id, ip, nilai):
	try:
		r = requests.post(ip + "ewallet/transfer/", data = {'user_id': user_id, 'nilai': nilai}, timeout=0.5)
	except:
		return -2
	response = r.json()['transferReturn']
	return int(response)

def is_valid_user_id(user_id):
	with open(utils.quorum_path_file) as f:
		data = json.load(f)

	for item in data:
		if item['npm'] == user_id:
			return item['ip']

	return ''
	