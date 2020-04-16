@x = global i32 undef, align 4

define i32 @main() {

; Code Block
; 0
%.v4 = add i32 0, 0
; x=0
store i32 %.v4, i32* @x


ret i32 0
}

