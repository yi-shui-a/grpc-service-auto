#include "FusionData.h"

int getFusionData(FusionInput *fusionInput, FusionOutput *fusionOutput){
    // 检查输入是否为空
    if (fusionInput == nullptr || fusionOutput == nullptr) {
        return ATOMIC_SERVICE_ERROR;
    }
    // 将fusionInput赋值给fusionOutput
    fusionOutput ->detection_result = fusionInput ->detection_result;
    fusionOutput ->radar_result = fusionInput ->radar_result;
    fusionOutput ->motor_result = fusionInput ->motor_result;
    fusionOutput ->robot_result = fusionInput ->robot_result;
    return ATOMIC_SERVICE_SUCCESS;
}