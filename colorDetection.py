import cv2
import pandas as pd

img_path = r'testImage.jpg'
img = cv2.imread(img_path)

#global variables
clicked = False     #a flag to check if the pictured is clicked
r = 0
g = 0
b = 0
x_pos = 0
y_pos = 0

#read csv and name the columns
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# func to get the x,y axis coordination of the mouse double click

def draw(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global r, g, b, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')            # name of the window that pops up
cv2.setMouseCallback('image',draw)  # call draw

while True:

    cv2.imshow("image", img)

    if clicked:

        # cv2.rectangle(img, start, end, color, thickness, -1 to fill the whole rect)
        cv2.rectangle(img, (20,20), (750, 60), (b, g, r), -1)

        # text string to represent color name and rgb values
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,end,font,fontScale,color,thickness,lineType)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors display the text in black so its visible
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
