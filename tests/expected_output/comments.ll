@x = global i32 undef, align 4

define i32 @main() {

; Code Block
; 0
%1 = add i32 0, 0
; x=0
store i32 %1, i32* @x


ret i32 0
}

