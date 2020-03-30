@y = global float undef, align 4

define i32 @main() {
%N0N1N0T = add i32 5, 0
%N1N1N0T = add i32 0, 0
%N1N0T = sdiv i32 %N0N1N0T, %N1N1N0T
store float %N1N0T, float* @y
ret i32 0
}

