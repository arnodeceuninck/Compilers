@x = global i32 undef, align 4
@y = global i32 undef, align 4
@z = global i32 undef, align 4
@a = global i32 undef, align 4
@b = global i32 undef, align 4

define i32 @main() {

; Code Block
; 6
%.v10 = add i32 6, 0
; x=6
store i32 %.v10, i32* @x
; 3
%.v17 = add i32 3, 0
; y=3
store i32 %.v17, i32* @y
; 13
%.v22 = add i32 13, 0
; z=13
store i32 %.v22, i32* @z
; 1
%.v31 = add i32 1, 0
; a=1
store i32 %.v31, i32* @a
; 69
%.v40 = add i32 69, 0
; b=69
store i32 %.v40, i32* @b


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
