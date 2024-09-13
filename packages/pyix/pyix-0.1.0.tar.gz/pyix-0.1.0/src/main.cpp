#include <iostream>
#include <string>
#include <map>
#include <fstream>
#include <windows.h>
#include <shlwapi.h>
#include <vector>
#include "P1Image.hpp"
#include "P1ImageTiffWriter.hpp"
#include "P1ImageRawImage.hpp"
#include "P1ImageConvertConfig.hpp"
#include "P1ImageStacking.hpp"

#pragma comment(lib, "shlwapi.lib")

struct CalibrationData {
    double pixelSize;
    double focalLength;
    double xp;
    double yp;
    double k1;
    double k2;
    double k3;
    double p1;
    double p2;
    double b1;
    double b2;
};

P1::ImageSdk::GeometricCorrection createGeometricCorrection(const CalibrationData &data) {
    P1::ImageSdk::GeometricCorrection correction;
    correction.pixelSize = data.pixelSize;
    correction.focalLength = data.focalLength;
    correction.xp = data.xp;
    correction.yp = data.yp;
    correction.k1 = data.k1;
    correction.k2 = data.k2;
    correction.k3 = data.k3;
    correction.p1 = data.p1;
    correction.p2 = data.p2;
    correction.b1 = data.b1;
    correction.b2 = data.b2;
    return correction;
}

CalibrationData createCalibrationData(const std::map<std::string, double> &calibrationMap) {
    CalibrationData data;
    data.pixelSize = calibrationMap.at("pixelSize");
    data.focalLength = calibrationMap.at("focalLength");
    data.xp = calibrationMap.at("xp");
    data.yp = calibrationMap.at("yp");
    data.k1 = calibrationMap.at("k1");
    data.k2 = calibrationMap.at("k2");
    data.k3 = calibrationMap.at("k3");
    data.p1 = calibrationMap.at("p1");
    data.p2 = calibrationMap.at("p2");
    data.b1 = calibrationMap.at("b1");
    data.b2 = calibrationMap.at("b2");
    return data;
}

std::string get_module_path() {
    wchar_t path[MAX_PATH];
    GetModuleFileNameW(NULL, path, MAX_PATH);

    // Convert wide string to narrow string
    char str[MAX_PATH];
    WideCharToMultiByte(CP_UTF8, 0, path, -1, str, MAX_PATH, NULL, NULL);

    return std::string(str);
}

std::string get_base_path() {
    std::string module_path = get_module_path();
    char drive[_MAX_DRIVE];
    char dir[_MAX_DIR];
    _splitpath_s(module_path.c_str(), drive, _MAX_DRIVE, dir, _MAX_DIR, nullptr, 0, nullptr, 0);

    return std::string(drive) + std::string(dir);
}

std::string get_sensor_profiles_path() {
    std::string base_path = get_base_path();
    std::string sensor_profiles_path = base_path + "SensorProfiles";

    // If the path doesn't exist, try the site-packages location
    if (!PathFileExistsA(sensor_profiles_path.c_str())) {
        sensor_profiles_path = base_path + R"(Lib\site-packages\SensorProfiles)";
    }

    return sensor_profiles_path;
}

std::string get_color_profiles_path() {
    std::string base_path = get_base_path();
    std::string color_profiles_path = base_path + "ColorProfiles";

    // If the path doesn't exist, try the site-packages location
    if (!PathFileExistsA(color_profiles_path.c_str())) {
        color_profiles_path = base_path + R"(Lib\site-packages\ColorProfiles)";
    }

    return color_profiles_path;
}

