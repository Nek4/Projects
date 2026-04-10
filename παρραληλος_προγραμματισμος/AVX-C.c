#include <immintrin.h>
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
    gettimeofday(&tp, NULL);
    *wct = (double)(tp.tv_sec + tp.tv_usec / 1000000.0);
}

int main() {
    double ts, te;
    float *a, *b;


    a = (float *)malloc(N * N * sizeof(float));
    b = (float *)malloc(N * N * sizeof(float));

    if (a == NULL || b == NULL) {
        printf("alloc error!\n");
        exit(1);
    }

    for (int i = 0; i < N * N; i++) {
        a[i] = (float)(i + 1);
        b[i] = 0.0f;
    }

    __m256 w1 = _mm256_set1_ps(W1);
    __m256 w2 = _mm256_set1_ps(W2);
    __m256 w3 = _mm256_set1_ps(W3);
    __m256 w4 = _mm256_set1_ps(W4);
    __m256 w5 = _mm256_set1_ps(W5);

    get_walltime(&ts);

    for (int k = 0; k < R; k++) {
        for (int i = 1; i < N - 1; i++) {
            int j;

            for (j = 1; j <= N - 9; j += 8) {
                __m256 center = _mm256_load_ps(&a[i * N + j]);
                __m256 top    = _mm256_load_ps(&a[(i - 1) * N + j]);
                __m256 bottom = _mm256_load_ps(&a[(i + 1) * N + j]);
                __m256 left   = _mm256_load_ps(&a[i * N + (j - 1)]);
                __m256 right  = _mm256_load_ps(&a[i * N + (j + 1)]);

                __m256 res = _mm256_mul_ps(center, w1);
                res = _mm256_add_ps(res, _mm256_mul_ps(top, w2));
                res = _mm256_add_ps(res, _mm256_mul_ps(bottom, w3));
                res = _mm256_add_ps(res, _mm256_mul_ps(left, w4));
                res = _mm256_add_ps(res, _mm256_mul_ps(right, w5));

                _mm256_store_ps(&b[i * N + j], res);
            }

            for (; j < N - 1; j++) {
                b[i * N + j] =
                    W1 * a[i * N + j] +
                    W2 * a[(i - 1) * N + j] +
                    W3 * a[(i + 1) * N + j] +
                    W4 * a[i * N + (j - 1)] +
                    W5 * a[i * N + (j + 1)];
            }
        }
    }

    get_walltime(&te);

    float check = 0.0f;
    for (int i = 0; i < N * N; i++) {
        check += b[i];
    }

    printf("check = %f\n", check);
    printf("time = %f sec\n", te - ts);

    free(a);
    free(b);

    return 0;
}