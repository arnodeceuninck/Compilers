@main.x = private unnamed_addr constant [3 x float] [float 1.000000e+00, float 2.000000e+00, float 3.000000e+00], align 4
@.str = private unnamed_addr constant [3 x i8] c"%f\00", align 1

define i32 @main() {
  %1 = alloca [3 x float], align 4
  %2 = alloca float, align 4
  %3 = bitcast [3 x float]* %1 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %3, i8* bitcast ([3 x float]* @main.x to i8*), i64 12, i32 4, i1 false)
  %4 = getelementptr inbounds [3 x float], [3 x float]* %1, i64 0, i64 0
  %5 = load float, float* %4, align 4
  store float %5, float* %2, align 4
  %6 = load float, float* %2, align 4
  %7 = fpext float %6 to double
  %8 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), double %7)
  ret i32 0
}

declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)
