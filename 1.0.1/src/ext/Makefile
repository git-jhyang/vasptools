
#LOC_IC	 = /opt/intel
#LOC_IC   = /APP/enhpc/compiler/intel/v11.7/256

FC	 = ifort
FCFLAGS  = 

LOC_MTST = ./mt_stream_f90-1.11

LIBNAME  = liblocfort

#=================================================================

SRC      = constants util vasp

SRC_MT   = mt_serial
#SRC_MTST = $(LOC_MTST)/mt_stream \
	   $(LOC_MTST)/f_jump_ahead_coeff/gf2xe \
	   $(LOC_MTST)/f_jump_ahead_coeff/f_get_coeff \
	   $(LOC_MTST)/mt_kind_defs

#=================================================================

OBJS      = $(addsuffix .o, ${SRC})
OBJS_MT   = $(addsuffix .o, ${SRC_MT})
#OBJS_MTST = $(addsuffix .o, ${SRC_MTST}) 

OBJS_ALL  = $(OBJS) $(OBJS_MT) #$(OBJS_MTST)

#=================================================================

constants.o : 
util.o 	    : constants.o
mt_serial.o : 
vasp.o      : constants.o util.o

#=================================================================

.PHONY: help all lfort mtst linc clean veryclean
.SUFFIXES: .f90 .o

help :
	#
	#    help      : print this help
	#    l4fortran : make library file '$(LIBNAME).a' for fortran
	#                should 'INCLUDE' paths '.' and './mtstream4py_f90'
	#    linc      : check '$(LIBNAME).a'
	#    clean     : remove created files
	#    veryclean : 'clean' with mt_stream created file
	#

all : mtst lfort

lfort : $(LIBNAME).a 

linc :
	ar t $(LIBNAME).a

#=======================================================================

$(LIBNAME).a : $(OBJS_ALL)
	ar src $@ $(OBJS_ALL)

#mtst : 
#	make -C $(LOC_MTST) all

%.o : %.f90
	$(FC) -c $(FCFLAGS) $<

clean :
	if [ -e $(LIBNAME).a ]; then rm -f $(LIBNAME).a; fi
	rm -f *.o *.mod 

veryclean: clean
	make -C $(LOC_MTST) clean
