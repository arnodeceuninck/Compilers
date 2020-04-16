@x = global i32 undef, align 4
@y = global i32* undef, align 8
@z = global i32 undef, align 4

define i32 @main() {

; Code Block
; 2
%.v4 = add i32 2, 0
; x=2
store i32 %.v4, i32* @x
%.t18 = load i32, i32* @x
; y=& x
store i32* @x, i32** @y
; 3
%.v11 = add i32 3, 0
; x=3
store i32 %.v11, i32* @x
%.t19 = load i32*, i32** @y
%.v14 = load i3, i3* %.t19
; z=* y
store i32 %.v14, i32* @z
; Print z
%.t20 = load i32, i32* @z
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.strd, i32 0, i32 0), i32 %.t20)


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
