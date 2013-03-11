#!/usr/bin/python
import re

text_in = open("test_cases/images",'r').read()
text_out = text_in

#TRAC		[[Image(image_url)]]
#REDMINE	!image_url! 
#TRAC		[[Image(attached_image.png)]]	
#REDMINE	!attached_image.png!	
image_loc = re.compile('\[\[Image\(.{4,}\]\]\)')
images = image_loc.findall(text_out)
for image in images:
	loc = image[len("[[Image("):]
	text_out = text_out.replace(image, "!"+loc+"!")

#SPECIAL ATTRIBUTES
img_r = re.compile('\[\[Image\(.{4,}, [a-z\-]+=.+\]\]\)')
imgs = img_r.findall(text_out)
for img in imgs:
	#search only finds first occurence
	img_name = re.compile('[^, ]+').search(img[len("[[Image("):]).group()

	#slicing after "[[Image(name, ", +2 is for space and comma 
	prefix_num = len("[[Image(")+len(img_name) +2 

	#TRAC		[[Image(photo.jpg, align=right)]]
	#REDMINE	!>image_url! 
	if (img[prefix_num:len(img)-3] =="align=right" ):
		text_out = text_out.replace(img,"!>"+img_name+"!"
	#TRAC		[[Image(photo.jpg, alt='Image title')]]
	#REDMINE	!image_url(Image title)! displays an image with an alt/title attribute	
	elif ((img[prefix_num:prefix_num+4])=="alt="):
		alt_txt = img[ prefix_num+4 : len(img)-3]
		text_out = text_out.replace(img, "!"+img_name+"("+alt_txt+")!"

	#TRAC		[[Image(photo.jpg, 120px)]]               
	#REDMINE	!{width: 100%}attached_image.png!	
	elif (img[len(img)-5:len(img)-3]=="px"): 
		pixel_size = img[prefix_num:len(img)-5]
		text_out = text_out.replace(img, "!{width: "+pixel_size+"%}"+img_name+"!"
		
	elif (img[len(img)-4:len(img)-3]=="%"):
		pixel_size = img[prefix_num:len(img)-4]
		text_out = text_out.replace(img, "!{width: "+pixel_size+"px}"+img_name+"!"

	#TRAC		[[Image(photo.jpg, key=value)]]
	#REDMINE	!{key: value}attached_image.png!
	else: 	
		keypairs = re.compile('[A-Za-z]+=[^,]+').findall(img[prefix_num:])
		new_keypairs = []
		for keypair in keypairs:
			match = re.compile('[a-zA-Z]+=').search(keypair)
			hd = match.start()
			key = match.group()
			val = keypair[len(key):] #doing this in the middle also removes the '='
			key = key[:len(key)-1] #chop off '='
			new_keypair = key+": "+val
			new_keypairs.append(new_keypair)
		text_out = text_out.replace(img,"!{"+ ", ".join([str(x) for x in new_keypairs])+"}"+img_name+"!"


print text_out
