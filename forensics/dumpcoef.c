/* Dump every DCT coefficient of every block in exact JpegFile.cc order:
   component order, block row-major (HeightInBlocks/WidthInBlocks), icoeff 0..63
   (natural order, as libjpeg stores blocks). int16 LE per coefficient. */
#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>
#include "jpegmini.h"
struct my_error_mgr { struct jpeg_error_mgr pub; jmp_buf jb; char msg[200]; };
static void ee(j_common_ptr c){ struct my_error_mgr *m=(struct my_error_mgr*)c->err; (*c->err->format_message)(c,m->msg); longjmp(m->jb,1);}
static void em(j_common_ptr c, int l){}
int main(int argc, char** argv){
    if (argc < 3) return 2;
    struct jpeg_decompress_struct cinfo;
    struct my_error_mgr jerr;
    FILE *f = fopen(argv[1], "rb");
    cinfo.err = jpeg_std_error(&jerr.pub);
    jerr.pub.error_exit = ee; jerr.pub.emit_message = em;
    if (setjmp(jerr.jb)) { fprintf(stderr, "ERR: %s\n", jerr.msg); return 1; }
    jpeg_CreateDecompress(&cinfo, 62, sizeof(cinfo));
    jpeg_stdio_src(&cinfo, f);
    jpeg_read_header(&cinfo, TRUE);
    JBLOCKIMAGE d = jpeg_read_coefficients(&cinfo);
    FILE *out = fopen(argv[2], "wb");
    unsigned int maxv = 0, maxh = 0;
    for (int i = 0; i < cinfo.num_components; i++) {
        if (cinfo.comp_info[i].v_samp_factor > maxv) maxv = cinfo.comp_info[i].v_samp_factor;
        if (cinfo.comp_info[i].h_samp_factor > maxh) maxh = cinfo.comp_info[i].h_samp_factor;
    }
    for (int icomp = 0; icomp < cinfo.num_components; icomp++) {
        unsigned int hb = (cinfo.image_height * cinfo.comp_info[icomp].v_samp_factor + 8*maxv - 1) / (8*maxv);
        unsigned int wb = (cinfo.image_width * cinfo.comp_info[icomp].h_samp_factor + 8*maxh - 1) / (8*maxh);
        for (unsigned int row = 0; row < hb; row++) {
            JBLOCKARRAY arr = (cinfo.mem->access_virt_barray)((j_common_ptr)&cinfo,
                                (jvirt_barray_ptr)d[icomp], row, 1, FALSE);
            for (unsigned int col = 0; col < wb; col++) {
                for (int i = 0; i < 64; i++) {
                    int16_t v = (int16_t)arr[0][col][i];
                    fwrite(&v, 2, 1, out);
                }
            }
        }
    }
    fclose(out);
    printf("dumped %d components\n", cinfo.num_components);
    return 0;
}
