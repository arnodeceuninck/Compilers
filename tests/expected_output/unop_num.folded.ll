@x = global i32 undef, align 4
@y = global i32 undef, align 4

define i32 @main() {
%N1N0T = add i32 1, 0
store i32 %N1N0T, i32* @x
%N1N1T = add i32 -1, 0
store i32 %N1N1T, i32* @y
ret i32 0
}

