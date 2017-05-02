#include <stdio.h>
#include <stdlib.h>
#include "s2plot.h"

int main(int argc, char *argv[])
{
   s2opend("/?",argc, argv);			/* Open the display */
   s2swin(-1.,1., -1.,1., -1.,1.);		/* Set the window coordinates */

/* Draw the coordinate box: character strings give formatting options */
   s2box("BCDETMNOPQ", 0,0, "BCDETMNOPQ", 0,0, "BDECTMNOPQ", 0,0);	

   s2lab("X-axis","Y-axis","Z-axis","Plot");	/* Write some labels */

   s2show(1);					/* Open the s2plot window */
   
   return 1;
}
