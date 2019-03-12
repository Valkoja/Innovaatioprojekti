using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LookAtTarget : MonoBehaviour
{
	public Transform target;
    bool spinCamera;
    public Transform cameraItem;
    float cameraHeight;
    public Slider cameraZoomSlider;
    float cameraCenterHeight;
    float cameraZoom;
	
    // Start is called before the first frame update
    void Start()
    {
        spinCamera = true;
        cameraHeight = 0.5f;
        //cameraCenterHeight = 0.3f;
        //cameraZoom = 3.0f;
    }

    // Update is called once per frame
    void Update()
    {
        if (spinCamera)
        {
            CameraSpinAction();
        }
        else
        {
            if (Input.GetMouseButtonDown(0))
            {
                Debug.Log(Input.mousePosition);
            }
            //handle mouse drag
        }
        
        transform.LookAt(target.transform);
    }

    void CameraSpinAction()
    {
        transform.Translate(Vector3.right * Time.deltaTime);
    }

    public void SetCameraSpin(bool b)
    {
        spinCamera = b;
    }

    public void SetCameraHeight(float f)
    {
        cameraHeight = f;
        cameraItem.position = new Vector3(cameraItem.position.x, cameraHeight, cameraItem.position.z);
    }

    public void SetCameraCenterHeight(float f)
    {
        target.position = new Vector3(target.position.x, f, target.position.z);
    }

    public void SetCameraZoom(float f)
    {
        float distance = 0.0f;
        f = -(f - (cameraZoomSlider.maxValue + cameraZoomSlider.minValue));
        distance = Vector3.Distance(new Vector3(target.position.x,0f,target.position.z), new Vector3(cameraItem.position.x,0f,cameraItem.position.z));
        cameraItem.Translate(Vector3.forward * (distance-f));
        cameraItem.position = new Vector3(cameraItem.position.x, cameraHeight, cameraItem.position.z);
    }
}
