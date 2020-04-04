@x = global float undef, align 4
@y = global i32 undef, align 4
@c = global i8 undef, align 1

define i32 @main() {
; x=42.0
%N1N0T = fadd float 42.0, 0.0
store float %N1N0T, float* @x
; y=42
%N1N1T = add i32 42, 0
store i32 %N1N1T, i32* @y
; c='b'
%N1N2T = add i8 98, 0
store i8 %N1N2T, i8* @c
ret i32 0
}

