using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LookAtTarget : MonoBehaviour
{
	public Transform target;
    bool spinCamera;
    public Transform cameraItem;
    float cameraHeight;
    float cameraCenterHeight;

	
    // Start is called before the first frame update
    void Start()
    {
        spinCamera = true;
        cameraHeight = 0.5f;
        cameraCenterHeight = 0.3f;
    }

    // Update is called once per frame
    void Update()
    {
        if (spinCamera)
        {
            cameraSpinAction();
        }
        target.position = new Vector3(target.position.x, cameraCenterHeight, target.position.z);
        cameraItem.position = new Vector3(cameraItem.position.x, cameraHeight, cameraItem.position.z);
        //target.position.y = cameraCenterHeight;
    }

    void cameraSpinAction()
    {
        transform.LookAt(target.transform);
        transform.Translate(Vector3.right * Time.deltaTime);
    }

    public void setCameraSpin(bool b)
    {
        spinCamera = b;
    }

    public void setCameraHeight(float f)
    {
        cameraHeight = f;
    }

    public void setCameraCenterHeight(float f)
    {
        cameraCenterHeight = f;
    }
}
