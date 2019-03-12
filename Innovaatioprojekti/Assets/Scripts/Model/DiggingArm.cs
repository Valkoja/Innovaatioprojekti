using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DiggingArm : MonoBehaviour
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
            // var xRotation = stateObject.GetComponent<MachineState>().diggingArmAngle;
            // Add 90 so we're moving zero point to be perpendicular to the ground
            // transform.localEulerAngles = new Vector3(-xRotation, 0, 0);
            
            var zRotation = stateObject.GetComponent<MachineState>().diggingArmAngle + stateObject.GetComponent<MachineState>().mainBoomAngle;
            transform.localEulerAngles = new Vector3(0, 0, -zRotation);
        }
    }
}