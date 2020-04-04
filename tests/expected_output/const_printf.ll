
define i32 @main() {
; Print 42.0
%N0N0T = fadd float 42.0, 0.0
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strf, i32 0, i32 0), double %N0T)
; Print 42
%N0N1T = add i32 42, 0
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strd, i32 0, i32 0), i32 %N1T)
; Print 'b'
%N0N2T = add i8 98, 0
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.strc, i32 0, i32 0), i8 %N2T)
ret i32 0
}

@.strc = private unnamed_addr constant [4 x i8] c"%c\0A\00", align 1
@.strd = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@.strf = private unnamed_addr constant [4 x i8] c"%f\0A\00", align 1
declare i32 @printf(i8*, ...)
