.globl main
.data
	victoryMessage: .asciiz "Congratulations you won!"
	colorBlue: .word 0x000000ff
	colorGreen: .word 0x007fff00
	colorYellow: .word 0x00ffff00
	colorBlack: .word 0x00000000
	# these are all the possible positions our figure can go
	# You need to see them by pairs of 2
	arrayOfNextPossiblePositions: .word -1, 0, 1, 0, 0, -1, 0, 1
	visited: .space 2048

	file: .asciiz "" #path to file for reading
	buffer: .space 1024 #We reserve 1024 bytes for the buffer
.text
########################################################################
#procedure to read and display the file on the bitmap
readAndDisplay:
	sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
	move	$fp, $sp	# frame	pointer now points to the top of the stack
	subu	$sp, $sp, 8	# allocate 8 bytes on the stack
	sw	$ra, -4($fp)	# store the value of the return address

readFile:
	li 	$v0, 13 	#We ask the system to open the file
	la 	$a0, file	#We give the system the path to the file
	li 	$a1, 0 		#We set flag to 0
	li 	$a2, 0 		#We set the mode to 0
	syscall

	move 	$a0, $v0 	#We move the file descriptor to $a0

	li 	$v0, 14 	#We ask the system to read the file into the buffer
	la 	$a1, buffer 	#We give the system the adress of the buffer
	la 	$a2, 1024 	#We give max amount of characters to be read
	syscall

	la 	$t0, buffer
	#we close the file thats in the file descriptor
	#because it is loaded in the buffer
	li 	$v0, 16
	syscall

	li 	$t1, 0

init:
	move 	$t3, $gp	#store the start of the bitmap display in $t3
	li	$s1, 0		#kolom
	li	$s2, 0		#rij

drawMap:
	loopRow:
		loopColumn:
			lbu 	$t1, ($t0)
			beqz 	$t1, exitReadAndDisplay
			lb 	$t1, ($t0)
			beq	$t1, 'w', paintBlue
			beq	$t1, 's', paintYellow
			beq	$t1, 'u', paintGreen
			beq	$t1, 'p', paintBlack
			beq	$t1, '\n', jump
		return:
			addi 	$t3, $t3, 4
			addi	$t0, $t0, 1
			addi	$s1, $s1, 1
			j	loopColumn
	jump:
		addi 	$t0, $t0, 1
		li	$s1, 0
		addi	$s2, $s2, 1
		j 	loopRow
paintGreen:
	lw 	$a0, colorGreen 	#store the color red in $a0
	sw 	$a0, ($t3) 		#display the color on the correct position
	move 	$s6, $s2		#store the position of the end in $s6
	move	$s7, $s1		# and in $s7
	j  	return			#return back to the previous position
paintBlue:
	lw 	$a0, colorBlue	 	#store the color red in $a0
	sw 	$a0, ($t3) 		#display the color on the correct position
	j  	return 			#return back to the previous position
paintYellow:
	lw 	$a0, colorYellow 	#store the color red in $a0
	sw 	$a0, ($t3) 		#display the color on the correct position
	move	$v0, $s2		#store the start position in the registers
					#$v0 and $v1
	move	$v1, $s1
	j  	return 			#return back to the previous position
paintBlack:
	lw 	$a0, colorBlack	 	#store the color red in $a0
	sw 	$a0, ($t3) 		#display the color on the correct position
	j  	return			#return back to the previous position

exitReadAndDisplay:
	lw	$ra, -4($fp)    # get return address from frame
	move	$sp, $fp        # get old frame pointer from current frame
	lw	$fp, ($sp)	# restore old frame pointer
	jr	$ra

