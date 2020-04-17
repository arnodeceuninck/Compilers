; This is the constant array
@main.x = private unnamed_addr constant [3 x i8] c"abc", align 1
@.str = private unnamed_addr constant [3 x i8] c"%c\00", align 1

define i32 @main() {
  %1 = alloca [3 x i8], align 1
  %2 = alloca i8, align 1
  %3 = bitcast [3 x i8]* %1 to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %3, i8* getelementptr inbounds ([3 x i8], [3 x i8]* @main.x, i32 0, i32 0), i64 3, i32 1, i1 false)
  %4 = getelementptr inbounds [3 x i8], [3 x i8]* %1, i64 0, i64 0
  %5 = load i8, i8* %4, align 1
  store i8 %5, i8* %2, align 1
  %6 = load i8, i8* %2, align 1
  %7 = sext i8 %6 to i32
  %8 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 %7)
  ret i32 0
}

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)
