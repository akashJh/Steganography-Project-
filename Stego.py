#Image Steganography Project
#Open an Image and Look at the Pixels in Hex
#A Delimmeter of 15-1 and 0 at the end to specify End of the Message helps in Retrieving

from PIL import Image
import binascii

#Helper Functions
def rgb2Hex(r,g,b):
	return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def hex2Rgb(hexcode):
	hexcode=hexcode.lstrip('#')
	return tuple(int(hexcode[i:i+1],16) for i in (0,2,4))

def str2Bin(message):
	#binary=bin(int(binascii.hexlify(message.encode()),16))
	binary= ''.join(format(ord(i), 'b') for i in message) 
	return binary

def bin2Str(binary):
	message=binascii.unhexlify('%x' % (int('0b'+binary,2)))
	return message

#Four Operation Functions 
def encode(hexcode,digit):
	if hexcode[-1] in ('0','1','2','3','4','5'):
		print("Previous Hex Code->",hexcode)
		hexcode=hexcode[:-1]+digit
		print("After Changing Hexcode->",hexcode)
		return hexcode
	else:
		return None

def decode(hexcode):
	if hexcode[-1] in ('0','1'):
		return hexcode[-1]
	else:
		return None

def hide(filename,message):
	#Given the Filename and Message hide it in the given File
	img=Image.open(filename)
	binary=str2Bin(message)+'1111111111111110'
	#Hide the binary into the Image and End it with 15-1 and 0 as delimetter
	#Check if Image is Editable
	if img.mode in ('PRGBA'):
		img=img.convert('RGBA')
		datas=img.getdata()
		#Changing the whole data into Newdata
		newData=[]
		digit=0
		for item in datas:
			if(digit<len(binary)):
				newPix=encode(rgb2Hex(item[0],item[1],item[2]),binary[digit])
				if(newPix==None):
					newData.append(item)
				else:
					#if Hiding is Succesfull insert the new Pixel with Hidden Data
					r,g,b=hex2Rgb(newPix)
					newData.append((r,g,b))
			else:
				newData.append(item)
		img.putdata(newData)
		new_name="hidden"
		img.save(new_name,"PNG")
		return "Data Hidden"
	else:
		print("Image Mode:{}".format(img.mode))
	return "Incorrect Image Type Given"

def retrive(filename):
	img=Image.open(filename)
	binary=''
	if img.mode in ('PRGBA'):
		img=img.convert('RGBA')
		datas=img.getdata()

		for item in datas:
			digit=decode(rgb2Hex(item[0],item[1],item[2]))
			if(digit==None):
				pass
			else:
				binary=binary+digit
				#At the End check if the Binary has Delimetter in the Last or not
				if(binary[:-16]=='1111111111111110'):
					print("Message Found: ")
					return bin2Str(binary[:-16])
		print("Retrieved Binary is:",binary)
		return bin2Str(binary)[1:]
	return "Incorrect Image Format!!"

def main():
	pic=input("Enter the Image:")
	print("1.Encode\n2.Decode")
	opt=int(input("Choose [1/2] : "))
	if(opt==1):
		text=input("Enter the message to hide: ")
		print(hide(pic,text))
	elif(opt==2):
		print(retrive(pic))
	else:
		exit(0)

main()