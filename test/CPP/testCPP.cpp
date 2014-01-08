#include <stdio.h>
#include <stddef.h>
#include <unistd.h>
#include <time.h>
#define  output "out"
#define  input  "in"
int  main (void)
{
    //define file handles
    FILE *ofp_export, *ofp_P8_13_value, *ofp_P8_13_direction;
    //define pin variables
    int pin_dir =117, logic_status = 1;
    int stop = 0;
    char* pin_direction = output;
    //establish a direction and value file within export for P8_13
    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export.\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d", 88);
    fflush(ofp_export);
        fclose(ofp_export);


    //establish a direction and value file within export for P8_13
    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export.\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d",86);
    fflush(ofp_export);
        fclose(ofp_export);


    //establish a direction and value file within export for P8_13
    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export.\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d",32);
    fflush(ofp_export);
        fclose(ofp_export);


    //establish a direction and value file within export for P8_13
    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export.\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d",74);
    fflush(ofp_export);
        fclose(ofp_export);


    //establish a direction and value file within export for P8_13
    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export.\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d",72);
    fflush(ofp_export);
        fclose(ofp_export);

    //configure P8_13 for writing
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio88/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open P8_13_direction.\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
        fclose(ofp_P8_13_direction);
    //configure P8_13 for writing
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio86/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open P8_13_direction.\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
        fclose(ofp_P8_13_direction);
    //configure P8_13 for writing
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio32/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open P8_13_direction.\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
        fclose(ofp_P8_13_direction);
    //configure P8_13 for writing
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio74/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open P8_13_direction.\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
        fclose(ofp_P8_13_direction);
    //configure P8_13 for writing
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio72/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open P8_13_direction.\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
        fclose(ofp_P8_13_direction);

    while(stop == 5000){
        //write a logic 1 to P8_13 to illuminate the LED
        ofp_P8_13_value = fopen("/sys/class/gpio/gpio86/value", "w");
        if(ofp_P8_13_value == NULL) {printf("Unable to open gpio117_value.\n");}
        fseek(ofp_P8_13_value, 0, SEEK_SET);
        fprintf(ofp_P8_13_value, "%d", logic_status);
        fflush(ofp_P8_13_value);
        fclose(ofp_P8_13_value);

        logic_status = logic_status?0:1;
        sleep(5);
        stop += 1;
    }

    //configure P8_13 for writing
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio88/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open P8_13_direction.\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",);
    fflush(ofp_P8_13_direction);
        fclose(ofp_P8_13_direction);
    stop = 0;
    while(stop == 5000){
        //write a logic 1 to P8_13 to illuminate the LED
        ofp_P8_13_value = fopen("/sys/class/gpio/gpio86/value", "w");
        if(ofp_P8_13_value == NULL) {printf("Unable to open gpio117_value.\n");}
        fseek(ofp_P8_13_value, 0, SEEK_SET);
        fprintf(ofp_P8_13_value, "%d", logic_status);
        fflush(ofp_P8_13_value);
        fclose(ofp_P8_13_value);

        logic_status = logic_status?0:1;
        sleep(5);
        stop += 1;
    }


    return 1;
}
