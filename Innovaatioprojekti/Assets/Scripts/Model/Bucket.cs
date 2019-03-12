﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bucket : MonoBehaviour
{
    private GameObject stateObject;

    // Start is called before the first frame update
    void Start()
    {
        this.stateObject = GameObject.Find("MachineState");
    }

    // Update is called once per frame
    void Update()
    {
        if(stateObject) {
            // Old:
            // var xRotation = stateObject.GetComponent<MachineState>().bucketAngle;
            // Add 90 so we're moving zero point to be perpendicular to the ground
            // transform.localEulerAngles = new Vector3(-xRotation, 0, 0);

            var rotations = stateObject.GetComponent<MachineState>().mainBoomAngle + stateObject.GetComponent<MachineState>().diggingArmAngle;
            var zRotation = stateObject.GetComponent<MachineState>().bucketAngle + rotations;
            transform.localEulerAngles = new Vector3(0, 0, -zRotation);
        }
    }
}