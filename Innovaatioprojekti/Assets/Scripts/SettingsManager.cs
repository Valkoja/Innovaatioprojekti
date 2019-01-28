using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SettingsManager : MonoBehaviour
{
    public bool CoordVisibility;
    public bool FPSVisibility;
    public string IPaddress;

    // Start is called before the first frame update
    void Start()
    {
        CoordVisibility = true;
        FPSVisibility = true;
        IPaddress = "";
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
