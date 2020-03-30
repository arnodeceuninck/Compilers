@i_am_a_really_long_variable_withCamelCaseInBetween = global i32 undef, align 4

define i32 @main() {
%N1N0T = add i32 0, 0
store i32 %N1N0T, i32* @i_am_a_really_long_variable_withCamelCaseInBetween
ret i32 0
}

