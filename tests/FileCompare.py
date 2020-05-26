# Compare a file, ignoring extra 0's added after a decimal point
def equal(file1, file2):
    # src: https://stackoverflow.com/questions/42512016/how-to-compare-two-files-as-part-of-unittest-while-getting-useful-output-in-cas
    file1 = open(file1)
    file2 = open(file2)

    # This function is written to ignore the extra zero's added behind a decimal point
    # Ahh yess, love the O(n^2)
    i = -1
    j = -1
    for line1 in file1:
        i += 1
        for line2 in file2:
            j += 1
            if i != j:
                continue
            if line1 == line2:
                continue
            if not "." in line1 and not "." in line2:  # zero check is only for decimals
                print("Found two lines that don't match:")
                print("Expected:", line1)
                print("Actual:", line2)
                return False
            ii = -1
            ji = -1
            # Find the char in the line from which they're not equal
            while ii < len(line1) - 1 and ji < len(line2) - 1:
                ii += 1
                ji += 1
                if line1[ii] == line2[ji]:
                    continue
                if line1[ii] == "0":
                    ji -= 1
                elif line2[ji] == "0":
                    ii -= 1
                else:
                    print("Found two lines that don't match:")
                    print("Expected:", line1)
                    print("Actual:", line2)
                    return False
        j = -1
    i = -1

    if i != j:
        return False

    file1.close()
    file2.close()

    return True
