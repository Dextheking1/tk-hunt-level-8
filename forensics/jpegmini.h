/* Minimal ABI-compatible subset of libjpeg(-turbo) 2.1.5 (JPEG_LIB_VERSION 70)
 * for crosscheck.c. Struct layouts transcribed from jpeglib.h tag 2.1.5.
 * The library validates structsize at jpeg_CreateDecompress time, so a layout
 * error is detected (JERR_VERSION_MISMATCH) rather than silent.
 */
#ifndef JPEGMINI_H
#define JPEGMINI_H

#include <stdio.h>
#include <stddef.h>

#define DCTSIZE   8
#define DCTSIZE2  64
#define NUM_QUANT_TBLS  4
#define NUM_HUFF_TBLS   4
#define NUM_ARITH_TBLS  16
#define MAX_COMPS_IN_SCAN 4
#define C_MAX_BLOCKS_IN_MCU 10
#define D_MAX_BLOCKS_IN_MCU 10
#define JPEG_LIB_VERSION 62  /* installed .so self-reports 62 */
#ifndef TRUE
#define TRUE    1
#define FALSE   0
#endif
/* IJG classic: typedef int boolean (HAVE_BOOLEAN in jconfig) */
typedef int boolean;

typedef unsigned char  UINT8;
typedef unsigned short UINT16;
typedef UINT8          JOCTET;
typedef unsigned char  JSAMPLE;
typedef short          JCOEF;
typedef unsigned int   JDIMENSION;   /* try int-sized first; library check guards */

typedef JSAMPLE *JSAMPROW;
typedef JSAMPROW *JSAMPARRAY;
typedef JCOEF JBLOCK[DCTSIZE2];
typedef JBLOCK *JBLOCKROW;
typedef JBLOCKROW *JBLOCKARRAY;
typedef JBLOCKARRAY *JBLOCKIMAGE;

typedef struct jpeg_error_mgr *j_error_ptr;
typedef struct jpeg_common_struct *j_common_ptr;
typedef struct jpeg_compress_struct *j_compress_ptr;
typedef struct jpeg_decompress_struct *j_decompress_ptr;

typedef struct {
  UINT16 quantval[DCTSIZE2];
  boolean sent_table;
} JQUANT_TBL;

typedef struct {
  UINT8 bits[17];
  UINT8 huffval[256];
  boolean sent_table;
} JHUFF_TBL;

typedef struct {
  int component_id;
  int component_index;
  int h_samp_factor;
  int v_samp_factor;
  int quant_tbl_no;
  int dc_tbl_no;
  int ac_tbl_no;
  JDIMENSION width_in_blocks;
  JDIMENSION height_in_blocks;
  int DCT_scaled_size;   /* JPEG_LIB_VERSION < 70 */
  JDIMENSION downsampled_width;
  JDIMENSION downsampled_height;
  boolean component_needed;
  int MCU_width;
  int MCU_height;
  int MCU_blocks;
  int MCU_sample_width;
  int last_col_width;
  int last_row_height;
  JQUANT_TBL *quant_table;
  void *dct_table;
} jpeg_component_info;

typedef struct jpeg_marker_struct *jpeg_saved_marker_ptr;
struct jpeg_marker_struct {
  jpeg_saved_marker_ptr next;
  UINT8 marker;
  unsigned int original_length;
  unsigned int data_length;
  JOCTET *data;
};

typedef enum { JCS_UNKNOWN, JCS_GRAYSCALE, JCS_RGB, JCS_YCbCr, JCS_CMYK,
               JCS_YCCK, JCS_EXT_RGB, JCS_EXT_RGBX, JCS_EXT_BGR, JCS_EXT_BGRX,
               JCS_EXT_XBGR, JCS_EXT_XRGB, JCS_EXT_RGBA, JCS_EXT_BGRA,
               JCS_EXT_ABGR, JCS_EXT_ARGB, JCS_RGB565 } J_COLOR_SPACE;

typedef enum { JDCT_ISLOW, JDCT_IFAST, JDCT_FLOAT } J_DCT_METHOD;
typedef enum { JDITHER_NONE, JDITHER_ORDERED, JDITHER_FS } J_DITHER_MODE;

#define jpeg_common_fields \
  struct jpeg_error_mgr *err; \
  struct jpeg_memory_mgr *mem; \
  struct jpeg_progress_mgr *progress; \
  void *client_data; \
  boolean is_decompressor; \
  int global_state

struct jpeg_common_struct {
  jpeg_common_fields;
};

struct jpeg_decompress_struct {
  jpeg_common_fields;

  struct jpeg_source_mgr *src;

  JDIMENSION image_width;
  JDIMENSION image_height;
  int num_components;
  J_COLOR_SPACE jpeg_color_space;

  J_COLOR_SPACE out_color_space;
  unsigned int scale_num, scale_denom;
  double output_gamma;
  boolean buffered_image;
  boolean raw_data_out;
  J_DCT_METHOD dct_method;
  boolean do_fancy_upsampling;
  boolean do_block_smoothing;
  boolean quantize_colors;
  J_DITHER_MODE dither_mode;
  boolean two_pass_quantize;
  int desired_number_of_colors;
  boolean enable_1pass_quant;
  boolean enable_external_quant;
  boolean enable_2pass_quant;

  JDIMENSION output_width;
  JDIMENSION output_height;
  int out_color_components;
  int output_components;
  int rec_outbuf_height;
  int actual_number_of_colors;
  JSAMPARRAY colormap;

  JDIMENSION output_scanline;
  int input_scan_number;
  JDIMENSION input_iMCU_row;
  int output_scan_number;
  JDIMENSION output_iMCU_row;
  int (*coef_bits)[DCTSIZE2];

