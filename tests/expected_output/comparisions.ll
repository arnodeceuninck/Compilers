@x1 = global i32 undef, align 4
@x2 = global i32 undef, align 4
@x3 = global i32 undef, align 4
@y1 = global i32 undef, align 4
@y2 = global i32 undef, align 4
@y3 = global i32 undef, align 4
@z1 = global i32 undef, align 4
@z2 = global i32 undef, align 4
@z3 = global i32 undef, align 4
@a1 = global i32 undef, align 4
@a2 = global i32 undef, align 4
@a3 = global i32 undef, align 4
@b1 = global i32 undef, align 4
@b2 = global i32 undef, align 4
@b3 = global i32 undef, align 4
@c1 = global i32 undef, align 4
@c2 = global i32 undef, align 4
@c3 = global i32 undef, align 4

define i32 @main() {
; x1=0<=1
; 0<=1
%N0N1N0T = add i32 0, 0
%N1N1N0T = add i32 1, 0
%t1 = icmp sle i32 %N0N1N0T, %N1N1N0T
%N1N0T = zext i1 %t1 to i32
store i32 %N1N0T, i32* @x1
; x2=0<=0
; 0<=0
%N0N1N1T = add i32 0, 0
%N1N1N1T = add i32 0, 0
%t2 = icmp sle i32 %N0N1N1T, %N1N1N1T
%N1N1T = zext i1 %t2 to i32
store i32 %N1N1T, i32* @x2
; x3=1<=0
; 1<=0
%N0N1N2T = add i32 1, 0
%N1N1N2T = add i32 0, 0
%t3 = icmp sle i32 %N0N1N2T, %N1N1N2T
%N1N2T = zext i1 %t3 to i32
store i32 %N1N2T, i32* @x3
; y1=0>=1
; 0>=1
%N0N1N3T = add i32 0, 0
%N1N1N3T = add i32 1, 0
%t4 = icmp sge i32 %N0N1N3T, %N1N1N3T
%N1N3T = zext i1 %t4 to i32
store i32 %N1N3T, i32* @y1
; y2=0>=0
; 0>=0
%N0N1N4T = add i32 0, 0
%N1N1N4T = add i32 0, 0
%t5 = icmp sge i32 %N0N1N4T, %N1N1N4T
%N1N4T = zext i1 %t5 to i32
store i32 %N1N4T, i32* @y2
; y3=1>=0
; 1>=0
%N0N1N5T = add i32 1, 0
%N1N1N5T = add i32 0, 0
%t6 = icmp sge i32 %N0N1N5T, %N1N1N5T
%N1N5T = zext i1 %t6 to i32
store i32 %N1N5T, i32* @y3
; z1=0==1
; 0==1
%N0N1N6T = add i32 0, 0
%N1N1N6T = add i32 1, 0
%t7 = icmp eq i32 %N0N1N6T, %N1N1N6T
%N1N6T = zext i1 %t7 to i32
store i32 %N1N6T, i32* @z1
; z2=0==0
; 0==0
%N0N1N7T = add i32 0, 0
%N1N1N7T = add i32 0, 0
%t8 = icmp eq i32 %N0N1N7T, %N1N1N7T
%N1N7T = zext i1 %t8 to i32
store i32 %N1N7T, i32* @z2
; z3=1==0
; 1==0
%N0N1N8T = add i32 1, 0
%N1N1N8T = add i32 0, 0
%t9 = icmp eq i32 %N0N1N8T, %N1N1N8T
%N1N8T = zext i1 %t9 to i32
store i32 %N1N8T, i32* @z3
; a1=0!=1
; 0!=1
%N0N1N9T = add i32 0, 0
%N1N1N9T = add i32 1, 0
%t10 = icmp ne i32 %N0N1N9T, %N1N1N9T
%N1N9T = zext i1 %t10 to i32
store i32 %N1N9T, i32* @a1
; a2=0!=0
; 0!=0
%N0N1N10T = add i32 0, 0
%N1N1N10T = add i32 0, 0
%t11 = icmp ne i32 %N0N1N10T, %N1N1N10T
%N1N10T = zext i1 %t11 to i32
store i32 %N1N10T, i32* @a2
; a3=1!=0
; 1!=0
%N0N1N11T = add i32 1, 0
%N1N1N11T = add i32 0, 0
%t12 = icmp ne i32 %N0N1N11T, %N1N1N11T
%N1N11T = zext i1 %t12 to i32
store i32 %N1N11T, i32* @a3
; b1=0<1
; 0<1
%N0N1N12T = add i32 0, 0
%N1N1N12T = add i32 1, 0
%t13 = icmp slt i32 %N0N1N12T, %N1N1N12T
%N1N12T = zext i1 %t13 to i32
store i32 %N1N12T, i32* @b1
; b2=0<0
; 0<0
%N0N1N13T = add i32 0, 0
%N1N1N13T = add i32 0, 0
%t14 = icmp slt i32 %N0N1N13T, %N1N1N13T
%N1N13T = zext i1 %t14 to i32
store i32 %N1N13T, i32* @b2
; b3=1<0
; 1<0
%N0N1N14T = add i32 1, 0
%N1N1N14T = add i32 0, 0
%t15 = icmp slt i32 %N0N1N14T, %N1N1N14T
%N1N14T = zext i1 %t15 to i32
store i32 %N1N14T, i32* @b3
; c1=0>1
; 0>1
%N0N1N15T = add i32 0, 0
%N1N1N15T = add i32 1, 0
%t16 = icmp sgt i32 %N0N1N15T, %N1N1N15T
%N1N15T = zext i1 %t16 to i32
store i32 %N1N15T, i32* @c1
; c2=0>0
; 0>0
%N0N1N16T = add i32 0, 0
%N1N1N16T = add i32 0, 0
%t17 = icmp sgt i32 %N0N1N16T, %N1N1N16T
%N1N16T = zext i1 %t17 to i32
store i32 %N1N16T, i32* @c2
; c3=1>0
; 1>0
%N0N1N17T = add i32 1, 0
%N1N1N17T = add i32 0, 0
%t18 = icmp sgt i32 %N0N1N17T, %N1N1N17T
%N1N17T = zext i1 %t18 to i32
store i32 %N1N17T, i32* @c3
ret i32 0
}

