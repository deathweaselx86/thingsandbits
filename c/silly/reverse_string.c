#include <string.h>
#include <stdio.h>

void reverse_string(char *string);

int main(int argc, char * argv[])
{
	if (argc > 1)
	{
		int count;
		printf("There are %d valid arguments\n", argc - 1 );
	
		for(count=1;count<argc;count++)
		{
			printf("%d: %s\n", count, argv[count]);
			printf("This argument reversed is: ");
			reverse_string(argv[count]);
		}
	
		return 0;
	}
}

void reverse_string(char *string)
{
	int length, i;
	char swap;

	if (string == NULL)
		return;
	
	length = strlen(string);
	for(i=0;i<length/2;i++)
	{
		swap = string[i];
		string[i] = string[length-1-i];
		string[length-1-i]=swap;
	}
	
	printf("%s\n", string);
}
