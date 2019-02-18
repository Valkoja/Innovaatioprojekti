using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Holds values in irl values
public class MachineState : MonoBehaviour
{
    public float mainBoomAngle = 0f;
    public float diggingArmAngle = 0f;
    public float bucketAngle = 0f;

    void Start()
    {
        // Reasonable initial state
        this.mainBoomAngle = 45;
        this.diggingArmAngle = -120;
        this.bucketAngle = -30;
    }

    void Update()
    {

    }

    public void consumeMessage(MachineStateMessage message)
    {
        if(message.quaternions.main_boom_orientation != null) {
            var quat = message.quaternions.main_boom_orientation;
            this.mainBoomAngle = xAngleFromRawQuaternion(quat);
        }
        if(message.quaternions.digging_arm_orientation != null) {
            var quat = message.quaternions.digging_arm_orientation;
            this.diggingArmAngle = xAngleFromRawQuaternion(quat);
        }
        if(message.quaternions.bucket_orientation != null) {
            var quat = message.quaternions.bucket_orientation;
            this.bucketAngle = xAngleFromRawQuaternion(quat);
        }
    }

    public float xAngleFromRawQuaternion(RawQuaternion quaternion) {
        return new Quaternion(quaternion.x, quaternion.y, quaternion.z, quaternion.w).eulerAngles.x;
    }
}
