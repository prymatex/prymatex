#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int count_spaces(char* text) {
    int count = 0;
    int index;
    for (index = 0; text[index] != '\0'; index++)
        if (text[index] == ' ')
            count++;
    return count;
}

int main(int argc, char** argv){
//strtok (args[1], " ");
    int args_len = argc + 1;
    char* env = "/usr/bin/env";
    int i;
    
    if (argc > 1)
        args_len += count_spaces(argv[1]);
    
    char* args[args_len];
    
    /* split arguments */
    args[0] = env;
    i = 1;
    args[i] = strtok(argv[1], " ");
    while(args[i] != NULL) {
        i++;
        args[i] = strtok(NULL, " ");
    }
    
    execv(env, argv);
    return 0;
}
