@x1 = global float undef, align 4
@x2 = global float undef, align 4
@x3 = global float undef, align 4
@y = global float undef, align 4
@z1 = global float undef, align 4
@z2 = global float undef, align 4

define i32 @main() {
; x1=0&&1
; 0&&1
%N0N1N0T = add i32 0, 0
%N1N1N0T = add i32 1, 0
%t1 = mul i32 %N0N1N0T, %N1N1N0T
%t2 = icmp ne i32 %t1, 0
%N1N0T = zext i1 %t2 to i32
store float %N1N0T, float* @x1
; x2=0&&0
; 0&&0
%N0N1N1T = add i32 0, 0
%N1N1N1T = add i32 0, 0
%t3 = mul i32 %N0N1N1T, %N1N1N1T
%t4 = icmp ne i32 %t3, 0
%N1N1T = zext i1 %t4 to i32
store float %N1N1T, float* @x2
; x3=1&&1
; 1&&1
%N0N1N2T = add i32 1, 0
%N1N1N2T = add i32 1, 0
%t5 = mul i32 %N0N1N2T, %N1N1N2T
%t6 = icmp ne i32 %t5, 0
%N1N2T = zext i1 %t6 to i32
store float %N1N2T, float* @x3
; y=0||1
; 0||1
%N0N1N3T = add i32 0, 0
%N1N1N3T = add i32 1, 0
%t7 = add i32 %N0N1N3T, %N1N1N3T
%t8 = icmp ne i32 %t7, 0
%N1N3T = zext i1 %t8 to i32
store float %N1N3T, float* @y
; z1=! 0
; ! 0
store float %N1N4T, float* @z1
; z2=! 1
; ! 1
store float %N1N5T, float* @z2
ret i32 0
}