int processImages(const std::string &rgbPath, const std::map<std::string, double> &rgbCalibrationMap,
                  const std::string &nirPath, const std::map<std::string, double> &nirCalibrationMap,
                  const std::string &outputPath) {
    try {
        std::string sensorProfilesPath = get_sensor_profiles_path();
        std::cout << "Using SensorProfiles from: " << sensorProfilesPath << std::endl;

        // Initialize the SDK with the automatically detected SensorProfiles path
        P1::ImageSdk::SetSensorProfilesLocation(sensorProfilesPath);
        P1::ImageSdk::Initialize();

        CalibrationData rgbCalibration = createCalibrationData(rgbCalibrationMap);
        CalibrationData nirCalibration = createCalibrationData(nirCalibrationMap);

        // Open and convert RGB IIQ file
        std::cout << "Open RGB IIQ file" << std::endl;
        P1::ImageSdk::RawImage rgb_iiq(rgbPath);

        P1::ImageSdk::GeometricCorrection rgb_calibration = createGeometricCorrection(rgbCalibration);

        std::cout << "Do the RGB conversion..." << std::endl;
        P1::ImageSdk::ConvertConfig rgb_config;
        rgb_config.SetGeometricCorrectionEnabled(true);
        rgb_config.SetGeometricCorrection(rgb_calibration);
        // rgb_config.SetOutputColorSpace(P1::ImageSdk::ColorSpace::adobeRGB);
        P1::ImageSdk::BitmapImage rgb_bitmap = rgb_config.ApplyTo(rgb_iiq);
        std::cout << "RGB Image dimensions: " << rgb_bitmap.Width() << "x" << rgb_bitmap.Height() << std::endl;

        // Open and convert NIR IIQ file
        std::cout << "Open NIR IIQ file" << std::endl;
        P1::ImageSdk::RawImage nir_iiq(nirPath);

        P1::ImageSdk::GeometricCorrection nir_calibration = createGeometricCorrection(nirCalibration);

        std::cout << nir_calibration.ToString() << std::endl;

        P1::ImageSdk::ConvertConfig nir_config;
        nir_config.SetGeometricCorrectionEnabled(false);
        // nir_config.SetOutputColorSpace(P1::ImageSdk::ColorSpace::adobeRGB);
        P1::ImageSdk::BitmapImage nir_bitmap = nir_config.ApplyTo(nir_iiq);
        std::cout << "NIR Image dimensions: " << nir_bitmap.Width() << "x" << nir_bitmap.Height() << std::endl;

        // Setup and do the image stacking
        P1::ImageSdk::StackingOutput output;
        output.hasRgbiBitmap = true;

        P1::ImageSdk::GeometricCorrection stacked_calibration;
        stacked_calibration.pixelSize = rgbCalibration.pixelSize;
        stacked_calibration.focalLength = rgbCalibration.focalLength;

        P1::ImageSdk::Stacking stacking;
        stacking.DoStacking(rgb_iiq, rgb_bitmap, stacked_calibration, nir_iiq, nir_bitmap, nir_calibration, output);

        std::cout << "Write image to tiff file..." << std::endl;
        P1::ImageSdk::TiffConfig outputConfig;
        outputConfig.tileSize = P1::ImageSdk::tileSize512;
        outputConfig.compression = P1::ImageSdk::TiffCompressionScheme_LZW;

        // AdobeRGB colour space
        outputConfig.commonConfig.outputColorSpace = P1::ImageSdk::ColorSpace::adobeRGB;

        std::string colorProfileFilename = get_color_profiles_path() + "\\Adobe RGB (1998).icm";
        std::cout << "Using color profile: " << colorProfileFilename << std::endl;

        std::ifstream file(colorProfileFilename, std::ios::binary | std::ios::ate);
        if (file.is_open()) {
            std::streamsize size = file.tellg();
            file.seekg(0, std::ios::beg);

            std::vector<char> colorProfileBuffer(size);
            if (file.read(colorProfileBuffer.data(), size)) {
                outputConfig.commonConfig.iccProfileData = colorProfileBuffer.data();
                outputConfig.commonConfig.iccProfileSize = static_cast<size_t>(size);
                std::cout << "ICC profile size: " << size << std::endl;
            } else {
                std::cout << "Could not read ICC profile" << std::endl;
            }
        } else {
            std::cout << "Could not open ICC profile file" << std::endl;
        }

        P1::ImageSdk::TiffWriter(outputPath, output.RgbiBitmap, rgb_iiq, outputConfig);

        std::cout << "Done!" << std::endl;
        return 0;
    }
    catch (P1::ImageSdk::SdkException &exception) {
        std::cout << "Exception: " << exception.what()
                  << "\nCode: " << exception.mCode
                  << "\nLine: " << exception.mLineNo
                  << std::endl;
        return 1;
    }
    catch (...) {
        std::cout << "Some other exception!" << std::endl;
        return -1;
    }
}
