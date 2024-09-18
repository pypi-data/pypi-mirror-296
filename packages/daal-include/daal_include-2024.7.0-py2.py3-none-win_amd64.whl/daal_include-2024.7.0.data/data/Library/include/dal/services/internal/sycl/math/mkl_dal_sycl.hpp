/*******************************************************************************
* Copyright 2014-2024 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/


#ifndef MKL_DAL_DPCPP_HPP
#define MKL_DAL_DPCPP_HPP

#include <sycl/sycl.hpp>
#include <cstdint>
#include <complex>

#define DLL_EXPORT

namespace oneapi {
namespace fpk {


enum class transpose : char {
    nontrans = 0,
    trans = 1,
    conjtrans = 3,
    N = 0,
    T = 1,
    C = 3
};

enum class uplo : char {
    upper = 0,
    lower = 1,
    U = 0,
    L = 1
};

enum class diag : char {
    nonunit = 0,
    unit = 1,
    N = 0,
    U = 1
};

enum class side : char {
    left = 0,
    right = 1,
    L = 0,
    R = 1
};

enum class offset : char {
    row = 0,
    column = 1,
    fix = 2,
    R = 0,
    C = 1,
    F = 2
};

enum class job : char {
    novec = 0,
    vec = 1,
    updatevec = 2,
    allvec = 3,
    somevec = 4,
    overwritevec = 5,
    N = 0,
    V = 1,
    U = 2,
    A = 3,
    S = 4,
    O = 5
};

enum class jobsvd : char {
    novec = 0,
    vectors = 1,
    vectorsina = 2,
    somevec = 3,
    N = 0,
    A = 1,
    O = 2,
    S = 3
};

enum class vector : char {
    q = 0,
    p = 1,
    none = 2,
    both = 3,
    Q = 0,
    P = 1,
    N = 2,
    V = 3
};

enum class index_base : char {
    zero = 0,
    one  = 1,
};

enum class layout : char {
    row_major = 0,
    col_major = 1,
    R = 0,
    C = 1,
};

using bfloat16 = sycl::ext::oneapi::bfloat16;

template <typename T>
class value_or_pointer {
    T value_;
    const T *ptr_;

public:
    // Constructor from value. Accepts not only type T but anything convertible to T.
    template <typename U, std::enable_if_t<std::is_convertible_v<U, T>, int> = 0>
    value_or_pointer(U value) : value_(value), ptr_(nullptr) {}

    // Constructor from pointer, assumed to be device-accessible.
    value_or_pointer(const T *ptr): value_(T(0)), ptr_(ptr) {}

    bool fixed() const {
        return ptr_ == nullptr;
    }

    T get_fixed_value() const {
        return value_;
    }

    const T* get_pointer() const {
        return ptr_;
    }

    T get() const {
        return ptr_ ? *ptr_ : value_;
    }

    void make_device_accessible(sycl::queue& queue) {
        if (!fixed() && sycl::get_pointer_type(ptr_, queue.get_context()) == sycl::usm::alloc::unknown) {
            *this = *ptr_;
        }
    }
};


/* APIs */



