@x1 = global float undef, align 4
@x2 = global float undef, align 4
@x3 = global float undef, align 4
@y = global float undef, align 4
@z1 = global float undef, align 4
@z2 = global float undef, align 4

define i32 @main() {

; Code Block
; 0
%.v5 = add i32 0, 0
; 1
%.v6 = add i32 1, 0
; 0&&1
%.t30 = mul i32 %.v5, %.v6
%.t31 = icmp ne i32 %.t30, 0
%.v4 = zext i1 %.t31 to i32
; x1=0&&1
store float %.v4, float* @x1
; 0
%.v10 = add i32 0, 0
; 0
%.v11 = add i32 0, 0
; 0&&0
%.t32 = mul i32 %.v10, %.v11
%.t33 = icmp ne i32 %.t32, 0
%.v9 = zext i1 %.t33 to i32
; x2=0&&0
store float %.v9, float* @x2
; 1
%.v15 = add i32 1, 0
; 1
%.v16 = add i32 1, 0
; 1&&1
%.t34 = mul i32 %.v15, %.v16
%.t35 = icmp ne i32 %.t34, 0
%.v14 = zext i1 %.t35 to i32
; x3=1&&1
store float %.v14, float* @x3
; 0
%.v20 = add i32 0, 0
; 1
%.v21 = add i32 1, 0
; 0||1
%.t37 = add i32 %.v20, %.v21
%.t36 = icmp ne i32 %.t37, 0
%.v19 = zext i1 %.t36 to i32
; y=0||1
store float %.v19, float* @y
; 0
%.v25 = add i32 0, 0
; ! 0
%.t38 = icmp eq i32 0, %.v25
%.v24 = zext i1 %.t38 to i32
; z1=! 0
store float %.v24, float* @z1
; 1
%.v29 = add i32 1, 0
; ! 1
%.t39 = icmp eq i32 0, %.v29
%.v28 = zext i1 %.t39 to i32
; z2=! 1
store float %.v28, float* @z2


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
