#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "main.cpp"

namespace py = pybind11;

PYBIND11_MODULE(pyix, m) {
    m.doc() = "Image stacking module for RGB and NIR images";

    m.def("stack_images", &processImages,
          py::arg("rgb_path"),
          py::arg("rgb_calibration_map"),
          py::arg("nir_path"),
          py::arg("nir_calibration_map"),
          py::arg("output_path"),
          "Stack RGB and NIR images and save the result");
}