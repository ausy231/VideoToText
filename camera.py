import cv2
from PIL import Image
import time


def getimage():
    result, img = cam.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    return image


def process(image, size):

    data = image.load()
    array = []
    characters = ['@', 'B', 'M', 'N', 'W', '#', '0', '8', 'D', 'K', 'Q', 'R', '&', '6', '9', 'A', 'E', 'G', 'H', 'O',
                  'b', 'd', 'g', 'p', 'q', '$', '%', '3', '4', '5', 'P', 'S', 'U', 'V', 'X', 'Z', 'a', 'e', 'h', 'k',
                  'm', 'w', '2', 'C', 'F', 'I', 'J', 'n', 'o', 'u', 'y', '*', '1', '7', 'L', 'T', 'Y', '[', ']', 'f',
                  'i', 'j', 's', 't', 'v', 'x', 'z', '{', '(', ')', '+', ':', '<', '=', '>', '?', '\\', 'c', 'l', 'r',
                  '!', '"', '^', '~', ',', '-', ';', '_', "'", '.', '`']
    averages = [0, 6, 14, 20, 20, 25, 31, 38, 40, 44, 47, 50, 51, 52, 55, 56, 56, 58, 69, 71, 71, 72, 72, 72, 74, 78,
                79, 80, 82, 83, 83, 84, 87, 91, 93, 95, 97, 97, 98, 98, 99, 99, 108, 109, 112, 115, 117, 121, 122, 124,
                124, 131, 132, 132, 133, 135, 135, 136, 137, 137, 145, 147, 147, 147, 148, 148, 148, 148, 155, 161, 161,
                163, 163, 169, 170, 172, 172, 173, 174, 174, 186, 190, 192, 196, 205, 207, 216, 220, 233, 236, 255]
    characters.reverse()
    y = 0
    x = 0
    while y < image.height:
        row = ""
        while x < image.width:
            average = (data[x, y][0] + data[x, y][1] + data[x, y][2]) / 3
            passed = False
            upper = len(characters)-1
            lower = 0
            index = int((len(characters)-1)/2)
            while not passed:
                if averages[index] <= average <= averages[index + 1]:
                    passed = True
                    row += characters[index]
                elif average < averages[index]:
                    upper = index
                    index = int((upper+lower)/2)
                elif average > averages[index]:
                    lower = index
                    index = int((upper+lower)/2)
                else:
                    row += " "
                    passed = True

            x += int(image.width / size)

        array.append(row)
        y += int(image.width / size / .6)
        x = 0
    f = open('text.txt', 'wb')
    for line in array:
        f.write((line + "\n").encode())
    f.close()


cam = cv2.VideoCapture(0)



duration = int(input("Duration: "))
size = int(input("Size in pixels (recommended 50 - 200): "))
start_time = time.perf_counter()
frame_count = 0
while time.perf_counter() - start_time < duration:
    img = getimage()
    process(getimage(), size)
    frame_count += 1

print(f"average frame rate: {frame_count//duration}fps")