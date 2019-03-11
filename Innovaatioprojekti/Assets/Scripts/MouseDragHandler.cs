using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseDragHandler : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    void OnMouseDrag()
    {
        Event e = Event.current;
        if (e.isMouse)
        {
            Debug.Log(e.delta);
        }
        else
        {
            Debug.Log("aintmouse");
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
