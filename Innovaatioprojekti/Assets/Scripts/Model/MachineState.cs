using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Holds values in irl values
public class MachineState : MonoBehaviour
{
    // Raw quaternions from device
    public Quaternion mainBoomQuaternion;
    public Quaternion diggingArmQuaternion;
    public Quaternion bucketQuaternion;
    public Quaternion frameQuaternion;

    // Euler angles from device
    public float mainBoomEulerAngle;
    public float diggingArmEulerAngle;
    public float bucketEulerAngle;
    public float framePitchEulerAngle;
    public float frameRollEulerAngle;
    public float headingEulerAngle;

    // Converted euler angles from quaternions
    public float mainBoomQuaternionAngle;
    public float diggingArmQuaternionAngle;
    public float bucketQuaternionAngle;

    // Limit toggles
    public Boolean limitLeft;
    public Boolean limitRight;
    public Boolean limitUpper;
    public Boolean limitLower;
    public Boolean limitForward;
    public Boolean limitProperty;
    public Boolean limitOverload;

    // Zero level measurements
    public float zeroHeightFrom;
    public float zeroDistanceTo;
    public float zeroHeightToSlope;

    void Start()
    {
        // Reasonable initial state
        this.mainBoomQuaternion = Quaternion.Euler(0, 0, 0);
        this.diggingArmQuaternion = Quaternion.Euler(0, 0, 0);
        this.bucketQuaternion = Quaternion.Euler(0, 0, 0);
        this.frameQuaternion = Quaternion.Euler(0, 0, 0);

        this.mainBoomQuaternionAngle = 40f;
        this.diggingArmQuaternionAngle = -100f;
        this.bucketQuaternionAngle = -90f;

        this.mainBoomEulerAngle = 40f;
        this.diggingArmEulerAngle = -100f;
        this.bucketEulerAngle = -90f;
        this.framePitchEulerAngle = 0f;
        this.frameRollEulerAngle = 0f;
        this.headingEulerAngle = 0f;
        
        this.limitLeft = false;
        this.limitRight = false;
        this.limitUpper = false;
        this.limitLower = false;
        this.limitForward = false;
        this.limitProperty = false;
        this.limitOverload = false;
        
        this.zeroHeightFrom = 0.0f;
        this.zeroDistanceTo = 0.0f;
        this.zeroHeightToSlope = 0.0f;
    }

    void Update()
    {

    }

    public void consumeMessage(MachineStateMessage message)
    {
        // Quaternions & derived angles
        if (message.quaternions.main_boom_orientation != null) {
            var quat = message.quaternions.main_boom_orientation;
            this.mainBoomQuaternion = new Quaternion(quat.x, quat.y, quat.z, quat.w);
            this.mainBoomQuaternionAngle = getEulerXAngle(quat.w, quat.x, quat.y, quat.z);
        }

        if (message.quaternions.digging_arm_orientation != null) {
            var quat = message.quaternions.digging_arm_orientation;
            this.diggingArmQuaternion = new Quaternion(quat.x, quat.y, quat.z, quat.w);
            this.diggingArmQuaternionAngle = getEulerXAngle(quat.w, quat.x, quat.y, quat.z);
        }

        if (message.quaternions.bucket_orientation != null) {
            var quat = message.quaternions.bucket_orientation;
            this.bucketQuaternion = new Quaternion(quat.x, quat.y, quat.z, quat.w);
            this.bucketQuaternionAngle = getEulerXAngle(quat.w, quat.x, quat.y, quat.z);
        }

        if (message.quaternions.frame_orientation != null) {
            var quat = message.quaternions.frame_orientation;
            this.frameQuaternion = new Quaternion(quat.x, quat.y, quat.z, quat.w);
        }

        // Euler angles
        if (message.angles.main_boom != null) {
            this.mainBoomEulerAngle = message.angles.main_boom;
        }

        if (message.angles.digging_arm != null) {
            this.diggingArmEulerAngle = message.angles.digging_arm;
        }

        if (message.angles.bucket != null) {
            this.bucketEulerAngle = message.angles.bucket;
        }

        if (message.angles.heading != null) {
            this.headingEulerAngle = message.angles.heading;
        }

        if (message.angles.frame_pitch != null) {
            this.framePitchEulerAngle = message.angles.frame_pitch;
        }

        if (message.angles.frame_roll != null) {
            this.frameRollEulerAngle = message.angles.frame_roll;
        }

        // Limit warnings
        if (message.limitWarnings.left != null) {
            this.limitLeft = message.limitWarnings.left;
        }

        if (message.limitWarnings.right != null) {
            this.limitRight = message.limitWarnings.right;
        }

        if (message.limitWarnings.upper != null) {
            this.limitUpper = message.limitWarnings.upper;
        }

        if (message.limitWarnings.lower != null) {
            this.limitLower = message.limitWarnings.lower;
        }

        if (message.limitWarnings.forward != null) {
            this.limitForward = message.limitWarnings.forward;
        }

        if (message.limitWarnings.property != null) {
            this.limitProperty = message.limitWarnings.property;
        }

        if (message.limitWarnings.overload != null) {
            this.limitOverload = message.limitWarnings.overload;
        }

        // Zero level
        if (message.zeroLevel.height_from_zero != null) {
            this.zeroHeightFrom = message.zeroLevel.height_from_zero;
        }

        if (message.zeroLevel.distance_to_zero != null) {
            this.zeroDistanceTo = message.zeroLevel.distance_to_zero;
        }

        if (message.zeroLevel.height_to_slope_from_zero != null) {
            this.zeroHeightToSlope = message.zeroLevel.height_to_slope_from_zero;
        }
    }

    public static float getEulerXAngle(float w, float x, float y, float z) {
        // roll (x-axis rotation)
        var sinr_cosp = +2.0f* w * x + y * z;
        var cosr_cosp = +1.0f - 2.0f * x * x + y * y;
        var roll = (float)Math.Atan2(sinr_cosp, cosr_cosp);

        return Mathf.Rad2Deg * roll;
    }
}