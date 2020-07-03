import png, noise, random, os
directory = os.path.dirname(os.path.realpath(__file__))

colorWidth, colorHeight, colors, _ =  png.Reader(os.path.join(directory,"code.png")).asRGBA8()
colors = list(map(list,colors))

width, height, zoom = 100, 100, .2

#Off limits ==================
def getColor(x, y):
  return colors[y][4*x:4*x+3]
# ============================

def clamp(val, low, high):
  """ Given a value, constrains it to between low and high"""
  return min(high, max(low, val))

def returnTempImgData(exponent, mapHeight, xPos, yPos):

  temporaryImgData = []

  for y in range(yPos, height+yPos):
    row = []
    for x in range(xPos, width+xPos):
      #rawNoise = (noise.snoise2(x / (width/zoom), y / (width/zoom), 10) + 42) / 42 #When you have the meaning of life, the universe and everything on your side yo
      rawNoise = (noise.snoise2(x / (width/zoom), y / (height/zoom), 10) + 1) / 2
      rawNoise = 1 - (rawNoise ** exponent)
      row.append(rawNoise)
    temporaryImgData.append(row)

  # low = min(map(min, temporaryImgData))
  # high = max(map(max, temporaryImgData))

  # #Normalize!

  # for y in range(height):
  #   for x in range(width):
  #     temporaryImgData[y][x] = 1 - (((temporaryImgData[y][x] - low) / (high - low)) ** exponent) 
  
  for i in range(0, len(temporaryImgData)): 
    for j in range(0, len(temporaryImgData[i])):
      temporaryImgData[i][j] = clamp(int(temporaryImgData[i][j]*(mapHeight-1)),0,mapHeight-1)
  
  return temporaryImgData

# ==============================

def createTile(xPos, yPos):

  imgData = []

  elevationMap = returnTempImgData(3, colorHeight, xPos*width, yPos*height) 

  moistureMap = returnTempImgData(1, colorHeight, (xPos+255)*width, (yPos+255)*height)

  #cloudMap = returnTempImgData(1, colorHeight, xPos*width, yPos*height)

  for y in range(height):
    row = []
    imgData.append(row)

    for x in range(width):
      pixel = (getColor(moistureMap[y][x], elevationMap[y][x]))
      #for z in range(0, 3):
        #pixel[z] += int(cloudMap[y][x]/1.5)
        #pixel[z] = clamp(pixel[z],0,255)
      row.extend(pixel)
      
  # Save as a png image with the format RGB (no alpha) called perlinterrain.png
  png.from_array(imgData, "RGB").save(os.path.join(directory,("Tiles/"+str(xPos)+", "+str(yPos)+".png")))

if __name__ == "__main__":
  for x in range(-25, 25):
    for y in range(-25, 25):
      print(y, x)
      createTile(x, y)