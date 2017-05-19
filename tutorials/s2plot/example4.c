#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "s2plot.h"

COLOUR *initColour(int N)
{
   COLOUR *col = (COLOUR *)calloc(N, sizeof(COLOUR));
   if (col == NULL) { exit(0); }		/* Could not allocate memory */
   
   int i;
   for (i=0;i<N;i++) {				
      col[i].r = drand48();			/* Random coordinate in [0..1] */
      col[i].g = drand48();		   
      col[i].b = drand48();
   }
   return col;
}

XYZ *initData(int N)
{
   XYZ *xyz = (XYZ *)calloc(N, sizeof(XYZ));
   if (xyz == NULL) { exit(0); }		/* Could not allocate memory */
   
   int i;
   for (i=0;i<N;i++) {				
      xyz[i].x = drand48()*2.0 - 1.0;		/* Random coordinate in [-1..1] */
      xyz[i].y = drand48()*2.0 - 1.0;		   
      xyz[i].z = drand48()*2.0 - 1.0;
   }
   return xyz;
}

void cb(double *t, int *kc)
/* Dynamic geometry: needs to know about the data */
{
   static float radius = 0.1;				/* Radius of a sphere */
   static int N = 1000;
   static XYZ *xyz = NULL;
   static COLOUR *col = NULL;

   static int flag = -1;
   if (flag < 0) {
      xyz = initData(N);
      col = initColour(N);
      flag = 1;
   }

   int i;

   if (*kc %2 == 1) {
      for (i=0;i<N;i++) {
         ns2vsphere(xyz[i], radius, col[i]);	/* Draw a sphere using using the colour */
      }
   } else {
      COLOUR white = { 1.0, 1.0, 1.0 };
      for (i=0;i<N;i++) {
         ns2vsphere(xyz[i], radius, white);	/* Draw a sphere using using the colour */
      }
   }
}

int main(int argc, char *argv[])
{
   srand48((long)time(NULL));			/* Alway seed your RNG! */

   s2opend("/?",argc, argv);			/* Open the display */
   s2swin(-1.,1., -1.,1., -1.,1.);		/* Set the window coordinates */

/* Draw the coordinate box: character strings give formatting options */
   s2box("BCDETMNOPQ", 0,0, "BCDETMNOPQ", 0,0, "BDECTMNOPQ", 0,0);	

   s2lab("X-axis","Y-axis","Z-axis","Plot");	/* Write some labels */

   ss2ssr(10);					/* Set the resolution of the sphere */
   
   cs2scb(cb);

   s2show(1);					/* Open the s2plot window */
   
   return 1;
}
