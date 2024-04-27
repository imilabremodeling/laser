import os 

t = 0
while True:
	file = os.listdir('.')
	for i in range(len(file)):
		if os.path.isfile(file[i]):
			if file[i]=='train.py':
				from train import inference
				inference()
				t=1
				break
	if t ==1:
		t = 0			
		break