namespace blas {

enum class compute_mode : std::uint64_t {
    unset            = 0x0,
    float_to_bf16    = 0x1,
    float_to_bf16x2  = 0x2,
    float_to_bf16x3  = 0x4,
    float_to_tf32    = 0x10,
    complex_3m       = 0x10000,
    any              = 0xFFFFFFFF,
    standard         = 0x2000000000000000,
    prefer_alternate = 0x4000000000000000,
    force_alternate  = 0x8000000000000000,
};

static inline compute_mode operator|(compute_mode m1, compute_mode m2)
{
    return static_cast<compute_mode>(static_cast<std::uint64_t>(m1) | static_cast<std::uint64_t>(m2));
}

static inline compute_mode operator|=(compute_mode &m1, compute_mode m2)
{
    m1 = m1 | m2;
    return m1;
}

inline namespace column_major {

#define FPK_DPCPP_DECLARE_BUF_GEMM(Ta, Tb, Tc, Ts) \
DLL_EXPORT void gemm(sycl::queue &queue, transpose transa, transpose transb, \
                     std::int64_t m, std::int64_t n, std::int64_t k, \
                     Ts alpha, sycl::buffer<Ta, 1> &a, std::int64_t lda, \
                     sycl::buffer<Tb, 1> &b, std::int64_t ldb, \
                     Ts beta, sycl::buffer<Tc, 1> &c, std::int64_t ldc, \
                     compute_mode mode = compute_mode::standard);

FPK_DPCPP_DECLARE_BUF_GEMM(float, float, float, float)
FPK_DPCPP_DECLARE_BUF_GEMM(double, double, double, double)
FPK_DPCPP_DECLARE_BUF_GEMM(bfloat16, bfloat16, float, float)

#undef FPK_DPCPP_DECLARE_BUF_GEMM

#define FPK_DPCPP_DECLARE_BUF_SYRK(T) \
DLL_EXPORT void syrk(sycl::queue &queue, uplo upper_lower, transpose trans, std::int64_t n, std::int64_t k, \
              T alpha, sycl::buffer<T, 1> &a, std::int64_t lda, \
              T beta, sycl::buffer<T, 1> &c, std::int64_t ldc, \
              compute_mode mode = compute_mode::standard);

FPK_DPCPP_DECLARE_BUF_SYRK(float)
FPK_DPCPP_DECLARE_BUF_SYRK(double)

#undef FPK_DPCPP_DECLARE_BUF_SYRK

#define FPK_DPCPP_DECLARE_BUF_TRSM(T) \
DLL_EXPORT void trsm(sycl::queue &queue, side left_right, uplo upper_lower, transpose trans, diag unit_diag, \
              std::int64_t m, std::int64_t n, \
              T alpha, sycl::buffer<T, 1> &a, std::int64_t lda, \
              sycl::buffer<T, 1> &b, std::int64_t ldb, \
              compute_mode mode = compute_mode::standard);

FPK_DPCPP_DECLARE_BUF_TRSM(float)
FPK_DPCPP_DECLARE_BUF_TRSM(double)

#undef FPK_DPCPP_DECLARE_BUF_TRSM

#define FPK_DPCPP_DECLARE_BUF_GEMV(T) \
DLL_EXPORT void gemv(sycl::queue &queue, transpose trans, std::int64_t m, std::int64_t n, T alpha, \
              sycl::buffer<T, 1> &a, std::int64_t lda, \
              sycl::buffer<T, 1> &x, std::int64_t incx, T beta, \
              sycl::buffer<T, 1> &y, std::int64_t incy);

FPK_DPCPP_DECLARE_BUF_GEMV(float)
FPK_DPCPP_DECLARE_BUF_GEMV(double)

#undef FPK_DPCPP_DECLARE_BUF_GEMV

#define FPK_DPCPP_DECLARE_BUF_AXPY(T) \
DLL_EXPORT void axpy(sycl::queue &queue, std::int64_t n, T alpha, sycl::buffer<T, 1> &x, std::int64_t incx, sycl::buffer<T, 1> &y, std::int64_t incy);

FPK_DPCPP_DECLARE_BUF_AXPY(float)
FPK_DPCPP_DECLARE_BUF_AXPY(double)

#undef FPK_DPCPP_DECLARE_BUF_AXPY

#define FPK_DPCPP_DECLARE_GEMM(Ta, Tb, Tc, Ts) \
DLL_EXPORT sycl::event gemm(sycl::queue &queue, transpose transa, transpose transb, \
                                std::int64_t m, std::int64_t n, std::int64_t k, \
                                value_or_pointer<Ts> alpha, const Ta *a, std::int64_t lda, \
                                const Tb *b, std::int64_t ldb, \
                                value_or_pointer<Ts> beta, Tc *c, std::int64_t ldc, \
                                compute_mode mode, const std::vector<sycl::event> &dependencies = {}); \
static inline sycl::event gemm(sycl::queue &queue, transpose transa, transpose transb, \
                                   std::int64_t m, std::int64_t n, std::int64_t k, \
                                   value_or_pointer<Ts> alpha, const Ta *a, std::int64_t lda, \
                                   const Tb *b, std::int64_t ldb, \
                                   value_or_pointer<Ts> beta, Tc *c, std::int64_t ldc, \
                                   const std::vector<sycl::event> &dependencies = {}) \
{ \
    return gemm(queue, transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc, compute_mode::standard, dependencies); \
}

FPK_DPCPP_DECLARE_GEMM(float, float, float, float)
FPK_DPCPP_DECLARE_GEMM(double, double, double, double)
FPK_DPCPP_DECLARE_GEMM(bfloat16, bfloat16, float, float)

#undef FPK_DPCPP_DECLARE_GEMM

#define FPK_DPCPP_DECLARE_SYRK(T) \
DLL_EXPORT sycl::event syrk(sycl::queue &queue, uplo upper_lower, transpose trans, std::int64_t n, std::int64_t k, \
              value_or_pointer<T> alpha, const T *a, std::int64_t lda, \
              value_or_pointer<T> beta, T *c, std::int64_t ldc, \
              compute_mode mode, const std::vector<sycl::event> &dependencies = {}); \
static inline sycl::event syrk(sycl::queue &queue, uplo upper_lower, transpose trans, std::int64_t n, std::int64_t k, \
              T alpha, const T *a, std::int64_t lda, \
              T beta, T *c, std::int64_t ldc, \
              const std::vector<sycl::event> &dependencies = {}) \
{ \
    return syrk(queue, upper_lower, trans, n, k, alpha, a, lda, beta, c, ldc, compute_mode::standard, dependencies); \
}

FPK_DPCPP_DECLARE_SYRK(float)
FPK_DPCPP_DECLARE_SYRK(double)

#undef FPK_DPCPP_DECLARE_SYRK

#define FPK_DPCPP_DECLARE_TRSM(T) \
DLL_EXPORT sycl::event trsm(sycl::queue &queue, side left_right, uplo upper_lower, transpose trans, diag unit_diag, \
              std::int64_t m, std::int64_t n, \
              value_or_pointer<T> alpha, const T *a, std::int64_t lda, \
              T *b, std::int64_t ldb, \
              compute_mode mode, const std::vector<sycl::event> &dependencies = {}); \
static inline sycl::event trsm(sycl::queue &queue, side left_right, uplo upper_lower, transpose trans, diag unit_diag, \
              std::int64_t m, std::int64_t n, \
              value_or_pointer<T> alpha, const T *a, std::int64_t lda, \
              T *b, std::int64_t ldb, \
              const std::vector<sycl::event> &dependencies = {}) \
{ \
    return trsm(queue, left_right, upper_lower, trans, unit_diag, m, n, alpha, a, lda, b, ldb, compute_mode::standard, dependencies); \
}

FPK_DPCPP_DECLARE_TRSM(float)
FPK_DPCPP_DECLARE_TRSM(double)

#undef FPK_DPCPP_DECLARE_TRSM

#define FPK_DPCPP_DECLARE_GEMV(T) \
DLL_EXPORT sycl::event gemv(sycl::queue &queue, transpose trans, std::int64_t m, std::int64_t n, value_or_pointer<T> alpha, \
              const T *a, std::int64_t lda, \
              const T *x, std::int64_t incx, value_or_pointer<T> beta, \
              T *y, std::int64_t incy, const std::vector<sycl::event> &dependencies = {});

FPK_DPCPP_DECLARE_GEMV(float)
FPK_DPCPP_DECLARE_GEMV(double)

#undef FPK_DPCPP_DECLARE_GEMV

#define FPK_DPCPP_DECLARE_AXPY(T) \
DLL_EXPORT sycl::event axpy(sycl::queue &queue, std::int64_t n, value_or_pointer<T> alpha, const T *x, std::int64_t incx, T *y, std::int64_t incy, const std::vector<sycl::event> &dependencies = {});

FPK_DPCPP_DECLARE_AXPY(float)
FPK_DPCPP_DECLARE_AXPY(double)

#undef FPK_DPCPP_DECLARE_AXPY

#define FPK_DPCPP_DECLARE_IMATCOPY(T) \
DLL_EXPORT sycl::event imatcopy(sycl::queue &queue, transpose trans, \
                                std::int64_t m, std::int64_t n, value_or_pointer<T> alpha, T *ab, \
                                std::int64_t lda, std::int64_t ldb, \
                                const std::vector<sycl::event> &dependencies = {});

FPK_DPCPP_DECLARE_IMATCOPY(float)
FPK_DPCPP_DECLARE_IMATCOPY(double)

#undef FPK_DPCPP_DECLARE_IMATCOPY

#define FPK_DPCPP_DECLARE_OMATCOPY(T) \
DLL_EXPORT sycl::event omatcopy(sycl::queue &queue, transpose trans, \
                                std::int64_t m, std::int64_t n, value_or_pointer<T> alpha, const T *a, \
                                std::int64_t lda, T *b, std::int64_t ldb, \
                                const std::vector<sycl::event> &dependencies = {});

FPK_DPCPP_DECLARE_OMATCOPY(float)
FPK_DPCPP_DECLARE_OMATCOPY(double)

#undef FPK_DPCPP_DECLARE_OMATCOPY

#define FPK_DPCPP_DECLARE_BUF_IMATCOPY(T) \
DLL_EXPORT void imatcopy(sycl::queue &queue, transpose trans, \
                         std::int64_t m, std::int64_t n, \
                         T alpha, sycl::buffer<T, 1> &ab, \
                         std::int64_t lda, std::int64_t ldb);

FPK_DPCPP_DECLARE_BUF_IMATCOPY(float)
FPK_DPCPP_DECLARE_BUF_IMATCOPY(double)

#undef FPK_DPCPP_DECLARE_BUF_IMATCOPY

#define FPK_DPCPP_DECLARE_BUF_OMATCOPY(T) \
DLL_EXPORT void omatcopy(sycl::queue &queue, transpose trans, \
                         std::int64_t m, std::int64_t n, \
                         T alpha, sycl::buffer<T, 1> &a, \
                         std::int64_t lda, sycl::buffer<T, 1> &b, std::int64_t ldb);

FPK_DPCPP_DECLARE_BUF_OMATCOPY(float)
FPK_DPCPP_DECLARE_BUF_OMATCOPY(double)

#undef FPK_DPCPP_DECLARE_BUF_OMATCOPY

} // namespace column_major
} // namespace blas


