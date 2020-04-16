@x = global i32 undef, align 4
@y = global i32 undef, align 4

; Code Block
; 1
%.v5 = add i32 1, 0
; x=1
store i32 %.v5, i32* @x
; -1
%.v9 = add i32 -1, 0
; y=-1
store i32 %.v9, i32* @y

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
