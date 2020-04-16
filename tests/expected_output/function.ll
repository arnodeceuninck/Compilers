; Code Block
; test(int i)
define i32 @test(i32 i) #0 {
; Code Block
; 0
%.v8 = add i32 0, 0
; i=0
%i.3 = alloca i32, align 4
store i32 %.v8, i32* %i.3
; return
%.t11 = load i32, i32* %i.3
ret i32 %.t11
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
