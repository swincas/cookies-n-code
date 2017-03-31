SOURCES := 	./src/main.c \
		./src/confObj.c \
		./src/parse_ini.c \
		./src/xmem.c \
		./src/xstring.c \
		./src/grid.c \
		./src/sources.c \
		./src/sources_to_grid.c \
		./src/fraction_q.c \
		./src/filtering.c \
		./src/phys_const.c \
		./src/self_shielding.c \
		./src/density_distribution.c \
		./src/recombination.c \
		./src/mean_free_path.c \
		./src/convolution_fftw.c \
		./src/utils.c\
		./src/input_redshifts.c\
		./src/input_grid.c \
		./src/photion_background.c \
		./src/redshift_tools.c \
		./src/cifog.c
OBJECTS := $(SOURCES:.c=.o)
DOBJECTS := $(SOURCES:.c=.d)
EXECUTABLE := cifog

# USE-MPI = YES

OPTIMIZE = -O3 -ftree-vectorize
WARNING = -Wall -Wextra -Wshadow -g

ifdef USE-MPI
	CC := mpicc
	CFLAGS := -c -std=c99 -march=native -lm $(WARNING) $(OPTIMIZE) -D __MPI
	LDFLAGS := -lfftw3_mpi -lfftw3 -lm -lmpich -lgsl -lgslcblas

else
	CC := gcc
	CFLAGS := -c -std=c99 -march=native -lm $(WARNING) $(OPTIMIZE) 
	#-D DEBUG_NREC
	LDFLAGS := -lfftw3 -lm -lgsl -lgslcblas
endif

.PHONY: all clean

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) $(LDFLAGS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@

clean: 
	rm -rf $(OBJECTS) $(DOBJECTS) $(EXECUTABLE)
