; This is the constant array
@main.x = private unnamed_addr constant [3 x i32] [i32 1, i32 2, i32 3]
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1

define i32 @main() {
  ; This will allocate the space for the array
  %1 = alloca [3 x i32], align 4
  ; This will allocate the variable
  %2 = alloca i32, align 4
  ; I do not know what this does
  %3 = bitcast [3 x i32]* %1 to i8*
  ; Stores the value of the array in %1
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* %3, i8* bitcast ([3 x i32]* @main.x to i8*), i64 12, i32 4, i1 false)
  ; Gets the value of the array the last number is the iterate value
  %4 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 2
  ; Stores it in another variable since it is a pointer
  %5 = load i32, i32* %4, align 4
  store i32 %5, i32* %2, align 4
  %6 = load i32, i32* %2, align 4
  %7 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32 %6)
  ret i32 0
}

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i32, i1)

declare i32 @printf(i8*, ...)

