@x1 = global float undef, align 4
@x2 = global float undef, align 4
@x3 = global float undef, align 4
@y = global float undef, align 4
@z1 = global float undef, align 4
@z2 = global float undef, align 4

define i32 @main() {
%N0N1N0T = add i32 0, 0
%N1N1N0T = add i32 1, 0
%t1 = add i32 %N0N1N0T, 0
%t2 = add i32 %N1N1N0T, 0
%t3 = mul i32 %t1, %t2
%t4 = icmp ne i32 %t3, 0
%N1N0T = zext i1 %t4 to i32
store float %N1N0T, float* @x1
%N0N1N1T = add i32 0, 0
%N1N1N1T = add i32 0, 0
%t5 = add i32 %N0N1N1T, 0
%t6 = add i32 %N1N1N1T, 0
%t7 = mul i32 %t5, %t6
%t8 = icmp ne i32 %t7, 0
%N1N1T = zext i1 %t8 to i32
store float %N1N1T, float* @x2
%N0N1N2T = add i32 1, 0
%N1N1N2T = add i32 1, 0
%t9 = add i32 %N0N1N2T, 0
%t10 = add i32 %N1N1N2T, 0
%t11 = mul i32 %t9, %t10
%t12 = icmp ne i32 %t11, 0
%N1N2T = zext i1 %t12 to i32
store float %N1N2T, float* @x3
%N0N1N3T = add i32 0, 0
%N1N1N3T = add i32 1, 0
%t13 = add i32 %N0N1N3T, 0
%t14 = add i32 %N1N1N3T, 0
%t15 = add i32 %t13, %t14
%t16 = icmp ne i32 %t15, 0
%N1N3T = zext i1 %t16 to i32
store float %N1N3T, float* @y
store float %N1N4T, float* @z1
store float %N1N5T, float* @z2
ret i32 0
}

