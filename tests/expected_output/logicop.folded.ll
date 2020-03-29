@x1 = global float 0.0, align 4
@x2 = global float 0.0, align 4
@x3 = global float 0.0, align 4
@y = global float 0.0, align 4
@z1 = global float 0.0, align 4
@z2 = global float 0.0, align 4

define i32 @main() {
%N1N0T = add i32 0, 0
store float %N1N0T, float* @x1
%N1N1T = add i32 0, 0
store float %N1N1T, float* @x2
%N1N2T = add i32 1, 0
store float %N1N2T, float* @x3
%N1N3T = add i32 1, 0
store float %N1N3T, float* @y
%N1N4T = add i32 1, 0
store float %N1N4T, float* @z1
%N1N5T = add i32 0, 0
store float %N1N5T, float* @z2
ret i32 0
}

