#include "ImageDetection.h"

int count = 0;

int imageDetect(RequestSignal *requestSignal, DetectionResult *detectionResult)
{
    // 随机生成一个检测结果
    detectionResult->camera_id = 1;
    detectionResult->object_class = "person";
    detectionResult->confidence = 0.9;
    detectionResult->x_min = 0.1 + count * 0.1;
    detectionResult->y_min = 0.1 + count * 0.1;
    detectionResult->x_max = 0.9 + count * 0.1;
    detectionResult->y_max = 0.9 + count * 0.1;
    count++;
    return ATOMIC_SERVICE_SUCCESS;
}
int statusDetect(RequestSignal *requestSignal, CameraStatus *cameraStatus)
{
    // 随机生成一个状态
    cameraStatus->status_code = 1;
    cameraStatus->description = "Camera is ready";
    return ATOMIC_SERVICE_SUCCESS;
}