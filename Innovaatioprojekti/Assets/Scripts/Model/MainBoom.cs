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
        if (stateObject) {
            var zRotation = stateObject.GetComponent<MachineState>().mainBoomQuaternionAngle;
            transform.localEulerAngles = new Vector3(0, 0, -zRotation);
        }
    }
}