  JQUANT_TBL *quant_tbl_ptrs[NUM_QUANT_TBLS];
  JHUFF_TBL *dc_huff_tbl_ptrs[NUM_HUFF_TBLS];
  JHUFF_TBL *ac_huff_tbl_ptrs[NUM_HUFF_TBLS];
  int data_precision;
  jpeg_component_info *comp_info;
  boolean progressive_mode;
  boolean arith_code;
  UINT8 arith_dc_L[NUM_ARITH_TBLS];
  UINT8 arith_dc_U[NUM_ARITH_TBLS];
  UINT8 arith_ac_K[NUM_ARITH_TBLS];
  unsigned int restart_interval;
  boolean saw_JFIF_marker;
  UINT8 JFIF_major_version;
  UINT8 JFIF_minor_version;
  UINT8 density_unit;
  UINT16 X_density;
  UINT16 Y_density;
  boolean saw_Adobe_marker;
  UINT8 Adobe_transform;
  boolean CCIR601_sampling;
  jpeg_saved_marker_ptr marker_list;

  int max_h_samp_factor;
  int max_v_samp_factor;
  int min_DCT_scaled_size;   /* JPEG_LIB_VERSION < 70 */
  JDIMENSION total_iMCU_rows;
  JSAMPLE *sample_range_limit;

  int comps_in_scan;
  jpeg_component_info *cur_comp_info[MAX_COMPS_IN_SCAN];
  JDIMENSION MCUs_per_row;
  JDIMENSION MCU_rows_in_scan;
  int blocks_in_MCU;
  int MCU_membership[D_MAX_BLOCKS_IN_MCU];
  int Ss, Se, Ah, Al;
  int unread_marker;

  void *master;
  void *main;
  void *coef;
  void *post;
  void *inputctl;
  void *marker;
  void *entropy;
  void *idct;
  void *upsample;
  void *cconvert;
  void *cquantize;
};

struct jpeg_error_mgr {
  void (*error_exit) (j_common_ptr cinfo);
  void (*emit_message) (j_common_ptr cinfo, int msg_level);
  void (*output_message) (j_common_ptr cinfo);
  void (*format_message) (j_common_ptr cinfo, char *buffer);
#define JMSG_LENGTH_MAX  200
  void (*reset_error_mgr) (j_common_ptr cinfo);
  int msg_code;
#define JMSG_STR_PARM_MAX  80
  union {
    int i[8];
    char s[JMSG_STR_PARM_MAX];
  } msg_parm;
  int trace_level;
  long num_warnings;
  const char * const *jpeg_message_table;
  int last_jpeg_message;
  const char * const *addon_message_table;
  int first_addon_message;
  int last_addon_message;
};

typedef struct jvirt_sarray_control *jvirt_sarray_ptr;
typedef struct jvirt_barray_control *jvirt_barray_ptr;

struct jpeg_memory_mgr {
  void *(*alloc_small) (j_common_ptr cinfo, int pool_id, size_t sizeofobject);
  void *(*alloc_large) (j_common_ptr cinfo, int pool_id, size_t sizeofobject);
  JSAMPARRAY (*alloc_sarray) (j_common_ptr cinfo, int pool_id,
                              JDIMENSION samplesperrow, JDIMENSION numrows);
  JBLOCKARRAY (*alloc_barray) (j_common_ptr cinfo, int pool_id,
                               JDIMENSION blocksperrow, JDIMENSION numrows);
  jvirt_sarray_ptr (*request_virt_sarray) (j_common_ptr cinfo, int pool_id,
                                           boolean pre_zero,
                                           JDIMENSION samplesperrow,
                                           JDIMENSION numrows,
                                           JDIMENSION maxaccess);
  jvirt_barray_ptr (*request_virt_barray) (j_common_ptr cinfo, int pool_id,
                                           boolean pre_zero,
                                           JDIMENSION blocksperrow,
                                           JDIMENSION numrows,
                                           JDIMENSION maxaccess);
  void (*realize_virt_arrays) (j_common_ptr cinfo);
  JSAMPARRAY (*access_virt_sarray) (j_common_ptr cinfo, jvirt_sarray_ptr ptr,
                                    JDIMENSION start_row, JDIMENSION num_rows,
                                    boolean writable);
  JBLOCKARRAY (*access_virt_barray) (j_common_ptr cinfo, jvirt_barray_ptr ptr,
                                     JDIMENSION start_row, JDIMENSION num_rows,
                                     boolean writable);
  void (*free_pool) (j_common_ptr cinfo, int pool_id);
  void (*self_destruct) (j_common_ptr cinfo);
  long max_memory_to_use;
  long max_alloc_chunk;
};

struct jpeg_source_mgr {
  const JOCTET *next_input_byte;
  size_t bytes_in_buffer;
  void (*init_source) (j_decompress_ptr cinfo);
  boolean (*fill_input_buffer) (j_decompress_ptr cinfo);
  void (*skip_input_data) (j_decompress_ptr cinfo, long num_bytes);
  boolean (*resync_to_restart) (j_decompress_ptr cinfo, int desired);
  void (*term_source) (j_decompress_ptr cinfo);
};

extern void jpeg_CreateDecompress(j_decompress_ptr cinfo, int version,
                                  size_t structsize);
extern struct jpeg_error_mgr *jpeg_std_error(struct jpeg_error_mgr *err);
extern void jpeg_stdio_src(j_decompress_ptr cinfo, FILE *infile);
extern boolean jpeg_read_header(j_decompress_ptr cinfo, boolean require_metadata);
extern JBLOCKIMAGE jpeg_read_coefficients(j_decompress_ptr cinfo);
extern void jpeg_abort_decompress(j_decompress_ptr cinfo);
extern void jpeg_destroy_decompress(j_decompress_ptr cinfo);

#endif
