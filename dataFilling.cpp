#include <cmath>
#include <cstdio>
#include <string>

/*
 * File may be a new version of dataFilling.py
 */ 

int main(){
    FILE* new_file = fopen("./data/fullData.csv", "w+");
    fprintf(new_file, "%s\n", "\'e\', \'a\', \'i\', \'om\', \'w\', \'mass\',");
    FILE* file = fopen("./data/source_data.csv", "r");
    int i = 0;
    char* line;
    while(fgets(line, 512, file) != NULL){
        
    }
}