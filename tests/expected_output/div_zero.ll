@y = global float undef, align 4

define i32 @main() {

; Code Block
; 5
%.v5 = add i32 5, 0
; 0
%.v6 = add i32 0, 0
; 5/0
%.v4 = sdiv i32 %.v5, %.v6
; y=5/0
store float %.v4, float* @y


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
