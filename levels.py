Levels = {
	1:{
		'sprites' : [
			{'type': 'rect', 'position': (0, "100%-50"), 'size': ('100%', 50), 'fills': ['white'] }, #position: (x,y), size: (width, height)
			{'type': 'goal', 'position': ("100%-75", "100%-250"), 'size': (50, 200), 'fills': ['grey', 'green'] }
		]
	},
	2:{
		'sprites' :[
			{'type': 'rect', 'position': (0, "100%-50"), 'size': ('50%-50', 50), 'fills': ['white'] },
			{'type': 'rect', 'position': ('50%+50', "100%-50"), 'size': ('50%-50', 50), 'fills': ['white'] },
			{'type': 'goal', 'position': ("100%-75", "100%-250"), 'size': (50, 200), 'fills': ['grey', 'green'] }
		]
	},
	3:{
		'sprites' :[
			{'type': 'rect', 'position': (0, "100%-50"), 'size': ('100%', 50), 'fills': ['white'] },
			{'type': 'spike', 'position': ('33.33%-20', "100%-90"), 'size': (40, 50), 'fills': ['black'] },
			{'type': 'spike', 'position': ('66.66%-20', "100%-90"), 'size': (40, 50), 'fills': ['black'] },
			{'type': 'goal', 'position': ("100%-75", "100%-250"), 'size': (50, 200), 'fills': ['grey', 'green'] }
		]
	},
	4:{
		'sprites' :[
			{'type': 'rect', 'position': (0, "100%-50"), 'size': ('50%-50', 50), 'fills': ['white'] },
			{'type': 'spike', 'position': ("50%-190", "100%-90"), 'size': (40,40), 'fills': ['black'], 'kill':True},
			{'type': 'rect', 'position': ('50%-150', "100%-100"), 'size': (100, 50), 'fills': ['white'] },
			{'type': 'rect', 'position': ('50%+50', "100%-100"), 'size': (100, 50), 'fills': ['white'] },
			{'type': 'spike', 'position': ("50%+150", "100%-90"), 'size': (40,40), 'fills': ['black'], 'kill':True},
			{'type': 'rect', 'position': ('50%+50', "100%-50"), 'size': ('50%-50', 100), 'fills': ['white'] },
			{'type': 'goal', 'position': ("100%-75", "100%-250"), 'size': (50, 200), 'fills': ['grey', 'green'] }
		]
	}
}