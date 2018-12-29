def cubentropy(img):
    """calculate the entropy of an image"""
    histogram = img.histogram()
    histogram_length = sum(histogram)
 
    samples_probability = [float(h) / histogram_length for h in histogram]
 
    return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])
"""def entropy(pixel):
    val=0
    width,height=pixel.size
    for y in range(0,height):
        for x in range(0,width):
            val=int(pixel[x][y])*int(log(pixel[x][y])+val

   #return val"""
