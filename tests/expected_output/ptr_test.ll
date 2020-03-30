@x = global i32 undef, align 4
@y = global i32* undef, align 8
@z = global i32 undef, align 4

define i32 @main() {
%N1N0T = add i32 2, undef
store i32 %N1N0T, i32* @x
store i32* @x, i32** @y
%N1N2T = add i32 3, 0
store i32 %N1N2T, i32* @x
%t1 = load i32*, i32** @y
%N1N3T = load i32, i32* %t1
store i32 %N1N3T, i32* @z
%t2 = load i32, i32* @z
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strd, i32 0, i32 0), i32 %t2)
ret i32 0
}

@.strd = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
declare i32 @printf(i8*, ...)
