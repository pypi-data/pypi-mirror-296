cmake_minimum_required(VERSION 3.15...3.29)
project(pyix LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Add FetchContent functionality
include(FetchContent)

# SDK Major version
set(SDK_MAJOR_VERSION "3")

# System name (lower case)
string(TOLOWER ${CMAKE_SYSTEM_NAME} SYSTEM_NAME_LC)

# File format extension
if (WIN32)
    set(SDK_PACKAGE_EXT ".zip")
else ()
    set(SDK_PACKAGE_EXT ".tgz")
endif ()

# Account for ARM based linux systems
if (NOT APPLE AND UNIX AND CMAKE_SYSTEM_PROCESSOR STREQUAL "aarch64")
    set(LINUX_ARCH "-arm64")
else ()
    set(LINUX_ARCH "")
endif ()

# Setup ImageSDK Download
FetchContent_Declare(ImageSDK
        URL "https://developer.phaseone.com/sdk/3.1/releases/imagesdk/${SDK_MAJOR_VERSION}/p1imagesdk-${SYSTEM_NAME_LC}${LINUX_ARCH}${SDK_PACKAGE_EXT}"
        SOURCE_DIR ImageSDK
)
# Download ImageSDK for the current system
message(STATUS "Downloading ImageSDK...")
FetchContent_Populate(ImageSDK)
find_package(ImageSDK CONFIG REQUIRED HINTS ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK)

# Add pybind11 2.13.1
set(PYBIND11_FINDPYTHON ON)
FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.13.1
)
FetchContent_MakeAvailable(pybind11)

# Add Python module
pybind11_add_module(pyix MODULE src/bindings.cpp)

# Set output name to avoid conflicts
set_target_properties(pyix PROPERTIES PREFIX "" OUTPUT_NAME "pyix")

# Link dynamic with ImageSDK
target_include_directories(pyix PRIVATE
        ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/include)
target_link_libraries(pyix PRIVATE
        ImageSDK::ImageSdkCpp
        shlwapi
)

set(REQUIRED_DLLS
        $<TARGET_FILE:ImageSDK::ImageSdkCpp>
        ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/lib/libifcoremd.dll
        ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/lib/libifportmd.dll
        ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/lib/libmmd.dll
        ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/lib/P1CIRSTACK.dll
        ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/lib/Qt5Core.dll
)

if(WIN32)
    # Copy DLLs to build directory
    add_custom_command(TARGET pyix POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different ${REQUIRED_DLLS} $<TARGET_FILE_DIR:pyix>
    )
endif()

# Get the Python site-packages directory
execute_process(
        COMMAND "${Python_EXECUTABLE}" -c "import site; print(site.getsitepackages()[0])"
        OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Ensure the path is in the correct format for CMake on Windows
if(WIN32)
#    set(PYTHON_SITE_PACKAGES "${PYTHON_SITE_PACKAGES}/Lib")
    string(REPLACE "\\" "/" PYTHON_SITE_PACKAGES ${PYTHON_SITE_PACKAGES})
endif()

message(STATUS "Python site-packages directory: ${PYTHON_SITE_PACKAGES}")

# Installation
install(TARGETS pyix DESTINATION "${PYTHON_SITE_PACKAGES}")
install(FILES ${REQUIRED_DLLS} DESTINATION "${PYTHON_SITE_PACKAGES}")
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/SensorProfiles DESTINATION "${PYTHON_SITE_PACKAGES}")

# Install SensorProfiles to the Python site-packages directory
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/ImageSDK/SensorProfiles
        DESTINATION "${PYTHON_SITE_PACKAGES}"
        COMPONENT Runtime)

# Install ColorProfiles from source directory to the Python site-packages directory
install(DIRECTORY src/ColorProfiles
        DESTINATION "${PYTHON_SITE_PACKAGES}"
        COMPONENT Runtime)
