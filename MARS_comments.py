# Since you can't see comments in MARS debuggers on a line that doesn't contain any instructions,
# this adds a useless instruction, so you can still see the comment inside the debugger

file = open("output/compiled.asm", "r")

output = ""
comment = "addi $s0, $s0, 0 "
for line in file:
    if len(line) >= 2 and line[0] == "\t" and line[1] == "#":
        line = comment + line
    output += line

file.close()
file = open("output/compiled_mars_comments.asm", "w+")
file.write(output)
file.close()
