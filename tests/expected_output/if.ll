@x = global i32 undef, align 4

define i32 @main() {
; x=3
%N1N0T = add i32 3, 0
store i32 %N1N0T, i32* @x
; if x<12
ret i32 0
}

