#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
/*
 *	Jessica Ross, Cpr E 308 Project 1: UNIX Shell
 * 
 * 	The command used to compile this is:
 * 	gcc -lc -o shell -g shell-ross-1.c */

/* This is the default prompt. */
#define defprompt "308sh>\0"

char* get_command();
/* It's not feasible to use a fixed sized buffer, so I wanted to have a
 * dynamic buffer from stdin. Initially I wanted to use gets() to get 
 * the input from stdin, but that is dangerous. Funny things happen
 * after buffer overruns. Therefore I remove characters from stdin one
 * at a time until '\n' and remove '\n' because those are dangerous.
 *
 * This function returns a pointer to the string of characters returned
 * from stdin. This pointer must be deallocated manually. */
int input_type(char* cmd);
/* This shell does different things based on the input. This function
 * returns an int based on what the shell is to do. 
 *
 */

int parse_command(char* command, char** command_arguments);
/* This function turns the line of input into something execvp can 
 * digest. It returns the number of strings that command_arguments carries. */

int main(int argc, char** argv)
{
	int ret,pid, size_of_arguments;
	int status;
	char *ourcwd= NULL;
	char* prompt = NULL;
	char* command = NULL;
	char* path = NULL;
	char *command_arguments[16]; /*This is used only when there are
				       command-line arguments. There shouldn't
				       be more than 16... hope there aren't,
				       anyway. */

	if(argc > 2)
	{
		/* for the prompt to be any different, I expect
		 * to have the calling process to call it like
		 * 'shell -p [prompt], so there should be 3 arguments
		 * else I think I'd like to ignore that input */
		        
		prompt = malloc(sizeof(char) * strlen(argv[2]));
		strcpy(prompt,argv[2]);
	}

	else
	{
		prompt = malloc(sizeof(char)*strlen(defprompt));
		strcpy(prompt,defprompt);
	}

	while(1)
	{
		if(command != NULL)
			free(command);
		printf("%s ", prompt);	
		command = get_command();
		/* My parsing code strips '/'. I don't have time
		 * to think about that right now, so this is a 
		 * quick fix. For now, it works. */
		path = malloc(sizeof(command)-3);
		path  = command+3;
		/* Sometimes command just returns a NULL character
		 * I'd prefer not to do anything then. What's the point
		 * of spawning a useless process? */
		if(command[0] != '\0')
		{
		ret = input_type(command);
		size_of_arguments = parse_command(command,command_arguments);
		switch(ret)
		{
			case 1:		printf("%d \n",getppid());
					break;
					
			case 2:		printf("%d \n",getpid());
					break;
					
			case 3:		free(prompt);
					free(command);
					exit(1);
					return 0;
					break;
			
			case 4:	
					pid = fork();
					if(pid < 0) /* There's been a fork error. */
					{	perror("fork: ");
						exit(1);
					}
					else
					{
						if(pid == 0)
						{
						
							printf("Child PID: %d \n", getpid());
							/* It seems that I have to tell the child process to go away if something goes wrong... */
							if(execvp(command,command_arguments) < 0) 
								{
									perror(command);
									exit(1);
								}
						}
					
						else
						{
							waitpid(-1,&status,WNOHANG);
							if(WIFEXITED(status))
								printf("Process %d exited normally.\n",pid);
							if(WIFSIGNALED(status))
								printf("Process %d was killed.\n",pid);
						}
					}
					
			break;

			case 5: 	ourcwd = getcwd(ourcwd,0);	
					/* getcwd() called with a NULL
					 * pointer and 0 size will make
					 * as much space as is needed to
					 * show the directory name, using
					 * malloc(). */
					if(ourcwd != NULL)
					{
						puts(ourcwd);	
						free(ourcwd);
						/* I suppose that I should 
						 * deallocate memory. Memory
						 * leaks are sort of bad.
						 * Also going to set ourcwd = 
						 * NULL just to make sure
						 * nothing weird
						 * happens to it. */
						ourcwd = NULL;
					}
					else /* getcwd didn't work?? waah. */
						perror("getcwd ");
					break;
					
			case 6:	
					pid = chdir(path);
					setenv("PWD",path,1);
					if(pid < 0)
						perror("chdir ");
					/* This is only an issue if something
					 * weird happens. */
					break;
			default:	pid = fork();
					if(pid < 0)
					{	perror("fork: ");
						exit(1);
					}
					else
					{
						if(pid == 0) /* The child does this. */
						{
							printf("Child PID: %d \n", getpid());
							if(execvp(command,command_arguments) < 0)
							{
								perror(command);
								exit(1);
							}
						}
						else
						{

							waitpid(pid,&status,0);
							if(WIFEXITED(status))
								printf("Process %d exited normally.\n",pid);
							if(WIFSIGNALED(status))
								printf("Process %d signalled somehow and killed.\n",pid);
								
						}
					}
					break;
					
		}
	} }

}

/* This tells that big switch statement up there what to do. */
int input_type(char* cmd)
{
	/* print the shell's parent's process id */
	if(strcmp(cmd,"ppid") == 0) 
		return 1;
	/* print the shell's process id */
	if(strcmp(cmd,"pid") == 0)
		return 2;

	/* we're done, clean up and quit the shell */
	if(strcmp(cmd,"exit") == 0)
		return 3;

	/* this is one of those nasty backgrounded commands */
	if(strpbrk(cmd,"&") != '\0')
		return 4;

	/* all we want is the current working directory */
	if(strcmp(cmd,"cd") == 0)
		return 5;

	/* CHANGE THE STUPID CURRENT WORKING DIRECTORY! AAAAH */
	if(strstr(cmd,"cd") != '\0' && strcmp(cmd,"cd") > 0)
		return 6;

	else /* chances are that we want to execute something. oooh. */
		return 0;
}

/* This is a dynamically allocated buffer for stdin. I would have prefered
 * to use gets(), but that's not safe. Stupid gets(). 
 *
 * This function returns a pointer to allocated memory and input string.*/
char* get_command()
{
	size_t buf_size = 1;
	char *cmd;
	
	cmd = malloc(1); /* Not sure if realloc works with a zero size... so..*/
	cmd[buf_size-1] = getchar();
	while(cmd[buf_size-1] != '\n')
	{
		buf_size = buf_size+1;
		cmd = realloc(cmd,buf_size);
		cmd[buf_size-1] = getchar();
		 if(cmd[buf_size-1] == '\t')
			cmd[buf_size-1] = ' ';
	}
	cmd[buf_size-1] = '\0'; 
	/* Occasionally this will have us get input consisting of exactly one
	 * null character. I'd like to skip stuff if that's the case. */
	return cmd;
}

int parse_command(char* command, char** command_arguments)
{
	int ic, ica; /* ic is the index that we are currently at in command
			and ica is the index that we are currently at
			in command arguments */
	ic = 0;
	ica = 0;
	/* This continues while we aren't out of input and while we
	 * aren't out of space for the arguments. I promise I'll make this
	 * dynamic if I have time... */
	while(ica < 16)
	{
		command_arguments[ica] = '\0';
		ica = ica+1;
	}
	ica = 0;
	while(*command != '\0')
	{
		while(*command == ' ')
			*command++ = '\0';
			
		*command_arguments++ = command;

		
		while(*command != '\0' && *command != ' ')
			command++;	
	}
	
	command_arguments[ica] = '\0';
	if(command_arguments[ica-1][strlen(command_arguments[ica-1])-1] == '&')
			command_arguments[ica-1] = '\0';
	return ica;
}	
