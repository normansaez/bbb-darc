#include "c_driver.h"

void flush_all(){
    int i=1;
    for (i=1;i<=53;i++)
        printf("%i\n",i);
}

int handle_gpio(int logic_status, char *pin_step){
    //Define names
    char *filename_dir;
    char *filename_val;
    char* pin_direction = "out";
    int gpio_num = 0;

    //prevent unknow status
    if (!(logic_status == 1 || logic_status == 0))
        return -1;

    //define file handles
    FILE *fh_export, *fh_value, *fh_direction;

    if (strcmp(pin_step,"P8_1") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P8_2") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P8_3") == 0 )
        gpio_num = 38;
    if (strcmp(pin_step,"P8_4") == 0 )
        gpio_num = 39;
    if (strcmp(pin_step,"P8_5") == 0 )
        gpio_num = 34;
    if (strcmp(pin_step,"P8_6") == 0 )
        gpio_num = 35;
    if (strcmp(pin_step,"P8_7") == 0 )
        gpio_num = 66;
    if (strcmp(pin_step,"P8_8") == 0 )
        gpio_num = 67;
    if (strcmp(pin_step,"P8_9") == 0 )
        gpio_num = 69;
    if (strcmp(pin_step,"P8_10") == 0 )
        gpio_num = 68;
    if (strcmp(pin_step,"P8_11") == 0 )
        gpio_num = 45;
    if (strcmp(pin_step,"P8_12") == 0 )
        gpio_num = 44;
    if (strcmp(pin_step,"P8_13") == 0 )
        gpio_num = 23;
    if (strcmp(pin_step,"P8_14") == 0 )
        gpio_num = 26;
    if (strcmp(pin_step,"P8_15") == 0 )
        gpio_num = 47;
    if (strcmp(pin_step,"P8_16") == 0 )
        gpio_num = 46;
    if (strcmp(pin_step,"P8_17") == 0 )
        gpio_num = 27;
    if (strcmp(pin_step,"P8_18") == 0 )
        gpio_num = 65;
    if (strcmp(pin_step,"P8_19") == 0 )
        gpio_num = 22;
    if (strcmp(pin_step,"P8_20") == 0 )
        gpio_num = 63;
    if (strcmp(pin_step,"P8_21") == 0 )
        gpio_num = 62;
    if (strcmp(pin_step,"P8_22") == 0 )
        gpio_num = 37;
    if (strcmp(pin_step,"P8_23") == 0 )
        gpio_num = 36;
    if (strcmp(pin_step,"P8_24") == 0 )
        gpio_num = 33;
    if (strcmp(pin_step,"P8_25") == 0 )
        gpio_num = 32;
    if (strcmp(pin_step,"P8_26") == 0 )
        gpio_num = 61;
    if (strcmp(pin_step,"P8_27") == 0 )
        gpio_num = 86;
    if (strcmp(pin_step,"P8_28") == 0 )
        gpio_num = 88;
    if (strcmp(pin_step,"P8_29") == 0 )
        gpio_num = 87;
    if (strcmp(pin_step,"P8_30") == 0 )
        gpio_num = 89;
    if (strcmp(pin_step,"P8_31") == 0 )
        gpio_num = 10;
    if (strcmp(pin_step,"P8_32") == 0 )
        gpio_num = 11;
    if (strcmp(pin_step,"P8_33") == 0 )
        gpio_num = 9;
    if (strcmp(pin_step,"P8_34") == 0 )
        gpio_num = 81;
    if (strcmp(pin_step,"P8_35") == 0 )
        gpio_num = 8;
    if (strcmp(pin_step,"P8_36") == 0 )
        gpio_num = 80;
    if (strcmp(pin_step,"P8_37") == 0 )
        gpio_num = 78;
    if (strcmp(pin_step,"P8_38") == 0 )
        gpio_num = 79;
    if (strcmp(pin_step,"P8_39") == 0 )
        gpio_num = 76;
    if (strcmp(pin_step,"P8_40") == 0 )
        gpio_num = 77;
    if (strcmp(pin_step,"P8_41") == 0 )
        gpio_num = 74;
    if (strcmp(pin_step,"P8_42") == 0 )
        gpio_num = 75;
    if (strcmp(pin_step,"P8_43") == 0 )
        gpio_num = 72;
    if (strcmp(pin_step,"P8_44") == 0 )
        gpio_num = 73;
    if (strcmp(pin_step,"P8_45") == 0 )
        gpio_num = 70;
    if (strcmp(pin_step,"P8_46") == 0 )
        gpio_num = 71;
    if (strcmp(pin_step,"P9_1") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_2") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_3") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_4") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_5") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_6") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_7") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_8") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_9") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_10") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_11") == 0 )
        gpio_num = 30;
    if (strcmp(pin_step,"P9_12") == 0 )
        gpio_num = 60;
    if (strcmp(pin_step,"P9_13") == 0 )
        gpio_num = 31;
    if (strcmp(pin_step,"P9_14") == 0 )
        gpio_num = 50;
    if (strcmp(pin_step,"P9_15") == 0 )
        gpio_num = 48;
    if (strcmp(pin_step,"P9_16") == 0 )
        gpio_num = 51;
    if (strcmp(pin_step,"P9_17") == 0 )
        gpio_num = 5;
    if (strcmp(pin_step,"P9_18") == 0 )
        gpio_num = 4;
    if (strcmp(pin_step,"P9_19") == 0 )
        gpio_num = 13;
    if (strcmp(pin_step,"P9_20") == 0 )
        gpio_num = 12;
    if (strcmp(pin_step,"P9_21") == 0 )
        gpio_num = 3;
    if (strcmp(pin_step,"P9_22") == 0 )
        gpio_num = 2;
    if (strcmp(pin_step,"P9_23") == 0 )
        gpio_num = 49;
    if (strcmp(pin_step,"P9_24") == 0 )
        gpio_num = 15;
    if (strcmp(pin_step,"P9_25") == 0 )
        gpio_num = 117;
    if (strcmp(pin_step,"P9_26") == 0 )
        gpio_num = 14;
    if (strcmp(pin_step,"P9_27") == 0 )
        gpio_num = 115;
    if (strcmp(pin_step,"P9_28") == 0 )
        gpio_num = 113;
    if (strcmp(pin_step,"P9_29") == 0 )
        gpio_num = 111;
    if (strcmp(pin_step,"P9_30") == 0 )
        gpio_num = 112;
    if (strcmp(pin_step,"P9_31") == 0 )
        gpio_num = 110;
    if (strcmp(pin_step,"P9_32") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_33") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_34") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_35") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_36") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_37") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_38") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_39") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_40") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_41A") == 0 )
        gpio_num = 20;
    if (strcmp(pin_step,"P9_41B") == 0 )
        gpio_num = 116;
    if (strcmp(pin_step,"P9_42A") == 0 )
        gpio_num = 7;
    if (strcmp(pin_step,"P9_42B") == 0 )
        gpio_num = 114;
    if (strcmp(pin_step,"P9_43") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_44") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_45") == 0 )
        gpio_num = 0;
    if (strcmp(pin_step,"P9_46") == 0 )
        gpio_num = 0;
    if (gpio_num == 0)
        return -1;

    // making path name
    filename_dir = malloc(strlen("/sys/class/gpio/gpioXXX/direction")+1);
    sprintf(filename_dir, "/sys/class/gpio/gpio%d/direction", gpio_num);
    printf("%s\n",filename_dir);

    filename_val = malloc(strlen("/sys/class/gpio/gpioXXX/value")+1);
    sprintf(filename_val, "/sys/class/gpio/gpio%d/value", gpio_num);
    printf("%s\n",filename_val);


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
    fprintf(fh_value, "%d", logic_status);
    fflush(fh_value);

    fclose(fh_export);
    fclose(fh_direction);
    fclose(fh_value);
    return 0;
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

