using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ChangeTabHandler : MonoBehaviour
{

    public GameObject generalPanel;
    public GameObject renderPanel;
    public GameObject connectionPanel;

    public Image generalImage;
    public Image renderImage;
    public Image connectionImage;

    bool generalPanelVisibility;
    bool renderPanelVisibility;
    bool connectionPanelVisibility;
    

    Color32 activeButtonColor; // 137x3 + 34
    Color32 inactiveButtonColor; // 255x3 + 34

    // Start is called before the first frame update
    void Start()
    {
        generalPanelVisibility = true;
        renderPanelVisibility = false;
        connectionPanelVisibility = false;
        activeButtonColor = new Color32(0x89, 0x89, 0x89, 0x22);
        inactiveButtonColor = new Color32(0xFF, 0xFF, 0xFF, 0x22);
        generalImage.color = activeButtonColor;
        renderImage.color = inactiveButtonColor;
        connectionImage.color = inactiveButtonColor;
        generalPanel.SetActive(generalPanelVisibility);
        renderPanel.SetActive(renderPanelVisibility);
        connectionPanel.SetActive(connectionPanelVisibility);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetCurrentPanelToGeneral()
    {
        generalPanelVisibility = true;
        renderPanelVisibility = false;
        connectionPanelVisibility = false;
        generalPanel.SetActive(generalPanelVisibility);
        renderPanel.SetActive(renderPanelVisibility);
        connectionPanel.SetActive(connectionPanelVisibility);
        generalImage.color = activeButtonColor;
        renderImage.color = inactiveButtonColor;
        connectionImage.color = inactiveButtonColor;
    }

    public void SetCurrentPanelToRender()
    {
        generalPanelVisibility = false;
        renderPanelVisibility = true;
        connectionPanelVisibility = false;
        renderPanel.SetActive(renderPanelVisibility);
        generalPanel.SetActive(generalPanelVisibility);
        connectionPanel.SetActive(connectionPanelVisibility);
        generalImage.color = inactiveButtonColor;
        renderImage.color = activeButtonColor;
        connectionImage.color = inactiveButtonColor;
    }

    public void SetCurrentPanelToConnection()
    {
        renderPanelVisibility = false;
        generalPanelVisibility = false;
        connectionPanelVisibility = true;
        renderPanel.SetActive(renderPanelVisibility);
        generalPanel.SetActive(generalPanelVisibility);
        connectionPanel.SetActive(connectionPanelVisibility);
        generalImage.color = inactiveButtonColor;
        renderImage.color = inactiveButtonColor;
        connectionImage.color = activeButtonColor;
    }
}
