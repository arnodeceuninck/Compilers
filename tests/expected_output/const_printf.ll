define i32 @main() {

; Code Block
; 42.0
%.v3 = fadd float 42.0, 0.0
; Print 42.0
%.v2 = fpext float %.v3 to double
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.strf, i32 0, i32 0), double %.v2)
; 42
%.v5 = add i32 42, 0
; Print 42
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.strd, i32 0, i32 0), i32 %.v5)
; b
%.v7 = add i8 98, 0
; Print b
call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.strc, i32 0, i32 0), i8 %.v7)


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
