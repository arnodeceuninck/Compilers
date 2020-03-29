@x = global i32 0, align 4
@y = global i32 0, align 4
@z = global i32 0, align 4
@a = global i32 0, align 4

define i32 @main() {
%N1N0T = add i32 5, 0
store i32 %N1N0T, i32* @x
%N1N1T = add i32 63, 0
store i32 %N1N1T, i32* @y
%N1N2T = add i32 2, 0
store i32 %N1N2T, i32* @z
%N1N3T = add i32 2, 0
store i32 %N1N3T, i32* @a
ret i32 0
}

