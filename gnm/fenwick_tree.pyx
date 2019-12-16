from libcpp.vector cimport vector

# distutils: language=c++

cdef extern from "fenwick_tree.h":
    cdef cppclass FenwickTree:
         FenwickTree() except +
         FenwickTree(int, double) except +
         int N, ntotal, offset
         double TotalSum
         vector[double] tree
         void SumTree()
         void Update(int, double)
         int Search(double)
         void ResetTree(double)


cdef class PyFenwickTree:
    cdef FenwickTree c_tree  # Hold a C++ instance which we're wrapping

    def __cinit__(self, int N, double InitialRate):
        self.c_tree = FenwickTree(N, InitialRate)

    def SumTree(self):
        return self.c_tree.SumTree()

    def Update(self, i, value):
        self.c_tree.Update(i, value)

    def Search(self, value):
        self.c_tree.Search(value)

    def ResetTree(self, value):
        self.c_tree.ResetTree(value)
