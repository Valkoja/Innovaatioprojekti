using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Holds values in irl values
public class MachineState : MonoBehaviour
{
    public Quaternion mainBoomRotation;
    public Quaternion diggingArmRotation;
    public Quaternion bucketRotation;

    public float mainBoomAngle;
    public float diggingArmAngle;
    public float bucketAngle;

    void Start()
    {
        // Reasonable initial state
        this.mainBoomRotation = Quaternion.Euler(35, 0, 0);
        this.diggingArmRotation = Quaternion.Euler(35, 0, 0);
        this.bucketRotation = Quaternion.Euler(35, 0, 0);

        this.mainBoomAngle = 40f;
        this.diggingArmAngle = -100f;
        this.bucketAngle = -90f;
    }

    void Update()
    {

    }

    public void consumeMessage(MachineStateMessage message)
    {
        if(message.quaternions.main_boom_orientation != null) {
            var quat = message.quaternions.main_boom_orientation;
            // this.mainBoomRotation = new Quaternion(quat.x, quat.y, quat.z, quat.w);
            this.mainBoomAngle = getEulerXAngle(quat.w, quat.x, quat.y, quat.z);
        }
        if(message.quaternions.digging_arm_orientation != null) {
            var quat = message.quaternions.digging_arm_orientation;
            // this.diggingArmRotation = new Quaternion(quat.x, quat.y, quat.z, quat.w);
            this.diggingArmAngle = getEulerXAngle(quat.w, quat.x, quat.y, quat.z);
        }
        if(message.quaternions.bucket_orientation != null) {
            var quat = message.quaternions.bucket_orientation;
            // this.bucketRotation = new Quaternion(quat.x, quat.y, quat.z, quat.w);
            this.bucketAngle = getEulerXAngle(quat.w, quat.x, quat.y, quat.z);
        }
        // this.mainBoomAngle = message.angles.main_boom / 10;
        // this.diggingArmAngle = message.angles.digging_arm / 10;
        // this.bucketAngle = message.angles.bucket / 10;
    }

    // public static float getAngle(float angle) {
    //     return (angle > 180) ? angle - 360 : angle;
    // }

    public static float getEulerXAngle(float w, float x, float y, float z) {
        // roll (x-axis rotation)
        var sinr_cosp = +2.0f* w * x + y * z;
        var cosr_cosp = +1.0f - 2.0f * x * x + y * y;
        var roll = (float)Math.Atan2(sinr_cosp, cosr_cosp);
        return Mathf.Rad2Deg * roll;
    }
}
