@x = global i32 0, align 4
@y = global i32* undef, align 8

define i32 @main() {
%N1N0T = add i32 1, 0
store i32 %N1N0T, i32* @x
store i32* @x, i32** @y
%N0N1N2T = add i32 2, 0
%t1 = load i32*, i32** @y
%N1N1N2T = load i32, i32* %t1
%N1N2T = mul i32 %N0N1N2T, %N1N1N2T
store i32 %N1N2T, i32* @x
ret i32 0
}

