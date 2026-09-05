/* Direct libjpeg cross-check of the StegSeek seed claim.
 * Replicates JpegFile.cc (component order, block row-major, icoeff 0..63,
 * nonzero-only sample list) using the actual C library StegSeek links,
 * then computes the first N vertex bits (magic etc.) with the Cracker.cc
 * LCG selector at a given seed.
 *
 * usage: crosscheck <file.jpg> <hexseed> [nbits]
 * prints: numSamples + extracted bits LSB-first (hex, 24 bits per group)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <setjmp.h>
#include "jpegmini.h"

#define MAXN 20000000

static unsigned char *evs;
static long nsamples = 0;

struct my_error_mgr {
    struct jpeg_error_mgr pub;
    jmp_buf setjmp_buffer;
    char msg[JMSG_LENGTH_MAX];
};

static void my_error_exit(j_common_ptr cinfo) {
    struct my_error_mgr *m = (struct my_error_mgr *)cinfo->err;
    (*cinfo->err->format_message)(cinfo, m->msg);
    longjmp(m->setjmp_buffer, 1);
}

static void my_emit(j_common_ptr cinfo, int msg_level) { (void)cinfo; (void)msg_level; }

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s file seed [nbits]\n", argv[0]); return 2; }
    const char *fn = argv[1];
    unsigned long seed0 = strtoul(argv[2], NULL, 16);
    int nbits = argc > 3 ? atoi(argv[3]) : 24;

    struct jpeg_decompress_struct cinfo;
    struct my_error_mgr jerr;
    FILE *f = fopen(fn, "rb");
    if (!f) { perror("fopen"); return 1; }
    cinfo.err = jpeg_std_error(&jerr.pub);
    jerr.pub.error_exit = my_error_exit;
    jerr.pub.emit_message = my_emit;
    if (setjmp(jerr.setjmp_buffer)) {
        fprintf(stderr, "JPEG error: %s\n", jerr.msg);
        fclose(f);
        return 1;
    }
    jpeg_CreateDecompress(&cinfo, JPEG_LIB_VERSION, sizeof(cinfo));
    jpeg_stdio_src(&cinfo, f);
    jpeg_read_header(&cinfo, TRUE);
    printf("libjpeg: %dx%d num_components=%d\n", cinfo.image_width,
           cinfo.image_height, cinfo.num_components);
    JBLOCKIMAGE dct = jpeg_read_coefficients(&cinfo);

    evs = (unsigned char *)malloc(MAXN);
    unsigned int maxv = 0, maxh = 0;
    for (int i = 0; i < cinfo.num_components; i++) {
        if (cinfo.comp_info[i].v_samp_factor > maxv) maxv = cinfo.comp_info[i].v_samp_factor;
        if (cinfo.comp_info[i].h_samp_factor > maxh) maxh = cinfo.comp_info[i].h_samp_factor;
    }
    /* JpegFile.cc: HeightInBlocks = div_roundup(image_height * v_samp, 8*maxv) */
    for (int icomp = 0; icomp < cinfo.num_components; icomp++) {
        unsigned int hb = (cinfo.image_height * cinfo.comp_info[icomp].v_samp_factor
                           + 8 * maxv - 1) / (8 * maxv);
        unsigned int wb = (cinfo.image_width * cinfo.comp_info[icomp].h_samp_factor
                           + 8 * maxh - 1) / (8 * maxh);
        /* JpegFile.cc pattern: access_virt_barray one row at a time */
        for (unsigned int currow = 0; currow < hb; currow++) {
            JBLOCKARRAY arr = (cinfo.mem->access_virt_barray)((j_common_ptr)&cinfo,
                                                              (jvirt_barray_ptr)dct[icomp],
                                                              currow, 1, FALSE);
            for (unsigned int col = 0; col < wb; col++) {
                JCOEF *blk = arr[0][col];
                for (int i = 0; i < 64; i++) {
                    JCOEF c = blk[i];
                    if (c != 0) {
                        if (nsamples >= MAXN) { fprintf(stderr, "overflow\n"); return 1; }
                        evs[nsamples++] = (unsigned char)((c < 0 ? -c : c) & 1);
                    }
                }
            }
        }
    }
    printf("numSamples=%ld\n", nsamples);

    /* Cracker.cc selection: 3 samples per vertex, LCG A=1367208549 C=1 */
    unsigned long seed = seed0;
    long sv_idx = 0;
    unsigned long acc = 0;
    int accb = 0;
    for (int b = 0; b < nbits; b++) {
        int ev = 0;
        for (int p = 0; p < 3; p++) {
            seed = (seed * 1367208549UL + 1UL) & 0xFFFFFFFFUL; /* UWORD32 wrap */
            double t = (double)seed / 4294967296.0;
            long valIdx = sv_idx + (long)(t * (double)(nsamples - sv_idx));
            if (valIdx < 0 || valIdx >= nsamples) {
                fprintf(stderr, "valIdx out of range at pick %ld\n", sv_idx);
                return 1;
            }
            ev += evs[valIdx];
            sv_idx++;
        }
        acc |= (unsigned long)(ev % 2) << b;
        if (b % 24 == 23) {
            printf("bits %d..%d: 0x%06lx\n", b - 23, b, acc);
            acc = 0;
        }
    }
    return 0;
}
