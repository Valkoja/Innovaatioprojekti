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
        if (stateObject) {
            var boomAngle = stateObject.GetComponent<MachineState>().mainBoomQuaternionAngle;
            var armAngle = stateObject.GetComponent<MachineState>().diggingArmQuaternionAngle;
            var zRotation = (armAngle - boomAngle) * -1;
            transform.localEulerAngles = new Vector3(0, 0, zRotation);
        }
    }
}