using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class TogglePanelVisibility : MonoBehaviour
{

    public GameObject childPanel;

    private bool panelVisibility;

    // Start is called before the first frame update
    void Start()
    {
        panelVisibility = false;
        childPanel.SetActive(panelVisibility);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void visibilityToggle()
    {
        panelVisibility = !panelVisibility;
        childPanel.SetActive(panelVisibility);
    }
}