########################################################################
#procedure to perform a dfs
dfs:
	sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
	move	$fp, $sp	# frame	pointer now points to the top of the stack
	subu	$sp, $sp, 52	# allocate 60 bytes on the stack
	sw	$ra, -4($fp)	# store the value of the return address
	sw	$s0, -8($fp)
	sw	$s1, -12($fp)
	sw	$s4, -16($fp)
	sw	$s5, -20($fp)
	sw	$t0, -24($fp)
	sw	$t1, -28($fp)
	sw	$t2, -32($fp)
	sw	$t3, -36($fp)
	sw	$t7, -40($fp)
	sw	$t8, -44($fp)
	sw	$t9, -48($fp)

	move 	$s0, $a0
	move	$s1, $a1
	move	$t9, $a2

	# We check if the current position is the exit and
	# we print a victory message if it is so
	bne	$s0, $s6, notWon
	bne	$s1, $s7, notWon
	j	youWon

	notWon:

	la	$s5, arrayOfNextPossiblePositions 	#$s5 iterates over all the
							#possible positions we can go to
	li 	$s4, 0

	loopMove:
		beq	$s4, 4, exitDfs	#If we iterated over all possible next positions
					#We finish the dfs procedure
		lw	$t0, 4($s5) 	#We load the value to calculate the
					#next row position into $t0
		add	$t0, $t0, $s0   #We calculate the next row location
		lw	$t1, ($s5)	#We load the value to calculate the
					#next column position into $t1
		add	$t1, $t1, $s1	#We calculate the next column location

		li	$t8, 0		#This is the iterator of the visited positions

		la	$t7, visited	#We store the adress of the visited positions in
					#$t7
		checkPositionInVisited:
			beq 	$t8, $t9, exitCheckPositionInVisited 	#$t9 contains the length of the visited positions

			#We check if the next position has already been visited
			lw	$s2, 0($t7) #by loading the x coordinate into $s2
			lw	$s3, 4($t7) #and the y coordinate into $s3

			#We check if both of the next possible coordinate is already taken if so
			#it must be two times equal
			bne 	$t0, $s2, addOne
			bne 	$t1, $s3, addOne
			j	returnLoopMove
			addOne:
				#if it doesnt equal to the coordinate give the next coordinate of the visited list
				#By increasing the index $t8 and the adress where the coordinates
				#are stored $t7
				addi $t8, $t8, 1
				addi $t7, $t7, 8
				j checkPositionInVisited

		exitCheckPositionInVisited:
			#We store the coordinates at the last available adress
			#of the visited list
			sw	$t0, 0($t7)
			sw	$t1, 4($t7)
			addi	$t9, $t9, 1 #We increase the length by 1

			#We update the players position by overloading the old coordinate
			#of the player and the newly stored coordinate
			move	$a0, $s0
			move	$a1, $s1
			move	$a2, $t0
			move	$a3, $t1
			jal	updatePlayerPosition

			#We retrieve the new coordinates of the player if there were any
			move	$t2, $v0
			move	$t3, $v1

			#We put the system short in sleep in order to maintain smoothness in the program
			li	$v0, 32
			la	$a0, 60
			syscall

			#if the original coordinates ($s0, $s1) of the player do equal to
			#the new coordinates ($t2, $t3) of update player then we need to
			#loop again
			bne	$t2, $s0, performNewDfs
			bne	$t3, $s1, performNewDfs
			j	loopAgain
			performNewDfs:
				#we need to perform a new dfs because the location of the player has been updated
				move	$a0, $t2
				move	$a1, $t3
				move	$a2, $t9
				jal 	dfs
			loopAgain:
				#We go back to the previous position of the player
				move	$a0, $t2
				move	$a1, $t3
				move	$a2, $s0
				move	$a3, $s1
				jal 	updatePlayerPosition

				#and once again we put the system to sleep
				li	$v0, 32
				la	$a0, 60
				syscall
	returnLoopMove:
		#If we reached the end of the program we need to loop back
		#and excecute it once again with a new coordinate to move to
		#else we exit the recursive calls
		addi	$s4, $s4, 1
		addi	$s5, $s5, 8
		j	loopMove

exitDfs:
	#We destroy the stackframe by retrieving the registers that
	#Were occupied before the procedure was called
	lw	$t9, -48($fp)
	lw	$t8, -44($fp)
	lw	$t7, -40($fp)
	lw	$t3, -36($fp)
	lw	$t2, -32($fp)
	lw	$t1, -28($fp)
	lw	$t0, -24($fp)
	lw	$s5, -20($fp)
	lw	$s4, -16($fp)
	lw	$s1, -12($fp)
	lw	$s0, -8($fp)
	lw	$ra, -4($fp)    # get return address from frame
	move	$sp, $fp        # get old frame pointer from current fra
	lw	$fp, ($sp)	# restore old frame pointer
	jr	$ra

