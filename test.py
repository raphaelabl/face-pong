import cv2

face_cascade = cv2.CascadeClassifier(r'/home/raphael/Dev/Python/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)

window_name = "image"

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


class Vec:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


ball = Vec(100, 100, 10, 10)
ball.x = 100
ball.y = 100
ball.dy = 10
ball.dx = -10

width = 640
height = 480

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_img, 1.25, 4)

    if len(faces) == 2:
        ball.x += ball.dx
        ball.y += ball.dy

        if ball.y > height - 5:
            ball.y = height - 5
            ball.dy *= -1

        if ball.y < 0:
            ball.y = 0
            ball.dy *= -1

        if ball.x > width - 5:
            ball.x = width - 5
            ball.dx *= -1

        if ball.x < 0:
            ball.x = 0
            ball.dx *= -1

    cv2.circle(img, (ball.x, ball.y), 5, (0, 0, 255), 1)

    faceCords = []

    for (x, y, w, h) in faces:
        faceCords.append(Vec(x, y, w, h))

    faceCords.sort(key=lambda c: c.x)

    for index, vec in enumerate(faceCords[0:2], start=0):
        cv2.rectangle(img, (100 + (index * 400), vec.y), (100 + (index * 400) + 30, vec.y + 100), (300, 300, 0), 1)

        if (100 + (index * 400)) < ball.x < (100 + (index * 400) + 30) and vec.y < ball.y < vec.y + vec.dy:
            ball.x = vec.x
            ball.dx *= -1

    cv2.imshow(window_name, img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
