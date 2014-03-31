#include "c_driver.h"

int move_motor(int steps, int pin_number){
    //Define names
    char *filename_dir;
    char *filename_val;
    //define file handles
    FILE *fh_export, *fh_value, *fh_direction;
    int count=0;
    
    // making path name
    filename_dir = malloc(strlen("/sys/class/gpio/gpioXXX/direction")+1);
    sprintf(filename_dir, "/sys/class/gpio/gpio%d/direction", pin_number);
    printf("%s\n",filename_dir);
    
    filename_val = malloc(strlen("/sys/class/gpio/gpioXXX/value")+1);
    sprintf(filename_val, "/sys/class/gpio/gpio%d/value", pin_number);
    printf("%s\n",filename_val);

    //define pin variables
    int logic_status = 1;
    char* pin_direction = "out";
    fh_export = fopen("/sys/class/gpio/export", "w");
    if(fh_export == NULL) {printf("Unable to open export.\n");}
    //fseek(fh_export, 0, SEEK_SET);
    //fprintf(fh_export, "%d", pin_number);
    //fflush(fh_export);

    fh_direction = fopen(filename_dir, "w");
    if(fh_direction == NULL) {printf("Unable to open %s\n",filename_dir);}
    //fseek(fh_direction, 0, SEEK_SET);
    //fprintf(fh_direction, "%s", pin_direction);
    //fflush(fh_direction);

    fh_value = fopen(filename_val, "w");
    if(fh_value == NULL) {printf("Unable to open %s.\n",filename_val);}
    //fseek(fh_value, 0, SEEK_SET);
    //logic_status = 1;
    //fprintf(fh_value, "%d", logic_status);
    //fflush(fh_value);

    while(count<= steps)
    {
        //delay_us(5000);
        //delay_us(5);
        logic_status = logic_status?0:1;
        //write to gpio23
        //fprintf(fh_value, "%d", logic_status);
        //fflush(fh_value);
        count += 1;
    }
    //fclose(fh_export);
    //fclose(fh_direction);
    //fclose(fh_value);
    return count;
}
