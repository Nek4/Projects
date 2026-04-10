// benchmark template: computing the sum of an 2d array of doubles

// compile with: gcc -Wall -O2 array2d-sum.c -o array2d-sum -DN=1000 -DR=100
// check assembly output: gcc -Wall -O2 array2d-sum.c -S -DN=1000 -DR=100


#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#define W1 0.6f
#define W2 0.1f
#define W3 0.1f
#define W4 0.1f
#define W5 0.1f



void get_walltime(double *wct) {
  struct timeval tp;
  gettimeofday(&tp,NULL);
  *wct = (double)(tp.tv_sec+tp.tv_usec/1000000.0);
}


int main() {
float *a, *b;
double ts,te;
a = (float *)malloc(N*N*sizeof(float));
b = (float *)malloc(N*N*sizeof(float));

  // 1. allocate array
  a = (float *)malloc(N*N*sizeof(double)); 
  if (a==NULL) {
    printf("alloc error!\n");
    exit(1);
  }

  // 2. init array to 1..N
  for (int i=0; i<N*N; i++) {
    a[i] = (float)(i + 1);
    b[i] = 0.0f;
}

  // get starting time (double, seconds) 
  get_walltime(&ts);
  
  // 3. Workload
 for (int k=0; k<R; k++) {
    for (int i=1; i<N-1; i++) {
        for (int j=1; j<N-1; j++) {
            b[i*N + j] =
                W1 * a[i*N + j] +
                W2 * a[(i-1)*N + j] +
                W3 * a[(i+1)*N + j] +
                W4 * a[i*N + (j-1)] +
                W5 * a[i*N + (j+1)];
        }
    }
}


  // get ending time
  get_walltime(&te);
  
float check = 0.0f;
    for (int i = 0; i < N * N; i++) {
        check += b[i];
    }
  // 4. DO NOT remove this: the compiler will optimize by removing test loops!
  printf("sum = %f\n ",check);

  // compute avg array element accesses /sec (total R*N*N element accesses)
  printf("check = %f\n", check);
  printf("time = %f sec\n", te - ts);
  

  free(a);  
  free(b);
  return 0;
}
