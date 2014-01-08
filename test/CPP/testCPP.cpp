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
    int logic_status = 0;
    int stop = 0;
    char* pin_direction = output;

    //EXPORTs
    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export. 88\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d", 88);
    fflush(ofp_export);
    fclose(ofp_export);


    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export. 86\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d",86);
    fflush(ofp_export);
    fclose(ofp_export);


    ofp_export = fopen("/sys/class/gpio/export", "w");
    if(ofp_export == NULL) {printf("Unable to open export. 32\n");}
    fseek(ofp_export, 0, SEEK_SET);
    fprintf(ofp_export, "%d",32);
    fflush(ofp_export);
    fclose(ofp_export);



    //PUT AS OUTPUT
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio88/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open. 88\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
    fclose(ofp_P8_13_direction);
    //
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio86/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open. 86\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
    fclose(ofp_P8_13_direction);
    //
    ofp_P8_13_direction = fopen("/sys/class/gpio/gpio32/direction", "w");
    if(ofp_P8_13_direction==NULL){printf("Unable to open. 32\n");}
    fseek(ofp_P8_13_direction, 0, SEEK_SET);
    fprintf(ofp_P8_13_direction, "%s",  pin_direction);
    fflush(ofp_P8_13_direction);
    fclose(ofp_P8_13_direction);

    //PUT SLEEP IN HIGH
    ofp_P8_13_value = fopen("/sys/class/gpio/gpio32/value", "w");
    if(ofp_P8_13_value == NULL) {printf("Unable to open. 32\n");}
    fseek(ofp_P8_13_value, 0, SEEK_SET);
    fprintf(ofp_P8_13_value, "%d", logic_status);
    fflush(ofp_P8_13_value);
    fclose(ofp_P8_13_value);
    
    //CHANGE DIRECTION T0 0
    ofp_P8_13_value = fopen("/sys/class/gpio/gpio88/value", "w");
    if(ofp_P8_13_value == NULL) {printf("Unable to open.\n");}
    fseek(ofp_P8_13_value, 0, SEEK_SET);
    fprintf(ofp_P8_13_value, "%d",0);
    fflush(ofp_P8_13_value);
    fclose(ofp_P8_13_value);

    while(stop == 5000){
        //PUT STEP in HIGH and LOW 
        ofp_P8_13_value = fopen("/sys/class/gpio/gpio86/value", "w");
        if(ofp_P8_13_value == NULL) {printf("Unable to open. 86\n");}
        fseek(ofp_P8_13_value, 0, SEEK_SET);
        fprintf(ofp_P8_13_value, "%d", logic_status);
        fflush(ofp_P8_13_value);
        fclose(ofp_P8_13_value);

        logic_status = logic_status?0:1;
        sleep(5);
        stop += 1;
    }

    //CHANGE DIRECTION TO OPOSIT DIRECTION
    ofp_P8_13_value = fopen("/sys/class/gpio/gpio88/value", "w");
    if(ofp_P8_13_value == NULL) {printf("Unable to open.\n");}
    fseek(ofp_P8_13_value, 0, SEEK_SET);
    fprintf(ofp_P8_13_value, "%d",1);
    fflush(ofp_P8_13_value);
    fclose(ofp_P8_13_value);
    stop = 0;
    while(stop == 5000){
        //PUT STEP in HIGH and LOW 
        ofp_P8_13_value = fopen("/sys/class/gpio/gpio86/value", "w");
        if(ofp_P8_13_value == NULL) {printf("Unable to open. 86\n");}
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
