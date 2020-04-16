@x = global i32 undef, align 4

; Code Block
; 3
%.v5 = add i32 3, 0
; x=3
store i32 %.v5, i32* @x
; if x<12
; 12
%.v9 = add i32 12, 0
%.t13 = load i32, i32* @x
; x<12
%.v7 = icmp slt i32 %.t13, %.v9
br i1 %.v7, label %iftrue6, label %iffalse6
iftrue6:

; Code Block
; 4
%.v12 = add i32 4, 0
; x=4
store i32 %.v12, i32* @x

br label %end6
iffalse6:

br label %end6
end6:


@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
