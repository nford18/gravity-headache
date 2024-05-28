#include <math.h>
#include <stdio.h>
#include <string.h>

/*
 * File is a start to a C version of dataFilling.py
 * ==> Remains unused <==
 */ 

char** line2Arr(char* line){
    // line[indexOf(line, '\n')] = '\0'; // strip the newline char
    char** output = malloc();
    char* token = strtok(line, ',');
    /* walk through other tokens */
    while( token != NULL && token != "\n") {
        printf( " %s\n", token );
    
        token = strtok(NULL, ",");
   }
}

int main(){
    FILE* new_file = fopen("./data/fullData.csv", "w+");
    fprintf(new_file, "%s\n", "\'e\', \'a\', \'i\', \'om\', \'w\', \'mass\',");
    FILE* file = fopen("./data/source_data.csv", "r");
    int i = 0;
    char* line;
    while(fgets(line, 512, file) != NULL){
        char* newline[10];
        char** lineArr;
        lineArr = line2Arr(line);
        



        fprintf(new_file, "\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\n",
            newline[0],newline[1],newline[2],newline[3],newline[4],
            newline[5],newline[6],newline[7],newline[8],newline[9]);
        i++;
    }
    fclose(file);
    fclose(new_file);
}
