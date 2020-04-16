@i_am_a_really_long_variable_withCamelCaseInBetween = global i32 undef, align 4

define i32 @main() {

; Code Block
; 0
%.v4 = add i32 0, 0
; i_am_a_really_long_variable_withCamelCaseInBetween=0
store i32 %.v4, i32* @i_am_a_really_long_variable_withCamelCaseInBetween


ret i32 0
}

@.strc = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.strd = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.strf = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @printf(i8*, ...)
