@x = global i32 undef, align 4

define i32 @main() {
; x=0
%N1N0T = add i32 0, 0
store i32 %N1N0T, i32* @x
ret i32 0
}

