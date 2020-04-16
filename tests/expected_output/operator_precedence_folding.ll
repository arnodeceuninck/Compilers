@x = global i32 undef, align 4
@y = global i32 undef, align 4
@z = global i32 undef, align 4
@a = global i32 undef, align 4
@b = global i32 undef, align 4

; Code Block
; 4
%.v7 = add i32 4, 0
; 2
%.v8 = add i32 2, 0
; 4*2
%.v6 = mul i32 %.v7, %.v8
; 1
%.v9 = add i32 1, 0
; 4*2+1
%.v5 = add i32 %.v6, %.v9
; 3
%.v10 = add i32 3, 0
; 4*2+1-3
%.v4 = sub i32 %.v5, %.v10
; x=4*2+1-3
store i32 %.v4, i32* @x
; 42
%.v15 = add i32 42, 0
; 30
%.v16 = add i32 30, 0
; 42%30
%.v14 = srem i32 %.v15, %.v16
; 4
%.v17 = add i32 4, 0
; 42%30/4
%.v13 = sdiv i32 %.v14, %.v17
; y=42%30/4
store i32 %.v13, i32* @y
; 8
%.v21 = add i32 8, 0
; 5
%.v22 = add i32 5, 0
; 8+5
%.v20 = add i32 %.v21, %.v22
; z=8+5
store i32 %.v20, i32* @z
; 1
%.v26 = add i32 1, 0
; 5
%.v28 = add i32 5, 0
; 2
%.v30 = add i32 2, 0
; 2
%.v31 = add i32 2, 0
; 2*2
%.v29 = mul i32 %.v30, %.v31
; 5-2*2
%.v27 = sub i32 %.v28, %.v29
; 1&&5-2*2
%.t41 = mul i32 %.v26, %.v27
%.t42 = icmp ne i32 %.t41, 0
%.v25 = zext i1 %.t42 to i32
; a=1&&5-2*2
store i32 %.v25, i32* @a
; 3
%.v36 = add i32 3, 0
; 20
%.v38 = add i32 20, 0
; 100
%.v39 = add i32 100, 0
; 20+100
%.v37 = add i32 %.v38, %.v39
; 3*20+100
%.v35 = mul i32 %.v36, %.v37
; 291
%.v40 = add i32 291, 0
; 3*20+100-291
%.v34 = sub i32 %.v35, %.v40
; b=3*20+100-291
store i32 %.v34, i32* @b

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
