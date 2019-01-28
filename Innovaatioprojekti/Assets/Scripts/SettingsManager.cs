using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;

public class SettingsManager : MonoBehaviour
{
    public bool CoordVisibility;
    public string IPaddress;

    // Start is called before the first frame update
    void Start()
    {
        CoordVisibility = true;
        IPaddress = "";
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    
}
