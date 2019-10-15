# macOS_Catalina_ReminderToJSON
Reminders data in macOS Catalina to JSON file


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
