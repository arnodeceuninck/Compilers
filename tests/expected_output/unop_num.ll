@x = global i32 undef, align 4
@y = global i32 undef, align 4

define i32 @main() {

; Code Block
; 1
%.v5 = add i32 1, 0
; + 1
%.v4 = add i32 %.v5, 0
; x=+ 1
store i32 %.v4, i32* @x
; 1
%.v9 = add i32 1, 0
; - 1
%.v8 = sub i32 0, %.v9
; y=- 1
store i32 %.v8, i32* @y


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