class exception : public std::exception {
    std::string msg_;
    public:
        exception(const std::string &domain, const std::string &function, const std::string &info = "") : std::exception() {
            msg_ = std::string("FPK: ") + domain + "/" + function + ((info.length() != 0) ? (": " + info) : "");
        }

        const char* what() const noexcept {
            return msg_.c_str();
        }
};

class unimplemented : public oneapi::fpk::exception {
    public:
        unimplemented(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "function is not implemented "+info) {
        }
};

class invalid_argument : public oneapi::fpk::exception {
    public:
        invalid_argument(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "invalid argument "+info) {
        }
};
class computation_error : public oneapi::fpk::exception {
    public:
        computation_error(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "computation error"+((info.length() != 0) ? (": "+info) : "")) {
        }
};

class batch_error : public oneapi::fpk::exception {
    public:
        batch_error(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "batch error"+((info.length() != 0) ? (": "+info) : "")) {
        }
};

namespace lapack {

class exception
{
public:
    exception(fpk::exception *_ex, std::int64_t info, std::int64_t detail = 0) : _info(info), _detail(detail), _ex(_ex) {}
    std::int64_t info()   const { return _info; }
    std::int64_t detail() const { return _detail; }
    const char*  what()   const { return _ex->what(); }
private:
    std::int64_t   _info;
    std::int64_t   _detail;
    fpk::exception *_ex;
};

class computation_error : public oneapi::fpk::computation_error, public oneapi::fpk::lapack::exception
{
public:
    computation_error(const std::string &function, const std::string &info, std::int64_t code)
        : oneapi::fpk::computation_error("LAPACK", function, info), oneapi::fpk::lapack::exception(this, code) {}
    using oneapi::fpk::computation_error::what;
};

class batch_error : public oneapi::fpk::batch_error, public oneapi::fpk::lapack::exception
{
public:
    batch_error(const std::string &function, const std::string &info, std::int64_t num_errors, std::vector<std::int64_t> ids = {}, std::vector<std::exception_ptr> exceptions = {})
            : oneapi::fpk::batch_error("LAPACK", function, info), oneapi::fpk::lapack::exception(this, num_errors), _ids(ids), _exceptions(exceptions) {}
    using oneapi::fpk::batch_error::what;
    const std::vector<std::int64_t>& ids() const { return _ids; }
    const std::vector<std::exception_ptr>& exceptions() const { return _exceptions; }
private:
    std::vector<std::int64_t> _ids;
    std::vector<std::exception_ptr> _exceptions;
};

class invalid_argument : public oneapi::fpk::invalid_argument, public oneapi::fpk::lapack::exception
{
public:
    invalid_argument(const std::string &function, const std::string &info, std::int64_t arg_position = 0, std::int64_t detail = 0)
        : oneapi::fpk::invalid_argument("LAPACK", function, info), oneapi::fpk::lapack::exception(this, arg_position, detail) {}
    using oneapi::fpk::invalid_argument::what;
};

class unimplemented : public oneapi::fpk::unimplemented, public oneapi::fpk::lapack::exception
{
public:
    unimplemented(const std::string &function, const std::string &info = "")
        : oneapi::fpk::unimplemented("LAPACK", function, info), oneapi::fpk::lapack::exception(this, -1) {}
    using oneapi::fpk::unimplemented::what;
};

void potrf(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, sycl::buffer<float>  &a, std::int64_t lda, sycl::buffer<float>  &scratchpad, std::int64_t scratchpad_size);
void potrf(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, sycl::buffer<double> &a, std::int64_t lda, sycl::buffer<double> &scratchpad, std::int64_t scratchpad_size);
sycl::event potrf(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, float  *a, std::int64_t lda, float  *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &events = {});
sycl::event potrf(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, double *a, std::int64_t lda, double *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &events = {});
template <typename data_t, void* = nullptr>
std::int64_t potrf_scratchpad_size(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t lda);

void potrs(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, sycl::buffer<float>  &a, std::int64_t lda, sycl::buffer<float>  &b, std::int64_t ldb, sycl::buffer<float>  &scratchpad, std::int64_t scratchpad_size);
void potrs(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, sycl::buffer<double> &a, std::int64_t lda, sycl::buffer<double> &b, std::int64_t ldb, sycl::buffer<double> &scratchpad, std::int64_t scratchpad_size);
sycl::event potrs(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, float  *a, std::int64_t lda, float  *b, std::int64_t ldb, float  *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &events = {});
sycl::event potrs(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, double *a, std::int64_t lda, double *b, std::int64_t ldb, double *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &events = {});
template <typename data_t, void* = nullptr>
std::int64_t potrs_scratchpad_size(sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, std::int64_t lda, std::int64_t ldb);

void syevd(sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, sycl::buffer<float>  &a, std::int64_t lda, sycl::buffer<float>  &w, sycl::buffer<float>  &scratchpad, std::int64_t scratchpad_size);
void syevd(sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, sycl::buffer<double> &a, std::int64_t lda, sycl::buffer<double> &w, sycl::buffer<double> &scratchpad, std::int64_t scratchpad_size);
sycl::event syevd(sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, float *a, std::int64_t lda, float *w, float *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &event_list = {});
sycl::event syevd(sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, double *a, std::int64_t lda, double *w, double *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &event_list = {});
template <typename data_t, void* = nullptr>
std::int64_t syevd_scratchpad_size(sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t lda);

void gesvd(sycl::queue &queue, oneapi::fpk::jobsvd jobu, oneapi::fpk::jobsvd jobvt, std::int64_t m, std::int64_t n, sycl::buffer<float> &a, std::int64_t lda, sycl::buffer<float> &s, sycl::buffer<float> &u, std::int64_t ldu, sycl::buffer<float> &vt, std::int64_t ldvt, sycl::buffer<float> &scratchpad, std::int64_t scratchpad_size);
void gesvd(sycl::queue &queue, oneapi::fpk::jobsvd jobu, oneapi::fpk::jobsvd jobvt, std::int64_t m, std::int64_t n, sycl::buffer<double> &a, std::int64_t lda, sycl::buffer<double> &s, sycl::buffer<double> &u, std::int64_t ldu, sycl::buffer<double> &vt, std::int64_t ldvt, sycl::buffer<double> &scratchpad, std::int64_t scratchpad_size);
sycl::event gesvd(sycl::queue &queue, oneapi::fpk::jobsvd jobu, oneapi::fpk::jobsvd jobvt, std::int64_t m, std::int64_t n, float *a, std::int64_t lda, float *s, float *u, std::int64_t ldu, float *vt, std::int64_t ldvt, float *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &event_list = {});
sycl::event gesvd(sycl::queue &queue, oneapi::fpk::jobsvd jobu, oneapi::fpk::jobsvd jobvt, std::int64_t m, std::int64_t n, double *a, std::int64_t lda, double *s, double *u, std::int64_t ldu, double *vt, std::int64_t ldvt, double *scratchpad, std::int64_t scratchpad_size, const std::vector<sycl::event> &event_list = {});
template <typename data_t, void* = nullptr>
std::int64_t gesvd_scratchpad_size(sycl::queue &queue, oneapi::fpk::jobsvd jobu, oneapi::fpk::jobsvd jobvt, std::int64_t m, std::int64_t n, std::int64_t lda, std::int64_t ldu, std::int64_t ldvt);

} // namespace lapack

