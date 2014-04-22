#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>


extern int move_motor(int steps, char *pin_step);
extern int handle_gpio(int logic_status, char *pin_step);
extern void delay_us(int n_sleep);
extern void  flush_all(void);

#define MAGIC 0x31337


