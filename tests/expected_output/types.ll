@x = global float undef, align 4
@y = global i32 undef, align 4
@c = global i8 undef, align 1

define i32 @main() {

; Code Block
; 42.0
%.v4 = fadd float 42.0, 0.0
; x=42.0
store float %.v4, float* @x
; 42
%.v7 = add i32 42, 0
; y=42
store i32 %.v7, i32* @y
; b
%.v10 = add i8 98, 0
; c=b
store i8 %.v10, i8* @c


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
