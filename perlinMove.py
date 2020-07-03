# Imports
import random, time, math, pygame, os, perlinWrite

# Utility
screenWidth, screenHeight, zoom = 800, 600, 7
Vector = pygame.math.Vector2

camera = {
		"pos": Vector(),
		"vel": Vector()
}

tileSize = 100
scale = zoom*tileSize

# Initialize Pygame
pygame.display.init()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.DOUBLEBUF)

pygame.display.set_caption("Explorer")
clock = pygame.time.Clock()

cacheTiles = {}
cloudLocation = Vector() # Uppercase ✨

clouds = pygame.image.load("Dropbox/Code/Perlin/cloud.png").convert_alpha() #🌤😍
cloudWidth, cloudHeight = clouds.get_size()

def drawTile(xPos, yPos):
	key = (xPos, yPos)
	if key in cacheTiles:
		screen.blit(cacheTiles[key], Vector(xPos*scale,yPos*scale)-camera['pos'])
	else:
		filePath = "Dropbox/Code/Perlin/Tiles/"+str(int(xPos))+", "+str(int(yPos))+".png"
		if os.path.isfile(filePath):
			cacheTiles[key] = pygame.image.load(filePath).convert()
			cacheTiles[key] = pygame.transform.scale(cacheTiles[key],[zoom*cacheTiles[key].get_width(),zoom*cacheTiles[key].get_height()])
		else:
			perlinWrite.createTile(xPos, yPos)
			print(xPos, yPos)
		drawTile(xPos, yPos)


# Main loop


while True:

	# Handle keyboard input
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]: pygame.event.post(pygame.event.Event(pygame.QUIT))

	for event in pygame.event.get():
		if event.type == pygame.QUIT: exit()

	if keys[pygame.K_UP   ]: camera["vel"].y -= 1
	if keys[pygame.K_DOWN ]: camera["vel"].y += 1
	if keys[pygame.K_RIGHT]: camera["vel"].x += 1
	if keys[pygame.K_LEFT ]: camera["vel"].x -= 1

	# Update everything
	cloudLocation += Vector(1, 0.2)
	camera["pos"] += camera["vel"]
	camera["vel"] *= 0.97

	# Draw everything ====================================================================
	screen.fill(0)
	
	xPos, yPos = int(camera["pos"].x//scale), int(camera["pos"].y//scale)
	for x in range(0, screenWidth // scale+2):
		for y in range(0, screenHeight // scale+2):

			drawTile(xPos+x, yPos+y)

	cloudXPos = int((cloudLocation.x - camera["pos"].x/2) % cloudWidth)
	cloudYPos = int((cloudLocation.y - camera["pos"].y/2) % cloudHeight)
	for x in range(-2, 2):
		for y in range(-2, 2):
			screen.blit(clouds, ((cloudWidth * x) + cloudXPos, (cloudHeight * y) + cloudYPos))

	# ====================================================================================

	pygame.display.flip()
	clock.tick(60)