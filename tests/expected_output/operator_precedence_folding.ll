@x = global i32 undef, align 4
@y = global i32 undef, align 4
@z = global i32 undef, align 4
@a = global i32 undef, align 4
@b = global i32 undef, align 4

define i32 @main() {
%N0N0N0N1N0T = add i32 4, 0
%N1N0N0N1N0T = add i32 2, 0
%N0N0N1N0T = mul i32 %N0N0N0N1N0T, %N1N0N0N1N0T
%N1N0N1N0T = add i32 1, 0
%N0N1N0T = add i32 %N0N0N1N0T, %N1N0N1N0T
%N1N1N0T = add i32 3, 0
%N1N0T = sub i32 %N0N1N0T, %N1N1N0T
store i32 %N1N0T, i32* @x
%N0N0N1N1T = add i32 42, 0
%N1N0N1N1T = add i32 30, 0
%N0N1N1T = srem i32 %N0N0N1N1T, %N1N0N1N1T
%N1N1N1T = add i32 4, 0
%N1N1T = sdiv i32 %N0N1N1T, %N1N1N1T
store i32 %N1N1T, i32* @y
%N0N1N2T = add i32 8, 0
%N1N1N2T = add i32 5, 0
%N1N2T = add i32 %N0N1N2T, %N1N1N2T
store i32 %N1N2T, i32* @z
%N0N1N3T = add i32 1, 0
%N0N1N1N3T = add i32 5, 0
%N0N1N1N1N3T = add i32 2, 0
%N1N1N1N1N3T = add i32 2, 0
%N1N1N1N3T = mul i32 %N0N1N1N1N3T, %N1N1N1N1N3T
%N1N1N3T = sub i32 %N0N1N1N3T, %N1N1N1N3T
%t1 = add i32 %N0N1N3T, 0
%t2 = add i32 %N1N1N3T, 0
%t3 = mul i32 %t1, %t2
%t4 = icmp ne i32 %t3, 0
%N1N3T = zext i1 %t4 to i32
store i32 %N1N3T, i32* @a
%N0N0N1N4T = add i32 3, 0
%N0N1N0N1N4T = add i32 20, 0
%N1N1N0N1N4T = add i32 100, 0
%N1N0N1N4T = add i32 %N0N1N0N1N4T, %N1N1N0N1N4T
%N0N1N4T = mul i32 %N0N0N1N4T, %N1N0N1N4T
%N1N1N4T = add i32 291, 0
%N1N4T = sub i32 %N0N1N4T, %N1N1N4T
store i32 %N1N4T, i32* @b
ret i32 0
}

