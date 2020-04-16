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

; Code Block
; 0
%.v5 = add i32 0, 0
; 1
%.v6 = add i32 1, 0
; 0<=1
%.t92 = icmp sle i32 %.v5, %.v6
%.v4 = zext i1 %.t92 to i32
; x1=0<=1
store i32 %.v4, i32* @x1
; 0
%.v10 = add i32 0, 0
; 0
%.v11 = add i32 0, 0
; 0<=0
%.t93 = icmp sle i32 %.v10, %.v11
%.v9 = zext i1 %.t93 to i32
; x2=0<=0
store i32 %.v9, i32* @x2
; 1
%.v15 = add i32 1, 0
; 0
%.v16 = add i32 0, 0
; 1<=0
%.t94 = icmp sle i32 %.v15, %.v16
%.v14 = zext i1 %.t94 to i32
; x3=1<=0
store i32 %.v14, i32* @x3
; 0
%.v20 = add i32 0, 0
; 1
%.v21 = add i32 1, 0
; 0>=1
%.t95 = icmp sge i32 %.v20, %.v21
%.v19 = zext i1 %.t95 to i32
; y1=0>=1
store i32 %.v19, i32* @y1
; 0
%.v25 = add i32 0, 0
; 0
%.v26 = add i32 0, 0
; 0>=0
%.t96 = icmp sge i32 %.v25, %.v26
%.v24 = zext i1 %.t96 to i32
; y2=0>=0
store i32 %.v24, i32* @y2
; 1
%.v30 = add i32 1, 0
; 0
%.v31 = add i32 0, 0
; 1>=0
%.t97 = icmp sge i32 %.v30, %.v31
%.v29 = zext i1 %.t97 to i32
; y3=1>=0
store i32 %.v29, i32* @y3
; 0
%.v35 = add i32 0, 0
; 1
%.v36 = add i32 1, 0
; 0==1
%.t98 = icmp eq i32 %.v35, %.v36
%.v34 = zext i1 %.t98 to i32
; z1=0==1
store i32 %.v34, i32* @z1
; 0
%.v40 = add i32 0, 0
; 0
%.v41 = add i32 0, 0
; 0==0
%.t99 = icmp eq i32 %.v40, %.v41
%.v39 = zext i1 %.t99 to i32
; z2=0==0
store i32 %.v39, i32* @z2
; 1
%.v45 = add i32 1, 0
; 0
%.v46 = add i32 0, 0
; 1==0
%.t100 = icmp eq i32 %.v45, %.v46
%.v44 = zext i1 %.t100 to i32
; z3=1==0
store i32 %.v44, i32* @z3
; 0
%.v50 = add i32 0, 0
; 1
%.v51 = add i32 1, 0
; 0!=1
%.t101 = icmp ne i32 %.v50, %.v51
%.v49 = zext i1 %.t101 to i32
; a1=0!=1
store i32 %.v49, i32* @a1
; 0
%.v55 = add i32 0, 0
; 0
%.v56 = add i32 0, 0
; 0!=0
%.t102 = icmp ne i32 %.v55, %.v56
%.v54 = zext i1 %.t102 to i32
; a2=0!=0
store i32 %.v54, i32* @a2
; 1
%.v60 = add i32 1, 0
; 0
%.v61 = add i32 0, 0
; 1!=0
%.t103 = icmp ne i32 %.v60, %.v61
%.v59 = zext i1 %.t103 to i32
; a3=1!=0
store i32 %.v59, i32* @a3
; 0
%.v65 = add i32 0, 0
; 1
%.v66 = add i32 1, 0
; 0<1
%.t104 = icmp slt i32 %.v65, %.v66
%.v64 = zext i1 %.t104 to i32
; b1=0<1
store i32 %.v64, i32* @b1
; 0
%.v70 = add i32 0, 0
; 0
%.v71 = add i32 0, 0
; 0<0
%.t105 = icmp slt i32 %.v70, %.v71
%.v69 = zext i1 %.t105 to i32
; b2=0<0
store i32 %.v69, i32* @b2
; 1
%.v75 = add i32 1, 0
; 0
%.v76 = add i32 0, 0
; 1<0
%.t106 = icmp slt i32 %.v75, %.v76
%.v74 = zext i1 %.t106 to i32
; b3=1<0
store i32 %.v74, i32* @b3
; 0
%.v80 = add i32 0, 0
; 1
%.v81 = add i32 1, 0
; 0>1
%.t107 = icmp sgt i32 %.v80, %.v81
%.v79 = zext i1 %.t107 to i32
; c1=0>1
store i32 %.v79, i32* @c1
; 0
%.v85 = add i32 0, 0
; 0
%.v86 = add i32 0, 0
; 0>0
%.t108 = icmp sgt i32 %.v85, %.v86
%.v84 = zext i1 %.t108 to i32
; c2=0>0
store i32 %.v84, i32* @c2
; 1
%.v90 = add i32 1, 0
; 0
%.v91 = add i32 0, 0
; 1>0
%.t109 = icmp sgt i32 %.v90, %.v91
%.v89 = zext i1 %.t109 to i32
; c3=1>0
store i32 %.v89, i32* @c3


ret i32 0
}

