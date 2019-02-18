using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainBoom : MonoBehaviour
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
            var xRotation = stateObject.GetComponent<MachineState>().mainBoomAngle;
            // Add 90 so we're moving zero point to be perpendicular to the ground
            transform.localEulerAngles = new Vector3(-xRotation+90, 0, 0);
        }
    }
}
