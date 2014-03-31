#include "c_driver.h"

int move_motor(int steps, int number){
    char *filename;
    filename = malloc(strlen("path/to/xxx/gpio")+1);
    sprintf(filename, "path/to/%d/gpio", number);
    printf("%s\n",filename);
    return 0;
}
