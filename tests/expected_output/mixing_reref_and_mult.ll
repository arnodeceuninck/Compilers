@x = global i32 undef, align 4
@y = global i32* undef, align 8

; Code Block
; 1
%.v4 = add i32 1, 0
; x=1
store i32 %.v4, i32* @x
%.t15 = load i32, i32* @x
; y=& x
store i32* @x, i32** @y
; 2
%.v12 = add i32 2, 0
%.t16 = load i32*, i32** @y
%.v13 = load i3, i3* %.t16
; 2** y
%.v11 = mul i32 %.v12, %.v13
; x=2** y
store i32 %.v11, i32* @x

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