namespace sparse {

struct matrix_handle;
typedef struct matrix_handle *matrix_handle_t;

DLL_EXPORT void init_matrix_handle(matrix_handle_t *handle);

// non-blocking version of release_matrix_handle, will schedule clean up of handle
// asychronously pending dependencies and return an event to track it
DLL_EXPORT sycl::event
release_matrix_handle(sycl::queue &queue,
                      matrix_handle_t *handle,
                      const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
//
// PROPERTY of matrix arrays/data. The property must be consistent with the
// data; this consistency is not verified and assumed to be true when provided
// by the user for performance reasons. If user-supplied data properties are
// inconsistent from actual matrix arrays/data, then applications may
// crash/hang/produce incorrect results.
enum class property : char {
    symmetric = 0,
    sorted    = 1,
};

DLL_EXPORT void set_matrix_property(matrix_handle_t handle, property property_value);

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_SET_CSR_DATA(IntType, FpType) \
    DLL_EXPORT sycl::event set_csr_data(sycl::queue &queue, \
                                        matrix_handle_t handle, \
                                        const IntType nrows, \
                                        const IntType ncols, \
                                        index_base index, \
                                        IntType *row_ptr, \
                                        IntType *col_ind, \
                                        FpType *val, \
                                        const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_SET_CSR_DATA(std::int32_t, float);
ONEFPK_DECLARE_SPARSE_SET_CSR_DATA(std::int32_t, double);
ONEFPK_DECLARE_SPARSE_SET_CSR_DATA(std::int64_t, float);
ONEFPK_DECLARE_SPARSE_SET_CSR_DATA(std::int64_t, double);

#undef ONEFPK_DECLARE_SPARSE_SET_CSR_DATA
/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_SET_COO_DATA(IntType, FpType) \
    DLL_EXPORT sycl::event set_coo_data(sycl::queue &queue, \
                                        matrix_handle_t handle, \
                                        const IntType nrows, \
                                        const IntType ncols, \
                                        const IntType nnz, \
                                        index_base index, \
                                        IntType *row_ind, \
                                        IntType *col_ind, \
                                        FpType *val, \
                                        const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_SET_COO_DATA(std::int32_t, float);
ONEFPK_DECLARE_SPARSE_SET_COO_DATA(std::int32_t, double);
ONEFPK_DECLARE_SPARSE_SET_COO_DATA(std::int64_t, float);
ONEFPK_DECLARE_SPARSE_SET_COO_DATA(std::int64_t, double);

#undef ONEFPK_DECLARE_SPARSE_SET_COO_DATA

/******************************************************************************/
//
// Types, Objects and APIs for Sparse Matrix * Sparse Matrix (matmat) multiplication
//

//
// Different VIEWS of matrix data (which may be different from the data itself)
// Views are different from the `enum class property` which describes the fixed
// property of data supplied to the matrix handle.
//
enum class matrix_view_descr : std::int32_t { general = 1 };

enum class matmat_request : std::int32_t {
    get_work_estimation_buf_size = 1,
    work_estimation = 2,

    get_compute_structure_buf_size = 3,
    compute_structure = 4,
    finalize_structure = 5,

    get_compute_buf_size = 6,
    compute = 7,
    get_nnz = 8,
    finalize = 9,
};

struct matmat_descr;
typedef matmat_descr *matmat_descr_t;

DLL_EXPORT void init_matmat_descr(matmat_descr_t *desc);
DLL_EXPORT void release_matmat_descr(matmat_descr_t *desc);

/******************************************************************************/
DLL_EXPORT sycl::event omatcopy(sycl::queue &queue,
                                transpose transpose_flag,
                                matrix_handle_t from_handle,
                                matrix_handle_t to_handle,
                                const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
DLL_EXPORT sycl::event sort_matrix(sycl::queue &queue,
                                   matrix_handle_t hMatrix,
                                   const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_UPDATE_DIAGONAL_VALUES(FpType) \
    DLL_EXPORT sycl::event update_diagonal_values(sycl::queue &queue, \
                                                  matrix_handle_t handle, \
                                                  std::int64_t length, \
                                                  const FpType *new_diag_values, \
                                                  const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_UPDATE_DIAGONAL_VALUES(float);
ONEFPK_DECLARE_SPARSE_UPDATE_DIAGONAL_VALUES(double);

#undef ONEFPK_DECLARE_SPARSE_UPDATE_DIAGONAL_VALUES

/******************************************************************************/
DLL_EXPORT sycl::event
optimize_gemv(sycl::queue &queue,
              transpose transpose_flag,
              matrix_handle_t handle,
              const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
DLL_EXPORT sycl::event
optimize_trmv(sycl::queue &queue,
              uplo uplo_flag,
              transpose transpose_flag,
              diag diag_val,
              matrix_handle_t handle,
              const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
DLL_EXPORT sycl::event
optimize_trsv(sycl::queue &queue,
              uplo uplo_flag,
              transpose transpose_flag,
              diag diag_val,
              matrix_handle_t handle,
              const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
DLL_EXPORT sycl::event
optimize_trsm(sycl::queue &queue,
              uplo uplo_val,
              transpose opA,
              diag diag_val,
              matrix_handle_t A,
              const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
DLL_EXPORT sycl::event
optimize_trsm(sycl::queue &queue,
              layout layout_val,
              uplo uplo_val,
              transpose opA,
              diag diag_val,
              matrix_handle_t A,
              const std::int64_t columns,
              const std::vector<sycl::event> &dependencies = {});

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_GEMV(FpType) \
    DLL_EXPORT sycl::event gemv(sycl::queue &queue, \
                                transpose transpose_flag, \
                                const FpType alpha, \
                                matrix_handle_t handle, \
                                const FpType *x, \
                                const FpType beta, \
                                FpType *y, \
                                const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_GEMV(float);
ONEFPK_DECLARE_SPARSE_GEMV(double);

#undef ONEFPK_DECLARE_SPARSE_GEMV

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_GEMVDOT(FpType) \
    DLL_EXPORT sycl::event gemvdot(sycl::queue &queue, \
                                   transpose transpose_flag, \
                                   const FpType alpha, \
                                   matrix_handle_t handle, \
                                   FpType *x, \
                                   const FpType beta, \
                                   FpType *y, \
                                   FpType *d, \
                                   const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_GEMVDOT(float);
ONEFPK_DECLARE_SPARSE_GEMVDOT(double);

#undef ONEFPK_DECLARE_SPARSE_GEMVDOT

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_SYMV(FpType) \
    DLL_EXPORT sycl::event symv(sycl::queue &queue, \
                                uplo uplo_flag, \
                                const FpType alpha, \
                                matrix_handle_t handle, \
                                FpType *x, \
                                const FpType beta, \
                                FpType *y, \
                                const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_SYMV(float);
ONEFPK_DECLARE_SPARSE_SYMV(double);

#undef ONEFPK_DECLARE_SPARSE_SYMV

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_TRMV(FpType) \
    DLL_EXPORT sycl::event trmv(sycl::queue &queue, \
                                uplo uplo_flag, \
                                transpose transpose_flag, \
                                diag diag_flag, \
                                const FpType alpha, \
                                matrix_handle_t handle, \
                                FpType *x, \
                                const FpType beta, \
                                FpType *y, \
                                const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_TRMV(float);
ONEFPK_DECLARE_SPARSE_TRMV(double);

#undef ONEFPK_DECLARE_SPARSE_TRMV

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_TRSV(FpType) \
    DLL_EXPORT sycl::event trsv(sycl::queue &queue, \
                                uplo uplo_val, \
                                transpose opA, \
                                diag diag_flag, \
                                const FpType alpha, \
                                matrix_handle_t handle, \
                                FpType *x, \
                                FpType *y, \
                                const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_TRSV(float);
ONEFPK_DECLARE_SPARSE_TRSV(double);

#undef ONEFPK_DECLARE_SPARSE_TRSV

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_GEMM(FpType) \
    DLL_EXPORT sycl::event gemm(sycl::queue &queue, \
                                layout dense_matrix_layout, \
                                transpose opA, \
                                transpose opB, \
                                const FpType alpha, \
                                matrix_handle_t handle, \
                                FpType *b, \
                                const std::int64_t columns, \
                                const std::int64_t ldb, \
                                const FpType beta, \
                                FpType *c, \
                                const std::int64_t ldc, \
                                const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_GEMM(float);
ONEFPK_DECLARE_SPARSE_GEMM(double);

#undef ONEFPK_DECLARE_SPARSE_GEMM

/******************************************************************************/
#define ONEFPK_DECLARE_SPARSE_TRSM(FpType) \
    DLL_EXPORT sycl::event trsm(sycl::queue &queue, \
                                layout layout_val, \
                                transpose opA, \
                                transpose opX, \
                                uplo uplo_val, \
                                diag diag_val, \
                                const FpType alpha, \
                                matrix_handle_t handle, \
                                const FpType *x, \
                                const std::int64_t columns, \
                                const std::int64_t ldx, \
                                FpType *y, \
                                const std::int64_t ldy, \
                                const std::vector<sycl::event> &dependencies = {})

ONEFPK_DECLARE_SPARSE_TRSM(float);
ONEFPK_DECLARE_SPARSE_TRSM(double);

#undef ONEFPK_DECLARE_SPARSE_TRSM

/******************************************************************************/
DLL_EXPORT void set_matmat_data(matmat_descr_t descr,
                                matrix_view_descr viewA,
                                transpose opA,
                                matrix_view_descr viewB,
                                transpose opB,
                                matrix_view_descr viewC);

DLL_EXPORT void get_matmat_data(matmat_descr_t descr,
                                matrix_view_descr &viewA,
                                transpose &opA,
                                matrix_view_descr &viewB,
                                transpose &opB,
                                matrix_view_descr &viewC);

DLL_EXPORT sycl::event matmat(sycl::queue &queue,
                              matrix_handle_t A,
                              matrix_handle_t B,
                              matrix_handle_t C,
                              sparse::matmat_request req,
                              sparse::matmat_descr_t descr,
                              std::int64_t *sizeTempBuffer,
                              void *tempBuffer,
                              const std::vector<sycl::event> &dependencies);

} // namespace sparse

namespace blas {
inline namespace column_major {


 } // namespace column_major
 } // namespace blas








/* end APIs */

} /* namespace fpk */
} /* namespace oneapi */

/* add Internal oneMKL Offset APIs */
#include "mkl_dal_blas_sycl.hpp"

#endif /*MKL_DAL_DPCPP_HPP*/
