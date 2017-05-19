*****************************************
S2PLOT (GEM by Chris Fluke, 26/04/2017)
*****************************************

- `Presentation (pdf) <s2plot2017.pdf>`_

---------------  
Example codes
---------------

- `Hello Interactive 3D World <example1.c>`_

.. code:: c

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

              return EXIT_SUCCESS;
          }

   
- `Randomly Coloured 3D Points <example2.c>`_

.. code:: c

          #include <stdio.h>
          #include <stdlib.h>
          #include <time.h>
          #include "s2plot.h"
          
          int main(int argc, char *argv[])
          {
              srand48((long)time(NULL));			/* Alway seed your RNG! */

              s2opend("/?",argc, argv);			/* Open the display */
              s2swin(-1.,1., -1.,1., -1.,1.);		/* Set the window coordinates */

              /* Draw the coordinate box: character strings give formatting options */
              s2box("BCDETMNOPQ", 0,0, "BCDETMNOPQ", 0,0, "BDECTMNOPQ", 0,0);	

              s2lab("X-axis","Y-axis","Z-axis","Plot");	/* Write some labels */

              int N = 1000;				/* How many points to plot? */
              XYZ xyz;					/* A vector position */
              COLOUR col;					/* An RGB colour */
              for (int i=0;i<N;i++) {				
                  xyz.x = drand48()*2.0 - 1.0;		/* Random coordinate in [-1..1] */
                  xyz.y = drand48()*2.0 - 1.0;		   
                  xyz.z = drand48()*2.0 - 1.0;

                  col.r = drand48();			/* Random colour map in [0..1] */
                  col.g = drand48();
                  col.b = drand48();
                  
                  ns2vpoint(xyz, col);			/* Plot the point using the colour */
              }

              s2show(1);					/* Open the s2plot window */

              return EXIT_SUCCESS;
          }

   
- `Randomly Coloured 3D Spheres <example3.c>`_

.. code:: c
          
          #include <stdio.h>
          #include <stdlib.h>
          #include <time.h>
          #include "s2plot.h"
          
          int main(int argc, char *argv[])
          {
              srand48((long)time(NULL));			/* Alway seed your RNG! */
              
              s2opend("/?",argc, argv);			/* Open the display */
              s2swin(-1.,1., -1.,1., -1.,1.);		/* Set the window coordinates */
              
              /* Draw the coordinate box: character strings give formatting options */
              s2box("BCDETMNOPQ", 0,0, "BCDETMNOPQ", 0,0, "BDECTMNOPQ", 0,0);	
          
              s2lab("X-axis","Y-axis","Z-axis","Plot");	/* Write some labels */
              

              int N = 1000;				/* How many points to plot? */
              XYZ xyz;					/* A vector position */
              COLOUR col;					/* An RGB colour */

              float radius = 0.1;				/* Radius of a sphere */
              ss2ssr(10);					/* Set the resolution of the sphere */

              for (int i=0;i<N;i++) {				
                  xyz.x = drand48()*2.0 - 1.0;		/* Random coordinate in [-1..1] */
                  xyz.y = drand48()*2.0 - 1.0;		   
                  xyz.z = drand48()*2.0 - 1.0;

                  col.r = drand48();			/* Random colour map in [0..1] */
                  col.g = drand48();
                  col.b = drand48();

                  ns2vsphere(xyz, radius, col);		/* Draw a sphere using using the colour */
              }

              s2show(1);					/* Open the s2plot window */
   
              return EXIT_SUCCESS;
          }

          

