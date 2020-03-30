
define i32 @main() {
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strf, i32 0, i32 0), double 42.0)
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strd, i32 0, i32 0), i32 42)
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strc, i32 0, i32 0), i8 98)
ret i32 0
}

@.strf = private unnamed_addr constant [4 x i8] c"%f\0A\00", align 1
@.strd = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@.strc = private unnamed_addr constant [4 x i8] c"%c\0A\00", align 1
declare i32 @printf(i8*, ...)
