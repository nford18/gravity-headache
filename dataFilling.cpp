#include <cmath>
#include <cstdio>
#include <string>
// #include "matplot++.h"

int main(){
    FILE* new_file = fopen("./data/fullData.csv", "w+");
    fprintf(new_file, "%s\n", "\'e\', \'a\', \'i\', \'om\', \'w\', \'mass\',");
    FILE* file = fopen("./data/source_data.csv", "r");
    int i = 0;
    char* line;
    while(fgets(line, 512, file) != NULL){
        
    }
}