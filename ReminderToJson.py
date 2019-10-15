import os
import glob
import sqlite3
import contextlib
import datetime
import sys
import json

"""
macOS Catalina Reminder data to json

How to run:
	python3 ReminderToJson.py
	tasks.json will be generated.


Analysis:
	sqlite3 sqlite_src_data/Data-2515E223-B8F9-4BFB-BD5E-C0258FFD639F.sqlite -line "select * from ZREMCDOBJECT" > dump.txt

Guess:
	Tasks and categories are records of ZREMCDOBJECT table

	Category:
		ZNAME1 ... category name (if not empty)
		ZREMINDERIDSMERGEABLEORDERING_V2_JSON is json represented children of ZREMCDOBJECT.ZCKIDENTIFIER 
		example:
			["38720FFD-05DC-4E67-9AA3-E349D326A387","F30DDAD0-7453-41F6-B3DC-0B0A845C5709",...]
	Task:
		ZTITLE1 ... title (if not empty)
		ZCKIDENTIFIER ... task id
"""

def execSQL(dbFilename, sql):
	with contextlib.closing(sqlite3.connect(dbFilename)) as f:
		c = f.cursor()
		rs = c.execute(sql)
		rs = [ list(r) for r in rs ]
		return rs

def getTasks(datadir):
	def d2s(v):
		if v is None:
			return ""
		d = datetime.datetime.fromtimestamp(v)
		return d.strftime("%Y/%m/%d %H:%M:%S")

	rs = []
	for filename in glob.glob(datadir+"/*.sqlite"):
		sql = """select ZCREATIONDATE, ZCOMPLETIONDATE, ZTITLE1, ZCKIDENTIFIER, ZNAME1, ZREMINDERIDSMERGEABLEORDERING_V2_JSON from ZREMCDOBJECT"""
		lrs = execSQL(filename, sql)
		rs += lrs
		print(len(lrs), "tasks extracted from file", filename)

	id2cat = {}
	for r in rs:
		d, ed, title, id, cname, children = r
		if children is not None:
			cs = json.loads(children)
#			print(cname, cs)
			for c in cs:
				assert c not in id2cat
				id2cat[c] = cname

	tasks = []
	dOffset = 946681200
	for r in rs:
		d, ed, title, id, cname, children = r
		if d and title and id:
			d += dOffset
			if ed:
				ed += dOffset
			task = {
				"created": d,
				"created_str": d2s(d),
				"finished": ed,
				"finished_str": d2s(ed),
				"title": title,
				"category": id2cat.get(id, ""),
			}
			tasks.append(task)
	tasks.sort(key=lambda e: e["created"])
	return tasks

if __name__=="__main__":
	argv = sys.argv[1:]+[""*100]
	datadir = argv[0]
	if len(datadir)==0:
		datadir = os.path.expanduser("~")+"/Library/Reminders/Container_v1/Stores"
	print("datadir", datadir)

	tasks = getTasks(datadir)

	with open("tasks.json", "w") as f:
		print(json.dumps(tasks, indent=4, ensure_ascii=False), file=f)
