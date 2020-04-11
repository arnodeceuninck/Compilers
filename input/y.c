int i = 0;
while(i < 10){
	printf(i);
	if (i == 5){
		break;
	} else {
	    i = i + 1;
	    continue;
	}
	i = 10;
}