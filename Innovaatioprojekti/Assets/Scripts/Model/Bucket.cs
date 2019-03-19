using System.Collections;
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
        if (stateObject) {
            var armAngle = stateObject.GetComponent<MachineState>().diggingArmQuaternionAngle;
            var bucketAngle = stateObject.GetComponent<MachineState>().bucketQuaternionAngle;
            var zRotation = (bucketAngle - armAngle) * -1;
            transform.localEulerAngles = new Vector3(0, 0, zRotation);
        }
    }
}