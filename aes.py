import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import misc 
from scipy import fftpack
import base64
import os
import random
import sys
import math
import matplotlib.pylab as pylab
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import string
import npcr as fn1
import uaci as fn2
import correlation_coeff as fn3

pylab.rcParams['figure.figsize'] = (20.0, 7.0)

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
def dct2(a):
    return fftpack.dct( fftpack.dct( a, axis=0, norm='ortho' ), axis=1, norm='ortho' )
def idct2(a):
    return fftpack.idct( fftpack.idct( a, axis=0 , norm='ortho'), axis=1 , norm='ortho')

#reading of image
img= misc.imread("lena_gray.jpg")
im = rgb2gray(img) 
imsize = im.shape
#print (imsize)
plt.imshow(im,cmap='gray')
plt.title( "Original image")
plt.show()
#print(im)
dct = np.zeros(imsize)

# dct of image
for i in np.r_[:imsize[0]:8]:
    for j in np.r_[:imsize[1]:8]:
        dct[i:(i+8),j:(j+8)] = dct2( im[i:(i+8),j:(j+8)] )

dct = dct.astype(np.uint8)
print(dct)
pos = 128
# block of image
plt.imshow(im[pos:pos+8,pos:pos+8],cmap='gray')
plt.title( "An 8x8 Image block")
plt.show()
# dct of that block
plt.imshow(dct[pos:pos+8,pos:pos+8],cmap='gray',vmax= np.max(dct)*0.01,vmin = 0)
plt.title( "An 8x8 DCT block")
plt.show()
plt.imshow(dct,cmap='gray',vmax = np.max(dct)*0.01,vmin = 0)
plt.title( "8x8 cmplt DCTs of the image")
plt.show()
#print (np.max(dct))
thresh = 0.012
dct_thresh = dct * (abs(dct) > (thresh*np.max(dct)))
plt.imshow(dct_thresh,cmap='gray',vmax = np.max(dct)*0.01,vmin = 0)
plt.title( "Thresholded 8x8 DCTs of the image")
plt.show()
im_dct = np.zeros(imsize)
for i in np.r_[:imsize[0]:8]:
    for j in np.r_[:imsize[1]:8]:
        im_dct[i:(i+8),j:(j+8)] = idct2( dct[i:(i+8),j:(j+8)] )
"""plt.imshow( np.hstack((im, im_dct) ),cmap='gray')
plt.title("Comparision between original and DCT compressed images" )
plt.show()"""
print(fn1.npcr(im,dct))
print(fn2.uaci(im,dct))
print(fn3.corr(im))
print(fn3.corr(dct))

#implementation of arnold map
n=imsize[1]
for i in range(0,256):
    for x in range(0, imsize[0]):
            for y in range(0, imsize[1]):

                dct[x][y] = dct[(x+y)%n][(x+2*y)%n]
                
plt.imshow(dct,cmap='gray')
plt.title( "arnold")
plt.show()

print(fn1.npcr(im,dct))
print(fn2.uaci(im,dct))
print(fn3.corr(im))
print(fn3.corr(dct))

#implementation of aes

fin_key=""
for y in range(0,4):
      txt= ''.join([random.choice(string.ascii_letters) for n in range(16)])
      key=os.urandom(16)
      cipher = AES.new(key, AES.MODE_ECB)
      enc =cipher.encrypt(txt)
      data=base64.b64encode(enc).decode('utf-8')
      fin_key=fin_key+data

k=0
w,h=8,8
mat=[[0 for x in range (w)]for y in range (h)]
for i in range(0, 8):
    for j in range(0, 8):
        mat[i][j]=ord(fin_key[k])
        k=k+1
print(mat)

x=0
y=0
n=imsize[0]
for a in range (0,64):
    for b in range(0,64):
        for i in range(0,8):
            for j in range(0,8):
              #print(x+i)
              #print(y+j)
              dct[i][j]=int(dct[x+i][y+j])^int(mat[i][j])
        x=x+8
    x=0
    y=y+8

print(dct)
plt.imshow(dct,cmap='gray')
plt.title( "aes")
plt.show()
print(fn1.npcr(im,dct))
print(fn2.uaci(im,dct))
print(fn3.corr(im))
print(fn3.corr(dct))

     



      
      
      



