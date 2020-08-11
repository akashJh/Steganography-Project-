#Image Steganography Project
#Open an Image and Look at the Pixels in Hex
#A Delimmeter of 15-1 and 0 at the end to specify End of the Message helps in Retrieving
#Functions
#rgb2Hex
#hex2Rgb
#str2Bin
#bin2Str
from PIL import Image
import binascii
import optparse
#Helper Functions
def rgb2Hex(r,g,b):
	return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def hex2Rgb(hexcode):
	return 	tuple(map(ord,hexcode[1:].decode('hex')))

def str2Bin(message):
	binary=bin(int(binascii.hexlify(message.encode()),16))
	return binary[:2]

def bin2Str(binary):
	message=binascii.unhexlify('%x' % (int('0b'+binary,2)))
	return message

#Four Operation Functions 
def encode(hexcode,digit):
	if hexcode[-1] in ('0','1','2','3','4','5'):
		hexcode=hexcode[:-1]+digit
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
		print("Image Data:")
		print(datas)
		newData=[]
		digit=0
		for item in datas:
			if(digit<len(binary)):
				newPix=encode(rgb2Hex(item[0],item[1],item[2]),binary[digit])
				if(newPix==None):
					newData.append(item)
				else:
					newData.append(newPix)
			else:
				newData.append(item)
		#newData=tuple(newData)
		print("New Data Made \n",newData)
		img.putdata(newData)
		img.save(filename,"PNG")
		return "Data Hidden"
	else:
		print("Image Mode:{}".format(img.mode))
	return "Incorrect Image Type Given"

def retrive(filename):
	img=Image.open(filename)
	binary=''
	if img.mode in ('RGBA'):
		img=img.convert('RGBA')
		datas=img.getdata()

		for item in datas:
			digit=decode(rgb2Hex(item[0],item[1],item[2]))
			if(digit==None):
				pass
			else:
				binary=binary+digit
				if(binary[:-16]=='1111111111111110'):
					print("Message Found: ")
					return bin2Str(binary[:-16])
		#At the End check if the Binary has Delimetter in the Last or not
		return bin2Str(binary)
	return "Incorrect Image Format!!"

def main():
	parser=optparse.OptionParser("Usage %prog"+'-e/-d <target file>')
	parser.add_option("-e",dest='hide',type='string',help="target Picture Path to hide text")
	parser.add_option("-d",dest='retrive',type='string',help="target Picture Path to retrive") 
	(options,args)=parser.parse_args()
	if( options.hide!=None):
		text=input("Enter the message to hide->")
		print(hide(options.hide,text))
	elif( options.retrive!=None):
		print(retrive(options.retrive))
	else:
		print(parser.usage)
		exit(0)

main()