########################################################################
#procedure to update the players position based on
#the keyboard input
updatePlayerPosition:
	sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
	move	$fp, $sp	# frame	pointer now points to the top of the stack
	subu	$sp, $sp, 36	# allocate 8 bytes on the stack
	sw	$ra, -4($fp)	# store the value of the return address
	sw	$t0, -8($fp)
	sw	$t1, -12($fp)
	sw	$s0, -16($fp)
	sw	$s1, -20($fp)
	sw	$s2, -24($fp)
	sw	$s3, -28($fp)
	sw	$s4, -32($fp)

	move	$s0, $a0	#current player row
	move	$s1, $a1	#current player column
	move	$s2, $a2	#new player row
	move	$s3, $a3	#new player column

	#We exit the procedure when the next position is equal to the previous
	seq	$t0, $s0, $s2	#To achieve this we check if the next is equal to
				#the previous position
	seq	$t1, $s1, $s3
	and	$t0, $t0, $t1	#if the rows are equal and the columns are equal
				#We need to exit the function
	beq	$t0, 1, exitCurrent

	#We calculate the next position of the player on the bitmap
	move	$a0, $s2
	move	$a1, $s3
	jal	calculateAdress

	#if it is equal to the a wall exit the function and give back the current
	#coordinates
	lw 	$a0, colorBlue
	lw	$s4, ($v0)
	beq	$a0, $s4, exitCurrent

	#Else print a yellow color on the next position
	lw	$a0, colorYellow
	sw	$a0, ($v0)

	#and paint the previous position black
	PaintCurrentPositionBlack:
		move 	$a0, $s0
		move	$a1, $s1
		jal	calculateAdress

		lw	$a0, colorBlack
		sw	$a0, ($v0)

		#If the next color ($a1) is green give print the victory message
		#and quit the function
	checkVictory:
		lw	$a0, colorGreen
		beq	$a0, $s4, youWon
		#Else exit the procedure with the coordinates of the next position
		j	exitNew

exitNew:
	move	$v0, $s2
	move	$v1, $s3
	j 	exitUpdatePlayerPosition

exitCurrent:
	move	$v0, $s0
	move	$v1, $s1

exitUpdatePlayerPosition:
	# We recover all the used registers in the stackframe
	lw	$s4, -32($fp)
	lw	$s3, -28($fp)
	lw	$s2, -24($fp)
	lw	$s1, -20($fp)
	lw	$s0, -16($fp)
	lw	$t1, -12($fp)
	lw	$t0, -8($fp)
	lw	$ra, -4($fp)    # get return address from frame
	move	$sp, $fp        # get old frame pointer from current fra
	lw	$fp, ($sp)	# restore old frame pointer
	jr	$ra

########################################################################
#procedure to calculate the a position in the bitmap display
calculateAdress:
	sw	$fp, 0($sp)	# push old frame pointer (dynamic link)
	move	$fp, $sp	# frame	pointer now points to the top of the stack
	subu	$sp, $sp, 24	# allocate 24 bytes on the stack
	sw	$ra, -4($fp)	# store the value of the return address
	sw	$s0, -8($fp)	# save locally used registers
	sw	$s1, -12($fp)
	sw	$s2, -16($fp)
	sw	$s3, -20($fp)

	move	$s0, $a0	#store the parameters given with the function in $s0
				#and $s1
	move	$s1, $a1

	li	$s2, 4
	li	$s3, 32

	#calculate the row adress
	mul 	$s0, $s2, $s0
	mul	$s0, $s3, $s0
	#calculate the column
	mul 	$s1, $s2, $s1

	add 	$s1, $s0, $s1
	add	$s1, $gp, $s1 	#add our result of the array and store it in $s1
				#the register that contains the base adress of the display

	move	$v0, $s1	#The return value: the adress of the location to check for

	lw	$s3, -20($fp)	# reset saved register $s3
	lw	$s2, -16($fp)	# reset saved register $s2
	lw	$s1, -12($fp)	# reset saved register $s1
	lw	$s0, -8($fp)	# reset saved register $s0
	lw	$ra, -4($fp)    # get return address from frame
	move	$sp, $fp        # get old frame pointer from current frame
	lw	$fp, ($sp)	# restore old frame pointer
	jr	$ra
########################################################################
#Starting Point
main:
	jal	readAndDisplay		# Call procedure readAndDisplay
					# gives back the start position
	move	$a0, $v0
	move	$a1, $v1
	li	$a2, 0
	jal 	dfs
#this displays a victory message and then exits the program
youWon:
	li	$v0, 4
	la	$a0, victoryMessage
	syscall

exit:
	li   	$v0, 10 		# system call for exit
	syscall      			# exit (back to operating system)
