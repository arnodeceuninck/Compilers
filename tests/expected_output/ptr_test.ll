@x = global i32 undef, align 4
@y = global i32* undef, align 8
@z = global i32 undef, align 4

define i32 @main() {
; x=2
%N1N0T = add i32 2, 0
store i32 %N1N0T, i32* @x
; y=& x
store i32* @x, i32** @y
; x=3
%N1N2T = add i32 3, 0
store i32 %N1N2T, i32* @x
; z=* y
; * y
%N0N1N3T = load i32*, i32** @y
%N1N3T = load i32, i32* %N0N1N3T
store i32 %N1N3T, i32* @z
; Print z
%N0N4T = load i32, i32* @z
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strd, i32 0, i32 0), i32 %N4T)
ret i32 0
}

@.strd = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
declare i32 @printf(i8*, ...)
