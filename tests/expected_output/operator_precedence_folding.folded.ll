@x = global i32 undef, align 4
@y = global i32 undef, align 4
@z = global i32 undef, align 4
@a = global i32 undef, align 4
@b = global i32 undef, align 4

define i32 @main() {
; x=6
%N1N0T = add i32 6, 0
store i32 %N1N0T, i32* @x
; y=3
%N1N1T = add i32 3, 0
store i32 %N1N1T, i32* @y
; z=13
%N1N2T = add i32 13, 0
store i32 %N1N2T, i32* @z
; a=1
%N1N3T = add i32 1, 0
store i32 %N1N3T, i32* @a
; b=69
%N1N4T = add i32 69, 0
store i32 %N1N4T, i32* @b
ret i32 0
}

