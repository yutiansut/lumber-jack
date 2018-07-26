# -*- coding: utf-8 -*-

cimport numpy as np
from libcpp cimport bool
from libcpp.string cimport string
from .includes cimport DataPtr, DType

cdef extern from "./../rust/liblumberjack.h":

    DataPtr arange(int start, int stop, DType dtype)
    DataPtr sum(DataPtr ptr)
    DataPtr cumsum(DataPtr ptr)
    double  mean(DataPtr ptr)
    DataPtr multiply_by_scalar(DataPtr ptr, double scalar, bool inplace)
    DataPtr add_by_scalar(DataPtr ptr, double scalar, bool inplace)
    double  series_map(np.uint8_t *source_ptr, np.uint32_t source_len,
                       np.uint8_t *target_ptr, np.uint32_t target_len,
                       np.uint8_t *func_ptr,   np.uint32_t func_len)
    DataPtr astype(DataPtr ptr, DType dtype)