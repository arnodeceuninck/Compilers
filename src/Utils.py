printString = 'call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str{}, i32 0, i32 0), {} {}{})\n'


# TODO make meaning of retval clear
def handle_return(retVal, output, formatTypes):
    output += retVal[0]
    for formatType in retVal[1]:
        formatTypes.add(formatType)
    return output


def get_LLVM_load():
    return "{}{} = load {}, {}* {}{}\n"
