#all: mainLM_hor_shift_fig6 mainLM_hor_shift_fig5 mainLM_hor_shift_exp1 mainLM_hor_shift_exp2 mainLM_hor_shift_exp3 mainLM_hor_shift_exp4 mainLM_hor_shift_exp5 mainLM_hor_shift_exp8 lib lib_time
all: lib_time 
 


	
lib_time: init_hor_shift.h constants_hor_shift.h LM_hor_shift.h LM_time_lib.c
	gcc -O3 -fPIC -shared LM_time_lib.c -o LM_time_lib.so



		
clean:
	rm -f *.o  LM_lib.so LM_time_lib.so mainLM_hor_shift

