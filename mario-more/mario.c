#include <stdio.h>
#include <cs50.h>

int main(void){
int h;
int spaces;
    do{
        h = get_int("height: ");//seguramente haya que declarar h en algun otro lado
    }
    while(h < 1 || h>8);

    for (int i=1; i<=h; i++){

        spaces = h-i;
        for(int j=0;j<spaces;j++){
            printf(" ");
        }
        for(int n=0;n<i;n++){
            printf("#");

        }
        printf("  "); //espacio en medio
        for(int n=0;n<i;n++){
            printf("#");
        }
        for(int j=0;j<spaces;j++){
            printf(" ");
        }
        printf("\n");

    }//for

}//main

