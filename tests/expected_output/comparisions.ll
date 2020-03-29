@x1 = global i32 0, align 4
@x2 = global i32 0, align 4
@x3 = global i32 0, align 4
@y1 = global i32 0, align 4
@y2 = global i32 0, align 4
@y3 = global i32 0, align 4
@z1 = global i32 0, align 4
@z2 = global i32 0, align 4
@z3 = global i32 0, align 4
@a1 = global i32 0, align 4
@a2 = global i32 0, align 4
@a3 = global i32 0, align 4
@b1 = global i32 0, align 4
@b2 = global i32 0, align 4
@b3 = global i32 0, align 4
@c1 = global i32 0, align 4
@c2 = global i32 0, align 4
@c3 = global i32 0, align 4

define i32 @main() {
%N0N1N0T = add i32 0, 0
%N1N1N0T = add i32 1, 0
%t1 = add i32 %N0N1N0T, 0
%t2 = add i32 %N1N1N0T, 0
%t3 = icmp sle i32 %t1, %t2
%N1N0T = zext i1 %t3 to i32
store i32 %N1N0T, i32* @x1
%N0N1N1T = add i32 0, 0
%N1N1N1T = add i32 0, 0
%t4 = add i32 %N0N1N1T, 0
%t5 = add i32 %N1N1N1T, 0
%t6 = icmp sle i32 %t4, %t5
%N1N1T = zext i1 %t6 to i32
store i32 %N1N1T, i32* @x2
%N0N1N2T = add i32 1, 0
%N1N1N2T = add i32 0, 0
%t7 = add i32 %N0N1N2T, 0
%t8 = add i32 %N1N1N2T, 0
%t9 = icmp sle i32 %t7, %t8
%N1N2T = zext i1 %t9 to i32
store i32 %N1N2T, i32* @x3
%N0N1N3T = add i32 0, 0
%N1N1N3T = add i32 1, 0
%t10 = add i32 %N0N1N3T, 0
%t11 = add i32 %N1N1N3T, 0
%t12 = icmp sge i32 %t10, %t11
%N1N3T = zext i1 %t12 to i32
store i32 %N1N3T, i32* @y1
%N0N1N4T = add i32 0, 0
%N1N1N4T = add i32 0, 0
%t13 = add i32 %N0N1N4T, 0
%t14 = add i32 %N1N1N4T, 0
%t15 = icmp sge i32 %t13, %t14
%N1N4T = zext i1 %t15 to i32
store i32 %N1N4T, i32* @y2
%N0N1N5T = add i32 1, 0
%N1N1N5T = add i32 0, 0
%t16 = add i32 %N0N1N5T, 0
%t17 = add i32 %N1N1N5T, 0
%t18 = icmp sge i32 %t16, %t17
%N1N5T = zext i1 %t18 to i32
store i32 %N1N5T, i32* @y3
%N0N1N6T = add i32 0, 0
%N1N1N6T = add i32 1, 0
%t19 = add i32 %N0N1N6T, 0
%t20 = add i32 %N1N1N6T, 0
%t21 = icmp eq i32 %t19, %t20
%N1N6T = zext i1 %t21 to i32
store i32 %N1N6T, i32* @z1
%N0N1N7T = add i32 0, 0
%N1N1N7T = add i32 0, 0
%t22 = add i32 %N0N1N7T, 0
%t23 = add i32 %N1N1N7T, 0
%t24 = icmp eq i32 %t22, %t23
%N1N7T = zext i1 %t24 to i32
store i32 %N1N7T, i32* @z2
%N0N1N8T = add i32 1, 0
%N1N1N8T = add i32 0, 0
%t25 = add i32 %N0N1N8T, 0
%t26 = add i32 %N1N1N8T, 0
%t27 = icmp eq i32 %t25, %t26
%N1N8T = zext i1 %t27 to i32
store i32 %N1N8T, i32* @z3
%N0N1N9T = add i32 0, 0
%N1N1N9T = add i32 1, 0
%t28 = add i32 %N0N1N9T, 0
%t29 = add i32 %N1N1N9T, 0
%t30 = icmp ne i32 %t28, %t29
%N1N9T = zext i1 %t30 to i32
store i32 %N1N9T, i32* @a1
%N0N1N10T = add i32 0, 0
%N1N1N10T = add i32 0, 0
%t31 = add i32 %N0N1N10T, 0
%t32 = add i32 %N1N1N10T, 0
%t33 = icmp ne i32 %t31, %t32
%N1N10T = zext i1 %t33 to i32
store i32 %N1N10T, i32* @a2
%N0N1N11T = add i32 1, 0
%N1N1N11T = add i32 0, 0
%t34 = add i32 %N0N1N11T, 0
%t35 = add i32 %N1N1N11T, 0
%t36 = icmp ne i32 %t34, %t35
%N1N11T = zext i1 %t36 to i32
store i32 %N1N11T, i32* @a3
%N0N1N12T = add i32 0, 0
%N1N1N12T = add i32 1, 0
%t37 = add i32 %N0N1N12T, 0
%t38 = add i32 %N1N1N12T, 0
%t39 = icmp slt i32 %t37, %t38
%N1N12T = zext i1 %t39 to i32
store i32 %N1N12T, i32* @b1
%N0N1N13T = add i32 0, 0
%N1N1N13T = add i32 0, 0
%t40 = add i32 %N0N1N13T, 0
%t41 = add i32 %N1N1N13T, 0
%t42 = icmp slt i32 %t40, %t41
%N1N13T = zext i1 %t42 to i32
store i32 %N1N13T, i32* @b2
%N0N1N14T = add i32 1, 0
%N1N1N14T = add i32 0, 0
%t43 = add i32 %N0N1N14T, 0
%t44 = add i32 %N1N1N14T, 0
%t45 = icmp slt i32 %t43, %t44
%N1N14T = zext i1 %t45 to i32
store i32 %N1N14T, i32* @b3
%N0N1N15T = add i32 0, 0
%N1N1N15T = add i32 1, 0
%t46 = add i32 %N0N1N15T, 0
%t47 = add i32 %N1N1N15T, 0
%t48 = icmp sgt i32 %t46, %t47
%N1N15T = zext i1 %t48 to i32
store i32 %N1N15T, i32* @c1
%N0N1N16T = add i32 0, 0
%N1N1N16T = add i32 0, 0
%t49 = add i32 %N0N1N16T, 0
%t50 = add i32 %N1N1N16T, 0
%t51 = icmp sgt i32 %t49, %t50
%N1N16T = zext i1 %t51 to i32
store i32 %N1N16T, i32* @c2
%N0N1N17T = add i32 1, 0
%N1N1N17T = add i32 0, 0
%t52 = add i32 %N0N1N17T, 0
%t53 = add i32 %N1N1N17T, 0
%t54 = icmp sgt i32 %t52, %t53
%N1N17T = zext i1 %t54 to i32
store i32 %N1N17T, i32* @c3
ret i32 0
}

