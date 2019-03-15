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
    Vector3 lastMousePosition;
    float cameraRotationX = -1f;
    float cameraRotationY = -1f;
    float cameraRotateSpeed = 3;
	
    // Start is called before the first frame update
    void Start()
    {
        lastMousePosition.Set(0.0f, 0.0f, 0.0f);
        spinCamera = false;
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
                lastMousePosition = Input.mousePosition;
            if (Input.GetMouseButton(0))
            {
                Vector3 pos = Camera.main.ScreenToViewportPoint(Input.mousePosition-lastMousePosition);
                Vector3 move = new Vector3(pos.x*cameraRotateSpeed*cameraRotationX, pos.y * cameraRotateSpeed * cameraRotationY, 0);
                cameraItem.Translate(move);
                lastMousePosition = Input.mousePosition;
            }
            if (Input.GetAxis("Mouse ScrollWheel") > 0f) 
            {
                cameraItem.Translate(Vector3.forward * 0.5f);
            }
            else if (Input.GetAxis("Mouse ScrollWheel") < 0f )
            {
                cameraItem.Translate(Vector3.forward * -0.5f);
            }
            CheckCameraBoundaries();
        }
            
        transform.LookAt(target.transform);
    }

    public void ReverseCameraX(bool r)
    {
        if (r)
        {
            cameraRotationX = -1;
        }
        else
        {
            cameraRotationX = 1;
        }
    }

    public void ReverseCameraY(bool r)
    {
        if (r)
        {
            cameraRotationY = -1;
        }
        else
        {
            cameraRotationY = 1;
        }
    }

    void CheckCameraBoundaries()
    {
        float Distance = Vector3.Distance(new Vector3(target.position.x, 0f, target.position.z), new Vector3(cameraItem.position.x, 0f, cameraItem.position.z));
        if (Distance > 5f)
        {
            cameraItem.Translate(Vector3.forward * (Distance-5f));
        }
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
