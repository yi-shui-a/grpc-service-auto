#include "FusionData.h"

int getFusionData(FusionInput *fusionInput, FusionOutput *fusionOutput){
    // 检查输入是否为空
    if (fusionInput == nullptr || fusionOutput == nullptr) {
        return ATOMIC_SERVICE_ERROR;
    }
    // 将fusionInput赋值给fusionOutput
    fusionOutput ->number1 = fusionInput ->camera_id;
    fusionOutput ->number1 = fusionInput ->robot_id;
    return ATOMIC_SERVICE_SUCCESS;
}