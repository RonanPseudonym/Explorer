import time, os, atexit

# settings
TERMINAL_WIDTH, TERMINAL_HEIGHT = os.get_terminal_size()

BAR_WIDTH = 10
BAR_EIGHTH_PIECES = (" ","▏","▎","▍","▌","▋","▊","▉")

# If a display call is less than this number of seconds after the last executed one, skip it
MIN_UPDATE_INTERVAL = 0.04


# Utility
def clamp(val, low, high):
  """ Given a value, constrains it to between low and high"""
  return min(high, max(low, val))

class LinearRegressionEstimate:
  """ Stores a series of (x, y) points and fits a line to them """

  def __init__(self):
    self.xs = []
    self.ys = []
    self.update()

  def addData(self, x, y):
    self.xs.append(x)
    self.ys.append(y)

  def update(self):
    n = len(self.xs)
    assert n == len(self.ys)

    if n <= 1:
      self.m = self.b = None
      return

    sumX = sum(self.xs)
    sumY = sum(self.ys)
    meanX = sumX / n
    meanY = sumY / n
    
    sumXSquared = sum(x * x for x in self.xs)
    sumXY = sum(x * y for x, y in zip(self.xs, self.ys))

    self.m = (sumXY - ((sumX * sumY) / n)) / (sumXSquared - ((sumX * sumX) / n))
    self.b = meanY - (self.m * meanX)

  def reset(self):
    self.xs.clear()
    self.ys.clear()
    self.update()

  def predictY(self, x):
    if self.m is None or self.b is None: return None
    return self.m * x + self.b

  def predictX(self, y):
    if self.m is None or self.b is None: return None
    return (y - self.b) / self.m




# ANSI escape code helpers
def clearScreen():
  """ Prints several ANSI escape codes that clear the screen and the history """
  print("\033[2J\033[3J\033[H")

def colorize(text, fg, bg=None):
  """ Pads text with ANSI escape codes such that, when printed, will have the desired colors for the foreground and background"""
  start, end = "", ""

  def addCode(code, argument):
    nonlocal start, end
    start += f"\033[{code};5;{argument}m"
    end   += f"\033[{code+1}m"

  addCode(38, fg)
  if bg: addCode(48, bg)

  return start + text + end

def hideCursor():
  """ After calling this function, the cursor will be hidden """
  print("\033[?25l")

def showCursor():
  """ After calling this function, the cursor will be visible """
  print("\033[?25h")


# Main
lr = LinearRegressionEstimate()

def reset():
  global startTime, lastUpdate
  startTime = time.time()
  lastUpdate = startTime

def display(amt, description="", barColorFG=160, barColorBG=239):
  global lastUpdate
  now = time.time()

  # Calculation
  amt = clamp(amt, 0, 1)

  if amt != 1 and now - lastUpdate < MIN_UPDATE_INTERVAL:
    return

  elapsedTime = now - startTime

  lr.addData(elapsedTime, amt)
  lr.update()

  lastUpdate = now


  # Drawing
  clearScreen()

  # Draw progress bar
  length = amt * BAR_WIDTH
  filled = int(length)
  remainder = length - int(length)
  remainderPiece = "" if amt == 1 else BAR_EIGHTH_PIECES[int(remainder * 8)]

  bar = (
    "█" * filled +
    remainderPiece + 
    " " * (BAR_WIDTH - filled - 1)
  )

  lines = [
    "\n" * (TERMINAL_HEIGHT // 2 - 3),
    description.center(TERMINAL_WIDTH),
    ""
  ]

  percent = int(amt * 100)
  lines.append(
    " " * ((TERMINAL_WIDTH - 5 - BAR_WIDTH) // 2) + # Leftpad
    f"{percent:3}% {colorize(bar, barColorFG, barColorBG)}" # Percent and bar
  )

  predictedLength = lr.predictX(1)
  timeRemaining = "xxx.x" if predictedLength is None else f"{max(0, predictedLength - elapsedTime):5.1f}"
  lines.append(f"{timeRemaining} seconds remaining  ".center(TERMINAL_WIDTH))

  print("\n".join(lines))

reset()

# Keeps the cursor visible if there is an exception
atexit.register(showCursor)
