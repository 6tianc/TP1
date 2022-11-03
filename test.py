a = [
    [0,1,2,3,4,5,6,7,8,9,10],
    [0,1,2,3,4,5,6,7,8,9,10],
    [0,1,2,3,4,5,6,7,8,9,10],
    [0,1,2,3,4,5,6,7,8,9,10],
    [0,1,2,3,4,5,6,7,8,9,10],
]

screen = '#000#000#000#000\n#000#000#f81#000\n#000#000#000#000'
rows = screen.split('\n')
n=len(rows)
image=[]
for i in range(n):
    image.append(rows[i].strip('#').split("#"))
xLength = len(image)
ylength = len(image[0])
for xVal in range(xLength):
    for yVal in range(ylength):
        image[xVal][yVal] = '#'+ image[xVal][yVal]
print(image)