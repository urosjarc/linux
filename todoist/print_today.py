# Use the todoist API to get tasks from the current day

import json
import todoist
from datetime import datetime

# Log user in; switch to OAuth eventually...
api = todoist.TodoistAPI()

email = 'jar.fmf@gmail.com'
password = ''  # raw_input('Password: ')


def tree(rootTasks, allTasks, level=0):
	rootTasks = sorted(sorted(rootTasks, key=lambda task: task['day_order']), key=lambda task: task['all_day'])
	level += 1
	for i, rootT in enumerate(rootTasks):
		print(' - '*(level-1) + rootT['content'])
		childs = []
		for task in allTasks:
			if rootT['id'] == task['parent_id']:
				childs.append(task)

		rootT['children'] = tree(sorted(childs, key=lambda task: task['item_order']), allTasks,level)
		for child in rootT['children']:
			print(' - '*level + child['content'])
	return rootTasks

def get_todays_tasks():
	"""
	Get tasks due on the current utc day
	:return: list of task dicts
	"""
	# user = api.user.login(email, password)
	api.user.login(email, password)
	tasks_today = []
	tasks_other = []

	# Sync (load) data
	response = api.sync()

	# Get "today", only keep Day XX Mon, which Todoist uses
	today = datetime.utcnow()

	# Get root items
	for item in response['items']:
		if item['due_date_utc'] is not None:
			itemDate = datetime.strptime(item['due_date_utc'], '%a %d %b %Y %X +0000')
			if itemDate.date() == today.date():
				tasks_today.append(item)
				continue

	return sorted(tasks_today, key=lambda task: task['due_date_utc']), response['items']


if __name__ == '__main__':
	tasks, allTasks = get_todays_tasks()
	with open('response.json', 'w') as file:
		json.dump(tree(tasks, allTasks), file, indent=4)
