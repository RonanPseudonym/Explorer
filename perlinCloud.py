import png, noise, os, loading

loading.hideCursor()

directory = os.path.dirname(os.path.realpath(__file__))

                   # ============= 🌸🌸🌸 ============
                   # Code Documentation
                   # Creative Commons 2020
                   # Ronan Underwood
                   # Some rights reserved
                   
                   # ============= :D =============
airAmount  = 0.3   # 0: all clouds      1: all air 🌸
brightness = 0.7   # 0: transparent     1: max     🌷
                   # ============= :D =============
                   
                   # Some rights reserved
                   # Ronan Underwood
                   # Creative Commons 2020
                   # Code Documentation
                   # ============= 🌸🌸🌸 ============

"""
                   # ============= 🌸🌸🌸 ============
                   # Documentación del código
                   # Creative Commons 2020
                   # Ronan Underwood
                   # Algunos derechos reservados
                   
                   # ============= :D =============
airAmount =   ---  # 0: todas las nubes 1: todo el aire 🌸
brillo    =   ---  # 0: transparente    1: máximo       🌷
                   # ============= :D =============
                   
                   # Algunos derechos reservados
                   # Ronan Underwood
                   # Creative Commons 2020
                   # Documentación del código
                   # ============= 🌸🌸🌸 ============

"""

width, height, zoom = 5000, 5000, 5
def returnTempImgData(xPos, yPos):

  temporaryImgData = []
  loading.reset()

  for y in range(yPos, height+yPos):
    loading.display((y-yPos)/(height-1), description="Generating Cloudmap")
    row = []
    for x in range(xPos, width+xPos):
      rawNoise = (noise.snoise2(x / (width/zoom), y / (height/zoom), 10, repeatx=zoom, repeaty=zoom) + 1) / 2
      rawNoise = 1 - rawNoise
      row.append(rawNoise)
    temporaryImgData.append(row)
  
  return temporaryImgData

# ==============================


imgData = []

cloudMap = returnTempImgData(0, 0)

for y in range(height):
    row = []
    imgData.append(row)
    for x in range(width):
        row.append(255)
        row.append(max(int((cloudMap[y][x] - airAmount) * 255 * brightness/(1-airAmount)), 0)) # M A T H 
png.from_array(imgData, "LA").save(os.path.join(directory,"cloud.png"))




#Added for a line 42