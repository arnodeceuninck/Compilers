@x1 = global float undef, align 4
@x2 = global float undef, align 4
@x3 = global float undef, align 4
@y = global float undef, align 4
@z1 = global float undef, align 4
@z2 = global float undef, align 4

; Code Block
; 0
%.v6 = add i32 0, 0
; x1=0
store float %.v6, float* @x1
; 0
%.v11 = add i32 0, 0
; x2=0
store float %.v11, float* @x2
; 1
%.v16 = add i32 1, 0
; x3=1
store float %.v16, float* @x3
; 1
%.v21 = add i32 1, 0
; y=1
store float %.v21, float* @y
; 1
%.v25 = add i32 1, 0
; z1=1
store float %.v25, float* @z1
; 0
%.v29 = add i32 0, 0
; z2=0
store float %.v29, float* @z2

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
