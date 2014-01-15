#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <time.h>
#include <sys/time.h>
#define output "out"
#define input "in"
void delay_us(int);

int main (int argc, char *argv[]) {
    //define file handles
    FILE *ofp_export, *ofp_value, *ofp_direction;
    
    //define pin variables
    int pin_number = 23, logic_status = 1;
    char* pin_direction = output;

    int steps = 0;
    int motor = 0;
    int stop = 0;

        motor = atoi(argv[1]);
        steps = atoi(argv[2]);
//step
//m1 => P8_27 => 86 
//m2 => P8_23 => 36
//m3 => P9_25 => 117
printf("m%d, steps=%d\n",motor,steps);

//motor 1 
    if (motor == 1){
        pin_number = 86;
        ofp_export = fopen("/sys/class/gpio/export", "w");
        if(ofp_export == NULL) {printf("Unable to open export.\n");}
        fseek(ofp_export, 0, SEEK_SET);
        fprintf(ofp_export, "%d", pin_number);
        fflush(ofp_export);
        ofp_direction = fopen("/sys/class/gpio/gpio86/direction", "w");
        if(ofp_direction == NULL) {printf("Unable to open gpio86_direction.\n");}
        fseek(ofp_direction, 0, SEEK_SET);
        fprintf(ofp_direction, "%s", pin_direction);
        fflush(ofp_direction);
        ofp_value = fopen("/sys/class/gpio/gpio86/value", "w");
        if(ofp_value == NULL) {printf("Unable to open gpio86_value.\n");}
        fseek(ofp_value, 0, SEEK_SET);
        logic_status = 1;
        fprintf(ofp_value, "%d", logic_status);
        fflush(ofp_value);
        while( stop <= steps)
        {
            //delay_us(5000);
            delay_us(5);
            logic_status = logic_status?0:1;
            //write to gpio86
            fprintf(ofp_value, "%d", logic_status);
            fflush(ofp_value);
            printf("%d\n",stop);
            stop += 1;
        }
        fclose(ofp_export);
        fclose(ofp_direction);
        fclose(ofp_value);
    }

//motor 2 
    if (motor == 2){
        pin_number = 36;
        ofp_export = fopen("/sys/class/gpio/export", "w");
        if(ofp_export == NULL) {printf("Unable to open export.\n");}
        fseek(ofp_export, 0, SEEK_SET);
        fprintf(ofp_export, "%d", pin_number);
        fflush(ofp_export);
        ofp_direction = fopen("/sys/class/gpio/gpio36/direction", "w");
        if(ofp_direction == NULL) {printf("Unable to open gpio36_direction.\n");}
        fseek(ofp_direction, 0, SEEK_SET);
        fprintf(ofp_direction, "%s", pin_direction);
        fflush(ofp_direction);
        ofp_value = fopen("/sys/class/gpio/gpio36/value", "w");
        if(ofp_value == NULL) {printf("Unable to open gpio36_value.\n");}
        fseek(ofp_value, 0, SEEK_SET);
        logic_status = 1;
        fprintf(ofp_value, "%d", logic_status);
        fflush(ofp_value);
        while( stop <= steps)
        {
            //delay_us(5000);
            delay_us(5);
            logic_status = logic_status?0:1;
            //write to gpio36
            fprintf(ofp_value, "%d", logic_status);
            fflush(ofp_value);
            printf("%d\n",stop);
            stop += 1;
        }
        fclose(ofp_export);
        fclose(ofp_direction);
        fclose(ofp_value);
    }

//motor 1 
    if (motor == 3){
        pin_number = 117;
        ofp_export = fopen("/sys/class/gpio/export", "w");
        if(ofp_export == NULL) {printf("Unable to open export.\n");}
        fseek(ofp_export, 0, SEEK_SET);
        fprintf(ofp_export, "%d", pin_number);
        fflush(ofp_export);
        ofp_direction = fopen("/sys/class/gpio/gpio117/direction", "w");
        if(ofp_direction == NULL) {printf("Unable to open gpio117_direction.\n");}
        fseek(ofp_direction, 0, SEEK_SET);
        fprintf(ofp_direction, "%s", pin_direction);
        fflush(ofp_direction);
        ofp_value = fopen("/sys/class/gpio/gpio117/value", "w");
        if(ofp_value == NULL) {printf("Unable to open gpio117_value.\n");}
        fseek(ofp_value, 0, SEEK_SET);
        logic_status = 1;
        fprintf(ofp_value, "%d", logic_status);
        fflush(ofp_value);
        while( stop <= steps)
        {
            //delay_us(5000);
            //delay_us(5);
            logic_status = logic_status?0:1;
            //write to gpio117
            fprintf(ofp_value, "%d", logic_status);
            fflush(ofp_value);
            printf("%d\n",stop);
            stop += 1;
        }
        fclose(ofp_export);
        fclose(ofp_direction);
        fclose(ofp_value);
    }


    return 1;
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

