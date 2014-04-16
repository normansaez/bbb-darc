#include "c_driver.h"

void flush_all(){
    int i=1;
    for (i=1;i<=53;i++)
        printf("%i\n",i);
}

int move_motor(int steps, char *pin_step){
    //Define names
    char *filename_dir;
    char *filename_val;
    int gpio_num = 0;
    //define file handles
    FILE *fh_export, *fh_value, *fh_direction;
    int count=0;

    if (strcmp(pin_step,"P8_27") == 0 )
        gpio_num = 86;
    if (strcmp(pin_step,"P8_23") == 0)
        gpio_num = 36;
    if (strcmp(pin_step,"P9_25") == 0)
        gpio_num = 117;
    if (gpio_num == 0)
        return -1;

    // making path name
    filename_dir = malloc(strlen("/sys/class/gpio/gpioXXX/direction")+1);
    sprintf(filename_dir, "/sys/class/gpio/gpio%d/direction", gpio_num);
    printf("%s\n",filename_dir);

    filename_val = malloc(strlen("/sys/class/gpio/gpioXXX/value")+1);
    sprintf(filename_val, "/sys/class/gpio/gpio%d/value", gpio_num);
    printf("%s\n",filename_val);

    //define pin variables
    int logic_status = 1;
    int delay = 1000;
    char* pin_direction = "out";

    fh_export = fopen("/sys/class/gpio/export", "w");
    if(fh_export == NULL) {printf("Unable to open export.\n");}
    fseek(fh_export, 0, SEEK_SET);
    fprintf(fh_export, "%d", gpio_num);
    fflush(fh_export);

    fh_direction = fopen(filename_dir, "w");
    if(fh_direction == NULL) {printf("Unable to open %s\n",filename_dir);}
    fseek(fh_direction, 0, SEEK_SET);
    fprintf(fh_direction, "%s", pin_direction);
    fflush(fh_direction);

    fh_value = fopen(filename_val, "w");
    if(fh_value == NULL) {printf("Unable to open %s.\n",filename_val);}
    fseek(fh_value, 0, SEEK_SET);
    logic_status = 1;
    fprintf(fh_value, "%d", logic_status);
    fflush(fh_value);

//if(gpio_num == 117)
//delay = 5000;

    while(count < (2*steps))
    {
        delay_us(delay);
        logic_status = logic_status?0:1;
        fprintf(fh_value, "%d", logic_status);
        fflush(fh_value);
        count += 1;
    }
    fclose(fh_export);
    fclose(fh_direction);
    fclose(fh_value);
    return count;
}

//******************************************************************
void delay_us(int desired_delay_us)
{
    struct timeval tv_start; //start time hack
    struct timeval tv_now; //current time hack
    int elapsed_time_us;
    gettimeofday(&tv_start, NULL);
    elapsed_time_us = 0;
    while(elapsed_time_us < desired_delay_us)
    {
        gettimeofday(&tv_now, NULL);
        if(tv_now.tv_usec >= tv_start.tv_usec)
            elapsed_time_us = tv_now.tv_usec - tv_start.tv_usec;
        else
            elapsed_time_us = (1000000 - tv_start.tv_usec) + tv_now.tv_usec;
        //printf("start: %ld \n", tv_start.tv_usec);
        //printf("now: %ld \n", tv_now.tv_usec);
        //printf("desired: %d \n", desired_delay_ms);
        //printf("elapsed: %d \n\n", elapsed_time_ms);
    }
}
//******************************************************************

