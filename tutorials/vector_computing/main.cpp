/* Sequential demonstration prepared for AVX Cookies 'n' Code Session
   Dr. Matthew Smith, msmith@astro.swin.edu.au  */

#include <stdio.h>
#include <stdlib.h>    // For posix_memalign
#include <math.h>
#include <immintrin.h> // For AVX Intrinsic functions and types

void Compute_C_AVX512(float *x, float *y, float *z, int N);

int main() {
	int N = 1025;	   // N = size of problem, a power of 2 is good.
	int NT;
	float *a, *b, *c;  // Three vectors containing N elements
	float error = 0.0; // Used later for testing
	size_t size;
	size_t alignment = 64;
	int i;

	// Compute Padded Length
	NT = (int)((N+16-1)/16);
	NT = 16*NT;
	size = NT*sizeof(float);
	// Print for our confirmation
	printf("Original problem size = %d, Modified problem size = %d\n", N, NT);

	// Allocate memory along cache boundaries
	posix_memalign((void**)&a, alignment, size);
        posix_memalign((void**)&b, alignment, size);
        posix_memalign((void**)&c, alignment, size);

	// Initialise a and b vectors
	for (i = 0; i < N; i++) {
		a[i] = (float)i; b[i] = (float)(2*i);
	}

	// Use the padded length when calling our AVX512 function
	Compute_C_AVX512(a, b, c, NT);

	// Check the result
	for (i = 0; i < N; i++) {
		error = error + c[i] - sqrtf(a[i]*a[i] + b[i]*b[i]);
	}
	printf("Error = %g\n", error);

	free(a); free(b); free(c);
	printf("Computation Complete\n");
	return 0;
}

void Compute_C_AVX512(float *x, float *y, float *z, int N) {
        int i;
        int N_AVX = N/16; // Integer number of AVX512 packed types.
        __m512 *AVX_a, *AVX_b, *AVX_c; // 512 bit packed type arrays
        __m512 AVX_tmp;                // 512 bit single tmp value
        // Map x, y, z onto these
        AVX_a = (__m512*)x; AVX_b = (__m512*)y; AVX_c = (__m512*)z;
        // Compute result for each packed type
        for (i = 0; i < N_AVX; i++) {
                AVX_tmp = AVX_a[i]*AVX_a[i] + AVX_b[i]*AVX_b[i];
                AVX_c[i] = _mm512_sqrt_ps(AVX_tmp);
        }
}

