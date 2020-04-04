@x1 = global float undef, align 4
@x2 = global float undef, align 4
@x3 = global float undef, align 4
@y = global float undef, align 4
@z1 = global float undef, align 4
@z2 = global float undef, align 4

define i32 @main() {
; x1=0
%N1N0T = add i32 0, 0
store float %N1N0T, float* @x1
; x2=0
%N1N1T = add i32 0, 0
store float %N1N1T, float* @x2
; x3=1
%N1N2T = add i32 1, 0
store float %N1N2T, float* @x3
; y=1
%N1N3T = add i32 1, 0
store float %N1N3T, float* @y
; z1=1
%N1N4T = add i32 1, 0
store float %N1N4T, float* @z1
; z2=0
%N1N5T = add i32 0, 0
store float %N1N5T, float* @z2
ret i32 0
}

