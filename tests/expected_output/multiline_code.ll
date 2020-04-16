@x = global i32 undef, align 4

; Code Block
; 0
%.v4 = add i32 0, 0
; x=0
store i32 %.v4, i32* @x

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
