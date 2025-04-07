file1 = "file1.txt"
file2 = "file2.txt"

with open(file1 , "r") as source:
    lines = source.readlines()

#invert lines
lines = [line.rstrip("\n") + "\n" for line in lines[::-1]]
print(lines)

with open(file2, "w") as destination:
    for line in lines:
        destination.write(line)
